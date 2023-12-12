import os
import html
import yaml
import json
import shutil
import markdown
from .util import Attributes
from .document import CompoundDocument
from .extension import PLSResExtension, FENCE_PARAMETERS
from .exercises import parse_exercise


class Site (CompoundDocument):
	"""Root document, that encompasses the whole site"""
	def __init__(self, parameters, quick=False, full=False):
		self.parameters = parameters
		self.sourcepath = parameters.source
		self.quick = quick
		self.full = full
		self.doctype = None
		self.docpath = ""
		self.name = "__main"
		self.category = None
		self.previous = None
		self.next = None
		self.exercises = {}
		self.global_exercises = {}

	def load(self):
		self.load_attributes()
		self.load_cache()
		self.load_documents()

	def load_attributes(self):
		attrpath = os.path.join(self.parameters.source, "attributes.yml")
		with open(attrpath, "r", encoding="utf-8") as attrfile:
			self.attributes = Attributes(yaml.load(attrfile.read(), yaml.Loader))
		self.extract_variables()

	def load_cache(self):
		if os.path.exists(self.parameters.cache) and not self.full:
			with open(self.parameters.cache, "r", encoding="utf-8") as cachefile:
				self.cache = Attributes(json.load(cachefile))
		else:
			self.cache = Attributes(documents={}, parenttable={}, math={})

	def load_exercise_config(self):
		attrpath = os.path.join(self.parameters.template, "exercises.yml")
		with open(attrpath, "r", encoding="utf-8") as attrfile:
			attributes = Attributes(yaml.load(attrfile.read(), yaml.Loader))
		return attributes

	def load_documents(self):
		"""Load all documents in the site"""
		self.documents = []
		for docname in self.attributes.documents:
			self.documents.append(self.load_document(self.parameters.source, docname))
		self.load_exercise_base()
		self.link_documents()
		self.pathtable = {}
		self.documenttree = self.build_documenttree(self.pathtable)
		self.linktable = {docpath: self.parameters.linkprefix + docpath.replace(".", "/") + self.parameters.pagesuffix for docpath in self.pathtable}
		self.parenttable = self.build_parenttable()
	
	def load_exercise_base(self):
		for path, dirs, files in os.walk(self.parameters.exercises):
			for filename in files:
				if filename.endswith(".xmd"):
					with open(os.path.join(path, filename), "r") as exercisefile:
						exercise = parse_exercise(exercisefile)
						exercise.name = path.replace(os.path.sep, ".").replace("/", ".") + "." + exercise.name
						self.global_exercises[exercise.name] = exercise
		self.exercises = self.global_exercises

		"""if len(self.exercises) > 0:
			exercise_directory = os.path.join("temp", "exercises")
			if not os.path.exists(exercise_directory):
				os.mkdir(exercise_directory)
			sourcepath = os.path.join(exercise_directory, "exdb.exercises.md")
			self.generate_exercises(sourcepath)
			self.documents.append(self.load_document("", "exercises", sourcepath))"""

	def render(self):
		"""Render the whole site"""
		self.pagetemplate = self.build_template()

		# Prepare the output directory and transfer the resources
		if not os.path.exists(self.parameters.output):
			os.mkdir(self.parameters.output)
		#else:
		#	for item in os.listdir(outpath):
		#		shutil.rmtree(os.path.join(outpath, item))
		shutil.copytree(self.parameters.resources, os.path.join(self.parameters.output, self.parameters.resources), dirs_exist_ok=True)

		# Extension configuration
		extconfig = Attributes(
			pathtable = self.pathtable,
			documenttree = self.documenttree,
			linktable = self.linktable,
			parenttable = self.parenttable,
			template = self.pagetemplate,
			licenses = self.load_licenses(),
			globals = {},
			cache = self.cache,
			quick = self.quick,
			updateall = (self.cache.parenttable != self.parenttable),
			exerciseconfig = self.load_exercise_config(),
		)

		super().render(self.parameters.output, extconfig, self.parameters)

		#for document in self.documents:
		#	if document.doctype == "page":
		#		subpath = os.path.join(self.parameters.output, document.name + "." + self.parameters.outformat)
		#	else:
		#		subpath = os.path.join(self.parameters.output, document.name)
		#	document.render(subpath, extconfig, self.parameters)

		self.generate_styles()
		self.generate_exdb(extconfig)
		self.save_cache()

	def build_linktable(self, parent=None):
		"""Build the table docpath -> internal link href"""
		linktable = {}
		for name, document in self.documenttree:
			linktable[document.docpath] = "/" + document.docpath.replace(".", "/") + self.parameters.pagesuffix
		return linktable

	def build_parenttable(self):
		"""Build the table docpath -> parent document"""
		parenttable = {}
		self.extract_parents(parenttable, self.documenttree)
		return parenttable

	def extract_parents(self, parenttable, tree):
		"""Recursively build the parent table"""
		for docname, subtree in tree.items():
			if docname == "_": continue
			parenttable[subtree["_"].docpath] = tree["_"].docpath
			if len(subtree) > 1:
				self.extract_parents(parenttable, subtree)

	def build_template(self):
		"""Build the website HTML template"""
		with open(os.path.join(self.parameters.template, "index.html"), "r", encoding="utf-8") as tempfile:
			template = tempfile.read()

		navigation = self.build_subnav(self.documenttree)
		template = template.replace("{=__sitenav}", navigation)
		template = template.replace("{=__linkprefix}", self.parameters.linkprefix)
		template = template.replace("{=__staticprefix}", self.parameters.staticprefix)

		with open(os.path.join(self.parameters.output, "_template.html"), "w", encoding="utf-8") as templatefile:
			templatefile.write(template)
		with open(os.path.join(self.parameters.output, "_sitenav.html"), "w", encoding="utf-8") as navfile:
			navfile.write(navigation)

		return template

	def build_subnav(self, tree, level=0):
		"""Recursively build the website global navbar"""
		navigation = f"""<ul class="list-unstyled ps-0 nav-ul exnav-ul exnav-ul-{level}">"""
		basedoc = tree["_"]
		for docname, subtree in tree.items():
			if docname == "_": continue
			if subtree['_'].attributes.hidden: continue
			navigation += f"""<li class="nav-li exnav-li exnav-li-{level}">"""
			if len(subtree) > 1:
				navigation += f"""<button class="btn btn-toggle rounded{{=collapsed-{subtree['_'].docpath}}}" data-bs-toggle="collapse" data-bs-target="#{basedoc.docpath.replace('.', '-')}-{docname}-toggle" aria-expanded="{{=expanded-{subtree['_'].docpath}}}">{html.escape(subtree['_'].title)}</button>"""
				navigation += f"""<div id="{basedoc.docpath.replace('.', '-')}-{docname}-toggle" class="collapse{{=show-{subtree['_'].docpath}}}">"""
				navigation += self.build_subnav(subtree, level+1)
				navigation += "</div>"
			else:
				navigation += f"""<a class="internal-link" href="{self.linktable[subtree['_'].docpath]}">{html.escape(subtree['_'].attributes.title)}</a>"""
			navigation += "</li>"
		navigation += "</ul>"
		return navigation

	def generate_styles(self):
		"""Generate some of the styles"""
		css_inputpath = os.path.join(self.parameters.resources, self.parameters.css)
		css_outputpath = os.path.join(self.parameters.output, self.parameters.resources, self.parameters.css)

		# Templated styles
		for filename in os.listdir(css_inputpath):
			with open(os.path.join(css_inputpath, filename), "r", encoding="utf-8") as basefile:
				css = basefile.read()
			css = css.replace("{=__staticprefix}", self.parameters.staticprefix)
			with open(os.path.join(css_outputpath, filename), "w", encoding="utf-8") as outfile:
				outfile.write(css)

		# Generated styles
		with open(os.path.join(css_outputpath, "genstyles.css"), "w", encoding="utf-8") as css:
			for fencetype, parameters in FENCE_PARAMETERS.items():
				r, g, b = parameters["color"]
				css.write(f"td.fence-{fencetype} {{border-left: solid 8px rgb({r},{g},{b}); border-right: solid 8px rgb({r},{g},{b});}}\n")

	def load_licenses(self):
		with open(os.path.join(self.parameters.template, "licenses.yml"), "r", encoding="utf-8") as licensefile:
			licenselist = yaml.load(licensefile.read(), yaml.Loader)

		licenses = {}
		for item in licenselist["licenses"]:
			for id in item["id"]:
				licenses[id] = item
		return licenses

	def generate_exdb(self, extconfig):
		extension = PLSResExtension(self.sourcepath, self, extconfig, self.parameters, ispage=False)
		extension.start()
		md = markdown.Markdown(extensions=["tables", extension])
		
		exdb = []
		exdb_renders = {}
		for name, exercise in self.global_exercises.items():
			exdb.append(exercise.serialize())
			exdb_renders[name] = md.convert("{!exercise: " + name + "}")
		
		with open(self.parameters["exdboutput"], "w") as f:
			json.dump(exdb, f)
		with open(self.parameters["exdbrender"], "w") as f:
			json.dump(exdb_renders, f)

	def save_cache(self):
		self.cache.parenttable = self.parenttable
		with open(self.parameters.cache, "w", encoding="utf-8") as cachefile:
			json.dump(self.cache, cachefile)
