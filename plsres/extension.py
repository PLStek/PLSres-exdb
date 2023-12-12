import os
import re
import io
import sys
import math
import time
import html
import yaml
import json
import locale
import builtins
import platform
import subprocess
import xml.etree.ElementTree as etree

import markdown
import markdown.util
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor, RawHtmlPostprocessor

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .util import Attributes

### Extension detection patterns
EXT_META_PREFIX = "////"
EXT_META_ASSIGN_REGEX = re.compile(r"[ \t]*([a-zA-Z_]\w*)[ \t]*=[ \t]*(.+)")
EXT_MATH_BLOCK_REGEX = re.compile(r"^\$\$(.*?)\$\$$", re.MULTILINE | re.DOTALL)
EXT_CODE_START_REGEX = re.compile(r"```[ \t]*((?P<lang>\w+)([ \t]*/[ \t]*((?P<mode>\w*)([ \t]*/[ \t]*(?P<params>.+?))?)?)?)?[ \t]*\n(?P<code>.*?)\s*```", re.MULTILINE | re.DOTALL)
EXT_COLLECTION_REGEX = re.compile(r"\{!collection[ \t]*:[ \t]*(?P<name>.*?)\}")
EXT_EXERCISE_REGEX = re.compile(r"\{!exerci[cs]e[ \t]*:[ \t]*(?P<name>.*?)\}")
EXT_EXPR_PATTERN = r"\{=(=)?[ \t]*(.+?)[ \t]*(:(.*?))?\}"
EXT_LINK_PATTERN = r"\{>[ \t]*(.+?)([ \t]*:[ \t]*(.+?))?\}"
EXT_ESCAPE_PATTERN = r"\\([ \t\n]+|>|<)"
EXT_MATH_PATTERN = r"\$\$(.*?)\$\$"
EXT_DELETE_PATTERN = r"~~(.*?)~~"
EXT_UNDERLINE_PATTERN = r"__(.*?)__"
EXT_SVG_PATTERN = r"\{!svg[ \t]*:[ \t]*(?P<name>.*?)([ \t]*:[ \t]*(?P<alt>.*?))?\}"
EXT_IMG_PATTERN = r"\{!img[ \t]*:[ \t]*(?P<name>.*?)([ \t]*:[ \t]*(?P<alt>.*?))?\}"
EXT_CONTENT_ANCHOR_SEP = "////"
EXT_FENCE_REGEX = re.compile(r";;;[ \t]*(?P<type>[\w_-]+)?", re.MULTILINE | re.DOTALL);

# Load the fence settings
with open(os.path.join("template", "fence.yml"), "r", encoding="utf-8") as fencefile:
	FENCE_PARAMETERS = yaml.load(fencefile.read(), yaml.Loader)


class PLSResExtension (Extension):
	"""Markdown extension for the PLSres. A new instance is created for each page"""
	def __init__(self, path, document, extconfig, parameters, ispage=True):
		super().__init__()
		self.path = path                               # Document file path
		self.document = document                       # Document object
		self.locals = {}                               # Document local variables
		self.config = extconfig
		self.parameters = parameters
		# extconfig["globals"]       # Site global variables
		# extconfig["licenses"]
		# extconfig["template"]      # HTML template for a web page
		# extconfig["pathtable"]     # Table docpath -> document
		# extconfig["documenttree"]  # Documents tree
		# extconfig["linktable"]     # Table docpath -> site path
		# extconfig["parenttable"]   # Table docpath -> parent document
		# extconfig["cache"]         # Compiler cache
		# extconfig["quick"]         # Whether to generate quickly (reuse cached results, ...)
		self.currentid = 0           # Unique id value within the document
		self.currentcode = 0         # Current code block ID
		self.keptfiles = {}
		self.ispage = ispage

	def extendMarkdown(self, md):
		md.preprocessors.register(MetaPreprocessor(self, md), "plsres_preprocess_variable", 1001)
		md.preprocessors.register(CodePreprocessor(self, md), "plsres_preprocess_code", 25)
		md.parser.blockprocessors.register(FenceProcessor(self, md.parser), "plsres_block_fence", 1002)
		md.parser.blockprocessors.register(FileCollectionProcessor(self, md.parser), "plsres_block_collection", 1001)
		md.parser.blockprocessors.register(ExerciseProcessor(md, self, md.parser), "plsres_block_exercise", 1000)
		md.parser.blockprocessors.register(MathBlockProcessor(md, self, md.parser), "plsres_block_math", 999)
		md.inlinePatterns.register(EscapeProcessor(self, md), "plsres_inline_escape", 1004)
		md.inlinePatterns.register(ExpressionProcessor(self, md), "plsres_inline_expression", 1003)
		md.inlinePatterns.register(InternalLinkProcessor(self, md), "plsres_inline_link", 1002)
		md.inlinePatterns.register(InternalSVGProcessor(self, md), "plsres_inline_svg", 1001)
		md.inlinePatterns.register(InternalImageProcessor(self, md), "plsres_inline_image", 1000)
		md.inlinePatterns.register(InlineMathProcessor(self, md), "plsres_inline_math", 999)
		md.inlinePatterns.register(DeleteProcessor(self, md), "plsres_inline_delete", 189)
		md.inlinePatterns.register(UnderlineProcessor(self, md), "plsres_inline_underline", 188)
		md.treeprocessors.register(StyleProcessor(self, md), "plsres_tree_style", 1000)
		if self.ispage:
			md.treeprocessors.register(ContentTreeProcessor(self, md), "plsres_tree_content", 0)
			if self.parameters.outformat == "html":
				md.postprocessors.register(TemplatePostprocessor(self, md), "plsres_postprocess_page", 0)
			else:
				md.postprocessors.register(JSONPostProcessor(self, md), "plsres_postprocess_page", 0)

	def uniqueid(self):
		"""Generate a unique ID within the document"""
		result = f"_plsres_id_{self.currentid}"
		self.currentid += 1
		return result

	def load_cache(self):
		if self.document.docpath not in self.config.cache.documents:
			self.config.cache.documents[self.document.docpath] = {}

	def doc_cache(self):
		return self.config.cache.documents[self.document.docpath]

	def start(self):
		self.load_cache()
		sys.path.append(os.path.abspath("temp"))

	def finish(self):
		"""Finish processing a document, write the cache"""
		self.config.cache.documents[self.document.docpath]["lastcompiled"] = time.time()
		sys.path.remove(os.path.abspath("temp"))


class MetaPreprocessor (Preprocessor):
	"""Processes the meta statements
	   Local variable definition :
	       //// variable = python expression
	"""
	def __init__(self, extension, *args, **kwargs):
		if extension is not None:
			super().__init__(*args, **kwargs)
			self.locals = extension.locals
			self.globals = extension.config.globals
		else:
			self.locals = {}
			self.globals = {}
		self.ext = extension

	def run(self, lines):
		result = []
		for i, line in enumerate(lines):
			if line.startswith(EXT_META_PREFIX):
				instruction = line.replace(EXT_META_PREFIX, "")
				if (match := EXT_META_ASSIGN_REGEX.match(instruction)):
					varname = match.group(1).strip()
					expression = match.group(2).strip()
					self.locals[varname] = eval(expression, self.globals, self.locals)
				else:
					raise SyntaxError(f"Invalid meta instruction at line {i} of file {self.ext.path} : `{instruction}`")
			else:
				result.append(line)
		return result

class CodePreprocessor (Preprocessor):
	"""Processes the code blocks
	   Simple code block :
	       ```language
		   code
		   ```
		With mode and parameters :
		   ```c/result/wrapmain; includes=["stdio.h", "stdlib.h"]
		   code
		   ```
	"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def run(self, lines):
		text = "\n".join(lines)
		while (match := EXT_CODE_START_REGEX.search(text)) is not None:
			lang = match.group("lang")
			mode = match.group("mode")
			if mode == "": mode = None
			paramstr = match.group("params")
			code = match.group("code")

			params = self.extract_params(lang, mode, paramstr)

			highlight_code, exec_code = self.preprocess_code(code)

			# Highlight with pygments
			if lang is not None:
				lexer = get_lexer_by_name(lang)
				formatter = HtmlFormatter(linenos=params["linenos"])
				html = highlight(highlight_code.strip("\n").rstrip(), lexer, formatter)
			else:
				html = "<pre>" + highlight_code + "</pre>"
			html = html.replace("`***", '<span class="code-emphasis">').replace("***`", '</span>')

			# Compute the results
			if mode == "result":
				if not params[".result.linux"] or platform.system() == "Linux":
					html += self.run_result(exec_code, lang, mode, params)
			elif mode == "keep":
				self.run_keep(exec_code, lang, mode, params)

			placeholder = self.md.htmlStash.store(html)
			text = text[:match.start()] + "\n" + placeholder + "\n" + text[match.end():]
			self.ext.currentcode += 1

			deleted = set()
			for name, counter in self.ext.keptfiles.items():
				if counter == 0:
					deleted.add(name)
				else:
					self.ext.keptfiles[name] -= 1
			for name in deleted:
				del self.ext.keptfiles[name]
				os.remove(os.path.join("temp", name))
		return text.split("\n")

	def preprocess_code(self, code):
		highlight_code = ""
		exec_code = ""
		highlight_only = False
		exec_only = False
		for line in code.splitlines():
			if line.strip() == "`!!!":
				exec_only = True
			elif line.strip() == "!!!`":
				exec_only = False
			elif line.strip() == "`///":
				highlight_only = True
			elif line.strip() == "///`":
				highlight_only = False
			else:
				if not highlight_only:
					exec_code += line + "\n"
				if not exec_only:
					highlight_code += line + "\n"
		return highlight_code, exec_code

	default_parameters = {
		# lang.mode.name
		"linenos": False,                  # Show the line numbers
		".keep.name": "__keep",            # File name to save the code under
		".keep.next": 0,                   # Number of following code blocks that need this file
		".result.stdin": "",               # String to put on the standard input
		".result.joinfiles": [],           # List of (file name, file content) for files that have to be along the program
		".result.argv": [],                # Command-line arguments for the program
		".result.linux": False,            # Compiles on linux only
		"c.result.wrapmain": False,        # Wrap the code in a default main function
		"c.result.includes": [],           # Standard headers to include
		"c.result.options": [],            # Misc compiler options
		"c.result.locale": False,          # Localized output encoding
		"python.result.imports": [],       # Modules to import in Python
		"python.result.exception": False,  # Display exception as stderr
	}

	def extract_params(self, lang, mode, paramstr):
		"""Set the parameter from the markdown parameter string"""
		params = self.default_parameters.copy()
		if paramstr is not None:
			for param in paramstr.split(";"):
				if "=" in param:
					key, expression = [item.strip() for item in param.split("=")]
					value = eval(expression, self.ext.config.globals, self.ext.locals)
				else:
					key = param.strip()
					value = True

				if lang is not None:
					if mode is not None:
						lmkey = f"{lang}.{mode}.{key}"
						if lmkey in params:
							params[lmkey] = value
							continue
					lkey = f"{lang}.{key}"
					if lkey in params:
						params[lkey] = value
						continue
				if mode is not None:
					mkey = f".{mode}.{key}"
					if mkey in params:
						params[mkey] = value
						continue
				if key in params:
					params[key] = value
					continue
				raise NameError(f"Unrecognized parameter {key} in code bloc {lang}/{mode}")
		return params

	def run_keep(self, code, lang, mode, params):
		filename = params[".keep.name"]
		keepfor = params[".keep.next"]
		with open(os.path.join("temp", filename), "w", encoding="utf-8") as keepfile:
			keepfile.write(code)
		self.ext.keptfiles[filename] = keepfor

	def run_result(self, code, lang, mode, params):
		if lang == "c":
			return self.run_result_c(code, lang, mode, params)
		elif lang in ("py", "python"):
			return self.run_result_python(code, lang, mode, params)
		else:
			raise NotImplementedError(f"Code block result mode unavailable for language {lang}")

	def run_result_c(self, code, lang, mode, params):
		"""Compute a result in C"""
		options = params["c.result.options"]
		if params["c.result.wrapmain"]:
			code = "int main() {\n" + code + "\nreturn 0;}"

		if params["c.result.includes"] == True:
			code = "#include <stdlib.h>\n#include <stdio.h>\n" + code
		elif len(params["c.result.includes"]) > 0:
			for include in params["c.result.includes"]:
				code = f"#include <{include}>\n" + code
			if "math.h" in params["c.result.includes"]:
				options.append("-lm")

		if self.ext.config.quick:  # Use cached results
			stdout, stderr = self.cached_results()
			if stdout is None or stderr is None:
				return ""
		else:  # Run everything in a temporary directory
			if not os.path.exists("temp"):
				os.mkdir("temp")

			os.chdir("temp")

			codefile = "_plsres_code_result.c"
			execfile = "_plsres_code_result" + (".exe" if platform.system() == "Windows" else "")
			with open(codefile, "w", encoding="utf-8") as f:
				f.write(code)

			# Compilation
			command = ["gcc", "-o", execfile, codefile] + options
			compilation = subprocess.run(command, capture_output=True)
			if compilation.returncode != 0:
				print(f"In document {self.ext.path}, code block\n{code}\nCompilation failed :\n{compilation.stderr.decode('utf-8')}")

			# Write the joined files
			if len(params[".result.joinfiles"]) > 0:
				for name, content in params[".result.joinfiles"]:
					with open(name, "w", encoding="utf-8") as f:
						f.write(content)

			# Run the program
			command = ["." + os.path.sep + execfile] + params[".result.argv"]
			if params["c.result.locale"]:
				encoding = locale.getdefaultlocale()[1]
			else:
				encoding="utf-8"
			result = subprocess.run(command, capture_output=True, input=params[".result.stdin"], encoding=encoding, text=True)
			stdout = result.stdout.replace("\r\n", "\n").strip("\n").rstrip()
			stderr = result.stderr.replace("\r\n", "\n").strip("\n").rstrip()

			os.remove(codefile)
			os.remove(execfile)
			if len(params[".result.joinfiles"]) > 0:
				for name, content in params[".result.joinfiles"]:
					os.remove(name)

			os.chdir("..")
			return self.build_result_html(params[".result.argv"], params[".result.stdin"], stdout, stderr, params[".result.joinfiles"])

	def run_result_python(self, code, lang, mode, params):
		for module in params["python.result.imports"]:
			code = f"import {module}\n" + code

		os.chdir("temp")
		# Write the joined files
		if len(params[".result.joinfiles"]) > 0:
			for name, content in params[".result.joinfiles"]:
				with open(name, "w", encoding="utf-8") as f:
					f.write(content)

		globals = builtins.__dict__ | self.python_builtins_patch()

		sys.argv = ["script.py"] + params[".result.argv"]
		sys.stdin = io.StringIO(params[".result.stdin"])
		sys.stdout = io.StringIO()
		sys.stderr = io.StringIO()

		codeexception = None
		try:
			exec(compile(code, "!!!!", "exec", optimize=0), globals)
		except Exception as exc:
			if params["python.result.exception"]:
				print(f"Traceback (most recent call last)", file=sys.stderr)
				tb = exc.__traceback__
				while tb is not None and tb.tb_frame.f_code.co_filename != "!!!!":
					tb = tb.tb_next
				while tb is not None:
					print(f"  File \"plsres_result.py\", line {tb.tb_lineno}, in {tb.tb_frame.f_code.co_name}", file=sys.stderr)
					print(f"    {code.splitlines()[tb.tb_lineno - 1].strip()}", file=sys.stderr)
					tb = tb.tb_next
				print(f"{exc.__class__.__name__}: {exc}", file=sys.stderr)
			else:
				codeexception = exc

		stdout = sys.stdout.getvalue()
		stderr = sys.stderr.getvalue()
		sys.stdout.close()
		sys.stderr.close()
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__

		if codeexception is not None:
			print(f"In document {self.ext.path}, code block\n{code}\n")
			raise codeexception

		if len(params[".result.joinfiles"]) > 0:
			for name, content in params[".result.joinfiles"]:
				os.remove(name)
		os.chdir("..")

		return self.build_result_html(params[".result.argv"], params[".result.stdin"], stdout, stderr, params[".result.joinfiles"])

	def python_builtins_patch(self):
		def input_patch(prompt):
			result = input(prompt)
			print(result)
			return result

		def debug(value):
			sys.__stdout__.write(f"DEBUG : {str(value)}\n")

		return {"input": input_patch, "debug": debug, "__name__": "__main__"}

	def build_result_html(self, argv, stdin, stdout, stderr, joinfiles):
		# Build the HTML result pane
		resultdiv_id = self.ext.uniqueid()
		htmlresult = f"""<button class="code-result-toggle btn btn-toggle collapsed" data-bs-toggle="collapse" data-bs-target="#{resultdiv_id}" aria-expanded="false">Résultat</button><div id="{resultdiv_id}" class="code-result collapse">"""

		if len(joinfiles) > 0:
			for name, content in joinfiles:
				htmlresult += f"""Fichier <code>{name}</code> : <pre class="code-result-joinfile">{content}</pre>"""
		if len(argv) > 0:
			htmlresult += f"""<pre class="code-result-args">./program {' '.join(argv)}</pre>"""
		if len(stdin) > 0:
			htmlresult += f"""Entrée : <pre class="code-result-stdin">{stdin}</pre>"""
		if len(stdout) > 0:
			htmlresult += f"""Sortie : <pre class="code-result-stdout">{stdout}</pre>"""
		if len(stderr) > 0:
			htmlresult += f"""Erreur : <pre class="code-result-stderr">{stderr}</pre>"""
		htmlresult += "</div>"
		return htmlresult

	def cached_results(self):
		"""Get the last cached results for this code block"""
		identifier = f"code-{self.ext.currentcode}"
		if identifier in self.ext.config.cache:
			cache = self.ext.doc_cache()[identifier]
			return cache["stdout"], cache["stderr"]
		else:
			return None, None

	def cache_results(self, stdout, stderr):
		"""Save the results of this code block"""
		identifier = f"code-{self.ext.currentcode}"
		self.ext.doc_cache()[identifier] = {"stdout": stdout, "stderr": stderr}


class MathBlockProcessor (BlockProcessor):
	"""Process math blocks
		$$\latex$$
	"""
	def __init__(self, md, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.md = md
		self.ext = extension

	def test(self, parent, block):
		match = EXT_MATH_BLOCK_REGEX.match(block)
		if match is None:
			return False
		return match.group(1) is not None

	def run(self, parent, blocks):
		if (match := EXT_MATH_BLOCK_REGEX.match(blocks[0])) is not None:
			if "$$" in match.group(1):
				return False
			latex = f"\\[{match.group(1)}\\]"
			#if latex in self.ext.config.cache.math:
			#	svg = self.ext.config.cache.math[latex]
			#else:
			#	svg = latex2svg(latex)["svg"]
			#	self.ext.config.cache.math[latex] = svg
			placeholder = self.md.htmlStash.store(latex)
			latexcontainer = etree.SubElement(parent, "div")
			latexcontainer.text = placeholder
			blocks.pop(0)
			return True
		else:
			return False

class FenceProcessor (BlockProcessor):
	"""Process fences
	   Fence with different types :
	       ;;; code
		   content
		   ;;; doc
		   content
		   ;;;
	"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def test(self, parent, block):
		match = EXT_FENCE_REGEX.match(block)
		if match is None:
			return False
		return match.group("type") is not None

	def run(self, parent, blocks):
		match = EXT_FENCE_REGEX.match(blocks[0])
		original_block = blocks[0]
		blocks[0] = blocks[0][match.end(0):]

		table = etree.SubElement(parent, "table")
		table.set("class", "fence")

		currentblocks = []
		currenttype = match.group("type")
		for index, block in enumerate(blocks):
			while (match := EXT_FENCE_REGEX.search(block)) is not None:
				matchtype = match.group("type")
				if matchtype is not None:
					currentblocks.append(block[:match.start(0)])
					block = block[match.end(0):]
					self.addcell(table, currentblocks, currenttype)
					currentblocks = []
					currenttype = matchtype
				else:
					currentblocks.append(block[:match.start(0)])
					self.addcell(table, currentblocks, currenttype)
					blocks[index] = block[match.end(0):]
					for i in range(0, index + (1 if blocks[index].strip() == "" else 0)):
						blocks.pop(0)
					return True
			currentblocks.append(block)
		blocks[0] = original_block
		return False

	def addcell(self, table, currentblocks, currenttype):
		"""Add and fill a new fence cell"""
		row = etree.SubElement(table, "tr")
		row.set("class", "fence-row")
		cell = etree.SubElement(row, "td")
		cell.set("class", f"fence-cell fence-{currenttype}")

		parameters = FENCE_PARAMETERS[currenttype]
		subblocks = []
		for block in currentblocks:
			block = block.strip()
			if block == "":
				continue
			if parameters["rawlines"]:
				processed = ""
				for line in block.splitlines():
					if not line.strip().startswith(("-", "+")) and line.strip() != "":
						line += "\\"
					processed += line + "\n"
				block = processed
			subblocks.append(block)
		self.parser.parseBlocks(cell, subblocks)

class FileCollectionProcessor (BlockProcessor):
	"""Process file collections
	       {!collection: collection name}"""

	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def test(self, parent, block):
		match = EXT_COLLECTION_REGEX.match(block.strip())
		return match is not None

	def run(self, parent, blocks):
		match = EXT_COLLECTION_REGEX.match(blocks[0].strip())
		collecname = match.group("name")

		collecpath = os.path.join(self.ext.parameters.resources, self.ext.parameters.collections, collecname)
		if not os.path.exists(collecpath):
			print(f"ERROR : Collection {collecname} ({collecpath}) does not exist")
			return False

		attributes = self.load_attributes(collecpath)
		filetree = self.load_filetree(collecpath)
		result = self.build_html(parent, attributes, collecpath, filetree)

		blocks.pop(0)
		return True

	def load_attributes(self, path):
		attrs = Attributes(title=None, fileTypes="*")
		with open(os.path.join(path, "attributes.yml"), "r", encoding="utf-8") as attrfile:
			attrs.update(yaml.load(attrfile.read(), yaml.Loader))
		return attrs

	def load_filetree(self, path):
		licensingpath = os.path.join(path, "licensing.yml")
		if os.path.exists(licensingpath):
			with open(licensingpath, "r", encoding="utf-8") as licensingfile:
				licensinglist = yaml.load(licensingfile.read(), yaml.Loader)
			licensing = {item["name"]: item for item in licensinglist["files"]}
		else:
			licensing = {}

		tree = {}
		for item in os.listdir(path):
			itempath = os.path.join(path, item)
			if os.path.isdir(itempath):
				subtree = self.load_filetree(itempath)
				tree[item] = {"type": "dir", "content": subtree}
			else:
				tree[item] = {"type": "file"}
				if item in licensing:
					tree[item].update(licensing[item])
		return tree

	def build_html(self, parent, attributes, collecpath, filetree):
		container = etree.SubElement(parent, "div")
		container.set("class", "collection")

		title = etree.SubElement(container, "p")
		title.set("class", "collection-title")
		title.text = attributes["title"]

		self.build_htmltree(container, attributes, "/" + collecpath.replace(os.path.sep, "/"), filetree)

	def build_htmltree(self, parent, attributes, treepath, filetree):
		list = etree.SubElement(parent, "ul")
		for name, info in filetree.items():
			if name not in ("attributes.yml", "licensing.yml"):
				item = etree.SubElement(list, "li")
				itemcontent = etree.SubElement(item, "p")
				itempath = f"{treepath}/{name}"
				if info["type"] == "dir":
					itemtext = name
					self.build_htmltree(item, attributes, itempath, info["content"])
				elif info["type"] == "file":
					itemtext = f'<a class="internal-link" href="{self.ext.parameters.staticprefix}{itempath}" alt="File download">{name}</a>'
					if "author" in info:
						itemtext += f"<br />Auteur : {info['author']}"
					if "license" in info:
						if info["license"] in self.ext.config.licenses:
							license = self.ext.config.licenses[info["license"]]
							itemtext += f'<br />Licence : <a href="{license["link"]}">{license["name"]}</a>'
						else:
							itemtext += f"<br />Licence : {info['license']}"
				itemcontent.text = itemtext

class ExerciseProcessor (BlockProcessor):
	"""Render exercises
		{!exercise: exercise-name}"""

	def __init__(self, md, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.md = md
		self.ext = extension

	def test(self, parent, block):
		match = EXT_EXERCISE_REGEX.match(block.strip())
		return match is not None

	def run(self, parent, blocks):
		match = EXT_EXERCISE_REGEX.match(blocks[0].strip())
		exercisename = match.group("name")
		try:
			exercise = self.ext.document.global_exercises[exercisename]
		except KeyError:
			print(f"In {self.ext.path}, exercise {exercisename} not found")
			return False
		htmltree = self.render_exercise(parent, exercise)

		blocks.pop(0)
		return True

	def render_exercise(self, parent, exercise):
		container_id = self.ext.uniqueid()

		extend_button = etree.SubElement(parent, "button")
		extend_button.set("class", "exercise-button exercise-toggle btn btn-toggle collapsed")
		extend_button.set("data-bs-toggle", "collapse")
		extend_button.set("data-bs-target", "#" + container_id)
		extend_button.set("aria-expanded", "false")
		extend_button.text = "> Exercice : " + exercise.title

		container = etree.SubElement(parent, "div")
		container.set("class", "exercise-container collapse")
		container.set("id", container_id)

		for i, question in enumerate(exercise.questions):
			self.render_question(container, question, i)

	def render_question(self, parent, question, index):
		container = etree.SubElement(parent, "div")
		container.set("class", "exercise-question-container")

		title = etree.SubElement(container, "p")
		title.set("class", "exercise-question-title")
		title.text = f"Question {index+1} [{'★' * question.difficulty}]"

		text_container = etree.SubElement(container, "div")
		text_container.set("class", "exercise-question-text-container")

		text = etree.SubElement(text_container, "div")
		text.set("class", "exercise-question-text")
		text.text = self.render_text(question.text)

		answer_class = self.ext.uniqueid()
		if question.type == "choices":
			for choice in question.choices:
				choice_container = etree.SubElement(text_container, "div")
				choice_container.set("class", "exercise-question-choice-container")

				choice_text = etree.SubElement(choice_container, "div")
				choice_text.set("class", "exercise-question-choice-text")
				choice_text.text = self.render_text(choice.text)

				choice_answer = etree.SubElement(choice_container, "div")
				choice_answer.set("class", "exercise-question-choice-answer " + answer_class)
				choice_answer.set("style", "display:none;")
				choice_answer.text = self.render_text(choice.answer)

		for hint in question.hints:
			hint_div_id = self.ext.uniqueid()
			extend_button = etree.SubElement(text_container, "button")
			extend_button.set("class", f"exercise-button exercise-question-hint-{hint.level} exercise-question-hint-toggle btn btn-toggle collapsed")
			extend_button.set("data-bs-toggle", "collapse")
			extend_button.set("data-bs-target", "#" + hint_div_id)
			extend_button.set("aria-expanded", "false")
			extend_button.text = f"> Indice [{hint.level}] : {self.ext.config.exerciseconfig.hintLevelDescription[hint.level]}"

			hint_container = etree.SubElement(text_container, "div")
			hint_container.set("class", "exercise-question-hint collapse")
			hint_container.set("id", hint_div_id)

			hint_text = etree.SubElement(hint_container, "div")
			hint_text.set("class", "exercise-wrapped-text")
			hint_text.text = self.render_text(hint.text)

		reveal_button = etree.SubElement(text_container, "button")
		reveal_button.set("class", "exercise-button answer-reveal-button btn btn-toggle")
		reveal_button.set("aria-expanded", "false")
		reveal_button.text = "> Révéler la solution"
		reveal_button.set("onclick", f"revealAnswers(this, \"{answer_class}\");")

		if question.answer is not None:
			answer_text = etree.SubElement(text_container, "div")
			answer_text.set("class", "exercise-question-answer " + answer_class)
			answer_text.set("style", "display:none;")
			answer_text.text = self.render_text(question.answer)


	def render_text(self, text):
		self.ext.ispage = False
		md = markdown.Markdown(extensions=["tables", self.ext])
		html = md.convert(text)
		self.ext.ispage = True
		placeholder = self.md.htmlStash.store(html)
		return placeholder


class ExpressionProcessor (InlineProcessor):
	"""Process inline expression templates
	       {=python expression}"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_EXPR_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		escape = match.group(1) is None
		expression = match.group(2)
		format = match.group(4)
		result = eval(expression, self.ext.config.globals | math.__dict__, self.ext.locals)
		if format is None:
			string = str(result)
		else:
			string = ("{:" + format + "}").format(result)
		if escape:
			string = html.escape(string)
		return (string, match.start(0), match.end(0))

class InternalLinkProcessor (InlineProcessor):
	"""Process site internal link templates
	       {> book.section.page#anchor: text to display}"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_LINK_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		docpath = match.group(1)
		if "#" in docpath:
			docpath, anchor = docpath.split("#")
		else:
			anchor = None

		content = match.group(3)
		element = etree.Element("a")
		if docpath in self.ext.config.linktable:
			href = self.ext.config.linktable[docpath]
			alt = self.ext.config.pathtable[docpath].attributes.title
			if content is None:
				content = alt
			element.set("class", "internal-link")
		else:
			href = (self.ext.parameters.linkprefix + docpath.replace(".", "/") + ".html").replace("//", "/")
			alt = "La page n’existe pas (encore ?)"
			if content is None:
				content = docpath
			element.set("class", "dead-link")
			print(f"WARNING : Dead internal link to {docpath} in {self.ext.path}")

		if anchor is not None:
			href += "#" + anchor

		element.set("href", href)
		element.set("alt", alt)
		element.text = content
		return (element, match.start(0), match.end())

class EscapeProcessor (InlineProcessor):
	"""Process custom escape sequences
	       Inline newline : `\ `
		   Greater and lower symbols : `\>`, `\<`
	"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_ESCAPE_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		escaped = match.group(1)
		if escaped.isspace():
			return (etree.Element("br"), match.start(0), match.end(0))
		elif escaped == "<":
			return ("&lt;", match.start(0), match.end(0))
		elif escaped == ">":
			return ("&gt;", match.start(0), match.end(0))

class DeleteProcessor (InlineProcessor):
	"""Process deleted (strikethrough) text
		~~Deleted text~~
	"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_DELETE_PATTERN, *args, *kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		deleted = match.group(1)
		element = etree.Element("del")
		element.text = deleted
		return (element, match.start(0), match.end())

class UnderlineProcessor (InlineProcessor):
	"""Process undelined text
		__Undelined text__
	"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_UNDERLINE_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		deleted = match.group(1)
		element = etree.Element("u")
		element.text = deleted
		return (element, match.start(0), match.end())

class InlineMathProcessor (InlineProcessor):
	"""Process inline math
		$$\latex$$
	"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_MATH_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		content = match.group(1)
		latex = f"\\({content}\\)"
		#if latex in self.ext.config.cache.math:
		#	svg = self.ext.config.cache.math[latex]
		#else:
		#	svg = latex2svg(latex)["svg"]
		#	self.ext.config.cache.math[latex] = svg
		placeholder = self.md.htmlStash.store(latex)
		return (placeholder, match.start(0), match.end())

class InternalSVGProcessor (InlineProcessor):
	"""Process SVG embeds, embeds the SVG code from a given file at res/img/path directly into the page
	       {!svg: my/svg/file.svg}"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_SVG_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		name = match.group("name")
		alt = match.group("alt")
		filename = os.path.join(self.ext.parameters.resources, self.ext.parameters.img, name)
		if os.path.exists(filename):
			try:
				with open(filename, "r", encoding="utf-8") as svgfile:
					svg = svgfile.read()

				try:  # Try to eliminate the superfluous XML header
					xmlstart = svg.index("<?")
					xmlend = svg.index("?>")
					svg = svg[xmlend + 2:]
				except ValueError:
					pass

				placeholder = self.md.htmlStash.store(svg.strip())
				#if alt is not None:
				#	element.set("alt", alt)
				return (placeholder, match.start(0), match.end(0))
			except UnicodeDecodeError:
				print(f"WARNING : In document {self.ext.path}, tried to load a non-SVG image with !svg : {match.group(0)}. Defaulting to !img behaviour")
				return InternalImageProcessor.handleMatch(self, match, data)
		else:
			print(f"In {self.ext.path}, file {filename} not found")
			if alt is not None:
				return (alt, match.start(0), match.end(0))
			return None, None, None

class InternalImageProcessor (InlineProcessor):
	"""Includes an image at res/img/path
	       {!img: my/image/file.png}"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(EXT_IMG_PATTERN, *args, **kwargs)
		self.ext = extension

	def handleMatch(self, match, data):
		name = match.group("name")
		alt = match.group("alt")
		filename = os.path.join(self.ext.parameters.resources, self.ext.parameters.img, name)
		if os.path.exists(filename):
			element = etree.Element("img")
			element.set("src", f"{self.ext.parameters.staticprefix}/{self.ext.parameters.resources}/{self.ext.parameters.img}/{name}".replace("//", "/"))
			if alt is not None:
				element.set("alt", alt)
			return (element, match.start(0), match.end(0))
		else:
			print(f"In {self.ext.path}, file {filename} not found")
			return None, None, None


class ContentTreeProcessor (Treeprocessor):
	"""Process the titles to build the contents tree and the navbar"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def iterparent(self, root):
		doublebuf = None
		for parent in root.iter():
			for i, child in enumerate(parent):
				if child is not doublebuf:
					yield i, parent, child
					doublebuf = child

	def run(self, root):
		tree = {None: (None, {})}
		stack = [tree]
		lasttitle = None
		currentlevel = 0
		titlesfound = 0
		for index, parent, element in self.iterparent(root):
			if element.tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
				level = int(element.tag[1])

				if level > currentlevel + 1:
					raise ValueError(f"At element {element}, heading level too low ({currentlevel} -> {level})")
				elif level > currentlevel:
					stack.append(stack[-1][lasttitle][1])
				elif level < currentlevel:
					for i in range(currentlevel - level):
						stack.pop()

				title, anchor = self.gettitle(element)
				if anchor is None:
					if titlesfound == 0 and element.tag == "h1":
						anchor = ""
					else:
						anchor = "section"
						for stackitem in stack[2:]:
							anchor += str(len(stackitem) + 1)
				anchor = anchor.strip()
				self.settitle(element, title, anchor)
				title = self.process_title(title)

				stack[-1][title] = (anchor, {})
				currentlevel = level
				lasttitle = title

				if element.tag == "h1":
					if titlesfound > 0:
						print(f"Multiple main titles (h1) found in {self.ext.path}. This may cause errors in anchor attributions. Consider splitting the page or using subordinate titles")
						print(f"Title text : {element.text}")
					else:
						parent.insert(index, self.build_linkdiv())
					titlesfound += 1
		root.append(self.build_linkdiv())
		self.ext.contenttree = tree[None][1]

	def gettitle(self, element):
		text = ""
		for textnode in element.itertext():
			text += textnode
		items = text.split(EXT_CONTENT_ANCHOR_SEP)
		return items[0], items[1] if len(items) > 1 else None

	def settitle(self, element, title, anchor):
		element.text = title
		element.set("id", anchor)

	def process_title(self, title):
		# For the moment, just remove all placeholders
		# NOTE : will it ever be useful to have inline HTML in contents items ?
		while markdown.util.STX in title:
			start = title.index(markdown.util.STX)
			end = title.index(markdown.util.ETX)
			title = title[:start] + title[end+1:].replace("  ", " ")
		return html.unescape(title)

	def build_linkdiv(self):
		linkdiv = etree.Element("div")
		linkdiv.set("class", "page-links")
		if self.ext.document.previous is not None and not self.ext.document.previous.attributes.hidden:
			prevlink = etree.SubElement(linkdiv, "a")
			prevlink.set("class", "internal-link link-previous")
			prevlink.set("href", self.ext.config.linktable[self.ext.document.previous.docpath])
			prevlink.text = f"<< {self.ext.document.previous.attributes.title}"
		if self.ext.document.category is not None and not self.ext.document.category.attributes.hidden:
			catlink = etree.SubElement(linkdiv, "a")
			catlink.set("class", "internal-link link-category")
			catlink.set("href", self.ext.config.linktable[self.ext.document.category.docpath])
			catlink.text = f"↑ {self.ext.document.category.attributes.title}"
		if self.ext.document.next is not None and not self.ext.document.next.attributes.hidden:
			nextlink = etree.SubElement(linkdiv, "a")
			nextlink.set("class", "internal-link link-next")
			nextlink.set("href", self.ext.config.linktable[self.ext.document.next.docpath])
			nextlink.text = f"{self.ext.document.next.attributes.title} >>"
		return linkdiv

class StyleProcessor (Treeprocessor):
	"""Add some style classes to various extension elements"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def run(self, root):
		for element in root.iter():
			if element.tag == "table":
				elclass = element.get("class")
				if elclass is None:
					element.set("class", "info-table")
				elif "fence" not in elclass:
					element.set("class", (elclass + " info-table").strip())
			elif element.tag == "a":
				if element.get("class") is None:
					element.set("class", "external-link")


class TemplatePostprocessor (Postprocessor):
	"""Put the document into the website HTML page template and fill in some of the templated values"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def run(self, htmlpage):
		page = self.ext.config.template
		for varname, value in self.ext.locals.items():
			page = page.replace(f"{{={varname}}}", str(value))
		for varname, value in self.ext.config.globals.items():
			page = page.replace(f"{{={varname}}}", str(value))
		page = page.replace("{=__title}", html.escape(self.ext.document.attributes.title) if self.ext.document.attributes.title is not None else "")
		page = page.replace("{=__subtitle}", html.escape(self.ext.document.attributes.subtitle) if self.ext.document.attributes.subtitle is not None else "")
		page = page.replace("{=__description}", html.escape(self.ext.document.attributes.description) if self.ext.document.attributes.description is not None else "")
		page = page.replace("{=__theme_color}", self.theme_color())
		page = page.replace("{=__content}", htmlpage)
		page = page.replace("{=__pagenav}", self.build_pagenav())

		parents = set()
		currentdoc = self.ext.document.docpath
		while currentdoc != "":
			parents.add(currentdoc)
			currentdoc = self.ext.config.parenttable[currentdoc]

		for docpath in self.ext.config.pathtable:
			if docpath in parents:
				page = page.replace(f"{{=collapsed-{docpath}}}", "").replace(f"{{=expanded-{docpath}}}", "true").replace(f"{{=show-{docpath}}}", " show")
			else:
				page = page.replace(f"{{=collapsed-{docpath}}}", " collapsed").replace(f"{{=expanded-{docpath}}}", "false").replace(f"{{=show-{docpath}}}", "")
		return page

	def theme_color(self):
		color = None
		document = self.ext.document
		while color is None and document is not None:
			if document.attributes.themeColor is not None:
				color = document.attributes.themeColor
			else:
				document = self.ext.config.pathtable[self.ext.config.parenttable[document.docpath]]
		return f"#{color[0] :2X}{color[1] :2X}{color[2] :2X}"

	def build_pagenav(self):
		return self.build_subnav(self.ext.contenttree)

	def build_subnav(self, tree, level=0):
		"""Recursively build the page navigation bar from the content tree"""
		navigation = f"""<ul class="list-unstyled nav-ul innav-ul innav-ul-{level}">"""
		for title, (anchor, subtree) in tree.items():
			navigation += f"""<li class="nav-li innav-li innav-li-{level}">"""
			navigation += f"""<a class="anchor-link" href="#{anchor}">{html.escape(title)}</a>"""
			if len(subtree) > 0:
				navigation += self.build_subnav(subtree, level+1)
			navigation += "</li>"
		navigation += "</ul>"
		return navigation

class JSONPostProcessor (Postprocessor):
	"""Output the document in the optimized JSON response format"""
	def __init__(self, extension, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ext = extension

	def run(self, htmlpage):
		pagenav = self.build_subnav(self.ext.contenttree)
		content = {
			"docpath": self.ext.document.docpath,
			"title": self.ext.document.attributes.title if self.ext.document.attributes.title is not None else "",
			"subtitle": self.ext.document.attributes.subtitle if self.ext.document.attributes.subtitle is not None else "",
			"description": self.ext.document.attributes.description if self.ext.document.attributes.description is not None else "",
			"themeColor": self.themeColor(),
			"pageNavigation": pagenav,
			"content": htmlpage,
			#"category": self.ext.config.linktable[self.ext.document.category.docpath] if self.ext.document.category is not None else None,
			#"previous": self.ext.config.linktable[self.ext.document.previous.docpath] if self.ext.document.previous is not None else None,
			#"next": self.ext.config.linktable[self.ext.document.next.docpath] if self.ext.document.next is not None else None,
		}
		return json.dumps(content)

	def build_subnav(self, tree, level=0):
		navigation = []
		for title, (anchor, subtree) in tree.items():
			navigation.append({
				"title": html.escape(title),
				"anchor": "#" + anchor,
				"level": level,
				"subtree": self.build_subnav(subtree, level+1) if len(subtree) > 0 else None,
			});
		return navigation


	def themeColor(self):
		color = None
		document = self.ext.document
		while color is None and document is not None:
			if document.attributes.themeColor is not None:
				color = document.attributes.themeColor
			else:
				document = self.ext.config.pathtable[self.ext.config.parenttable[document.docpath]]
		return f"#{color[0] :2X}{color[1] :2X}{color[2] :2X}"
