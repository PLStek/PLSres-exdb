"""
Base classes for PL$res resources documents
"""


import os
import yaml
import markdown
from functools import lru_cache
from .util import Attributes
from .extension import PLSResExtension, MetaPreprocessor
from .exercises import parse_exercise


DOCTYPES = {"site", "book", "section", "page"}


class Document (object):
	"""Base class for all documents"""
	def __init__(self, sourcepath, docname, docpath, attributes=None, exercises={}, global_exercises={}):
		self.sourcepath = sourcepath
		self.name = docname
		self.docpath = docpath
		self.attributes = attributes
		
		self.exercises = {}
		for name, exercise in exercises.items():
			if exercise.courses is None:
				exercise.courses = self.attributes.relevantCourses
			fullname = self.docpath + "." + exercise.name
			exercise.name = fullname
			self.exercises[fullname] = exercise
		self.global_exercises = global_exercises
		self.global_exercises.update(self.exercises)
		
		self.category = None
		self.previous = None
		self.next = None
		self.extract_variables()
		self.load_documents()

	def extract_variables(self):
		"""Extract the values from attributes.yml"""
		if self.attributes is not None:
			self.attributes.title =           self.attributes["title"] if "title" in self.attributes else None
			self.attributes.subtitle =        self.attributes["subtitle"] if "subtitle" in self.attributes else None
			self.attributes.description =     self.attributes["description"] if "description" in self.attributes else None
			self.attributes.themeColor =      self.attributes["themeColor"] if "themeColor" in self.attributes else None
			self.attributes.hidden =          self.attributes["hidden"] if "hidden" in self.attributes else False
			self.attributes.relevantCourses = self.attributes["relevantCourses"] if "relevantCourses" in self.attributes else []
		else:
			self.attributes = Attributes(title=None, subtitle=None, description=None, themeColor=None, hidden=False, relevantCourses=[])

	def load_documents(self):
		"""Load the sub-sections of this document"""
		self.documents = []
		if not self.has_subdocuments(): return

		if self.attributes is None or "sections" not in self.attributes:
			filenames = sorted([filename for filename in os.listdir(self.sourcepath) if filename.endswith(".md")])
			for filename in filenames:
				if "--" in filename:
					docname = os.path.splitext(filename)[0].partition("--")[-1]
				else:
					docname = os.path.splitext(filename)[0]
				self.documents.append(self.load_document(self.sourcepath, docname, filename=filename))
		else:
			for docname in self.attributes["sections"]:
				document = self.load_document(self.sourcepath, docname)
				self.attributes.relevantCourses = list(set(self.attributes.relevantCourses + document.attributes.relevantCourses))
				self.documents.append(document)

		self.link_documents()

	def link_documents(self):
		for i, document in enumerate(self.documents):
			document.category = self
			if i > 0:
				document.previous = self.documents[i-1]
			if i < len(self.documents) - 1:
				document.next = self.documents[i+1]

	def load_document(self, sourcepath, docname, filename=None):
		"""Load the sub-document at the given path
		   - sourcepath : path to the current document’s folder
		   - docname    : codename of the document
		   - filename   : to give an explicit file name for a page instead of autodetect in a folder"""
		pagepath = os.path.join(sourcepath, docname + ".md" if filename is None else filename)  # If it is a page, this will be its exact path
		subdir = os.path.join(sourcepath, docname)  # Otherwise, this is the folder the document will be in
		attrpath = os.path.join(subdir, "attributes.yml")  # This is the possible position of the document’s attributes.yml
		exercisedir = os.path.join(subdir, "exercises")  # This is the possible position of the document's exercises
		docpath = (self.docpath + "." + docname).strip(".")  # Docpath of the sub-document to load

		if filename is None and os.path.exists(exercisedir):
			exercises = self.load_exercises(exercisedir)
		else:
			exercises = {}

		if filename is None and os.path.exists(attrpath):
			with open(attrpath, "r", encoding="utf-8") as attrfile:
				attributes = Attributes(yaml.load(attrfile.read(), yaml.Loader))
				if "documentType" in attributes:
					doctype = attributes["documentType"]
					if doctype == "book":
						return Book(subdir, docname, docpath, attributes, exercises, self.global_exercises)
					elif doctype == "section":
						return Section(subdir, docname, docpath, attributes, exercises, self.global_exercises)
					elif doctype == "page":
						if "sourceFile" in attributes:
							filename = attributes["sourceFile"]
						else:
							filename = [filename for filename in os.listdir(subdir) if filename.endswith(".md")][0]
						return Page(os.path.join(subdir, filename), docname, docpath, attributes, exercises, self.global_exercises)
					else:
						raise ValueError(f"Unrecognized documentType : {doctype}")
				elif self.doctype in ("book", "section"):
					return Section(subdir, docname, docpath, attributes, exercises, self.global_exercises)
				else:
					raise ValueError(f"Unknown document type for {docname}, loading from {self.name}")
		elif os.path.exists(pagepath):
			return Page(pagepath, docname, docpath, None, exercises, self.global_exercises)
		else:
			raise ValueError(f"No document found for name {docname}, loading from {self.name}")
	
	def load_exercises(self, exercisedir):
		exercises = {}
		for filename in os.listdir(exercisedir):
			try:
				with open(os.path.join(exercisedir, filename), "r") as exercisefile:
					exercise = parse_exercise(exercisefile)
					exercises[exercise.name] = exercise
			except Exception as exc:
				print(f"In exercise file {os.path.join(exercisedir, filename)} :")
				raise
		return exercises

	def build_documenttree(self, pathtable):
		"""Recursively build the site documents tree"""
		tree = {}
		for document in self.documents:
			tree[document.name] = document.build_documenttree(pathtable)

		tree["_"] = self
		pathtable[self.docpath] = self
		return tree


class CompoundDocument (Document):
	"""Base class for compound documents (as in not a single page : book, section)"""
	course_info = None

	def __init__(self, sourcepath, docname, docpath, attributes, exercises, global_exercises):
		super().__init__(sourcepath, docname, docpath, attributes, exercises, global_exercises)
		self.title = attributes["title"]

	def has_subdocuments(self):
		return True

	def load_documents(self):
		super().load_documents()

		if len(self.exercises) > 0:
			exercise_directory = os.path.join("temp", "exercises")
			if not os.path.exists(exercise_directory):
				os.mkdir(exercise_directory)
			sourcepath = os.path.join(exercise_directory, self.docpath + ".exercises.md")
			self.generate_exercises(sourcepath)
			self.documents.append(self.load_document("", "exercises", sourcepath))
		self.link_documents()

	def render(self, outpath, extconfig, parameters):
		"""For the moment, just render the sub-document"""
		if not os.path.exists(outpath):
			os.mkdir(outpath)

		self.generate_index(os.path.join(outpath, "index." + parameters.outformat), extconfig, parameters)

		for document in self.documents:
			if document.doctype == "page":
				subpath = os.path.join(outpath, document.name + "." + parameters.outformat)
			else:
				subpath = os.path.join(outpath, document.name)
			document.render(subpath, extconfig, parameters)

	def generate_index(self, outpath, extconfig, parameters):
		if extconfig.cache.parenttable == extconfig.parenttable and self.docpath in extconfig.cache.documents:
			doccache = extconfig.cache.documents[self.docpath]
			editdate = os.path.getmtime(self.sourcepath)
			if editdate <= doccache["lastcompiled"]:
				return

		doclist = ""
		for document in self.documents:
			if not document.attributes.hidden:
				course_list = " ".join(self.course_icon(course, parameters) for course in sorted(document.attributes.relevantCourses))
				doclist += f"""- <a class="index-link" href="{extconfig.linktable[document.docpath]}">{document.attributes.title} <span class="course-list">{course_list}</span></a>\n"""

		markdown_page = f"""//// title = "{self.attributes.title}"
//// subtitle = "{self.attributes.subtitle}"
//// description = "{self.attributes.description}"
//// themeColor = {self.attributes.themeColor}
# {{=title}}
*{{=subtitle}}*

{" ".join(self.course_icon(course, parameters) for course in sorted(self.attributes.relevantCourses))}

{doclist}"""

		print(f"Rendering document {self.docpath}")
		extension = PLSResExtension(self.sourcepath, self, extconfig, parameters)
		extension.start()
		md = markdown.Markdown(extensions=["tables", extension])
		html = md.convert(markdown_page)

		with open(outpath, "w", encoding="utf-8") as outfile:
			outfile.write(html)
		extension.finish()

	def generate_exercises(self, sourcepath):
		exerciselist = ""
		for exercise in self.exercises:
			exerciselist += f"{{!exercise: {exercise}}}\n\n"

		markdown_page = f"""//// title = "Exercices"
//// description = "{self.attributes.description}"
//// themeColor = {self.attributes.themeColor}
# {{=title}}

{exerciselist}"""

		with open(sourcepath, "w", encoding="utf-8") as sourcefile:
			sourcefile.write(markdown_page)

	@classmethod
	def course_icon(cls, course, parameters):
		if cls.course_info is None:
			with open(os.path.join(parameters.template, "courses.yml"), "r", encoding="utf-8") as infofile:
				cls.course_info = yaml.load(infofile.read(), yaml.Loader)["courses"]

		if course not in cls.course_info:
			print(f"WARNING : Unknown course {course}, define it in {parameters.template}/courses.yml to fix")
			bgcolor = "#000000"
			fgcolor = "#FFFFFF"
		else:
			bgcolor_rgb = cls.course_info[course]
			bgcolor = f"#{bgcolor_rgb[0] :02X}{bgcolor_rgb[1] :02X}{bgcolor_rgb[2] :02X}"
			gray = 0.2989 * bgcolor_rgb[0] + 0.5870 * bgcolor_rgb[1] + 0.1140 * bgcolor_rgb[2]
			fgcolor = "#000000" if gray > 127 else "#FFFFFF"

		courseitem = f'<span class="smaller">{course}</span>' if len(course) > 6 else course
		return f'<span class="course-icon" style="background-color:{bgcolor}; color:{fgcolor}">{courseitem}</span>'



class Book (CompoundDocument):
	"""Book document type"""
	def __init__(self, sourcepath, docname, docpath, attributes, exercises, global_exercises):
		self.doctype = "book"
		super().__init__(sourcepath, docname, docpath, attributes, exercises, global_exercises)

class Section (CompoundDocument):
	"""Section document type"""
	def __init__(self, sourcepath, docname, docpath, attributes, exercises, global_exercises):
		self.doctype = "section"
		super().__init__(sourcepath, docname, docpath, attributes, exercises, global_exercises)


class Page (Document):
	"""Web-page document type"""
	def __init__(self, sourcepath, docname, docpath, attributes=None, exercises={}, global_exercises={}):
		self.doctype = "page"
		self.category = None
		self.previous = None
		self.next = None
		super().__init__(sourcepath, docname, docpath, attributes, exercises, global_exercises)

	def has_subdocuments(self):
		return False

	def extract_variables(self):
		if self.attributes is not None:
			self.attributes.title =           self.attributes["title"] if "title" in self.attributes else None
			self.attributes.subtitle =        self.attributes["subtitle"] if "subtitle" in self.attributes else None
			self.attributes.description =     self.attributes["description"] if "description" in self.attributes else None
			self.attributes.themeColor =      self.attributes["themeColor"] if "themeColor" in self.attributes else None
			self.attributes.hidden =          self.attributes["hidden"] if "hidden" in self.attributes else False
			self.attributes.relevantCourses = self.attributes["relevantCourses"] if "relevantCourses" in self.attributes else []
		else:  # No individual attributes.yml, we need to extract those from the page’s content
			preprocessor = MetaPreprocessor(None)
			with open(self.sourcepath, "r", encoding="utf-8") as mdfile:
				preprocessor.run(mdfile.read().splitlines())
			self.attributes = Attributes(
				title = preprocessor.locals["title"] if "title" in preprocessor.locals else None,
				subtitle = preprocessor.locals["subtitle"] if "subtitle" in preprocessor.locals else None,
				description = preprocessor.locals["description"] if "description" in preprocessor.locals else None,
				themeColor = preprocessor.locals["themeColor"] if "themeColor" in preprocessor.locals else None,
				hidden = preprocessor.locals["hidden"] if "hidden" in preprocessor.locals else False,
				relevantCourses = preprocessor.locals["relevantCourses"] if "relevantCourses" in preprocessor.locals else [],
			)

	def render(self, outpath, extconfig, parameters):
		"""Render the markdown code with the PLSres extensions"""
		if extconfig.cache.parenttable == extconfig.parenttable and self.docpath in extconfig.cache.documents:
			doccache = extconfig.cache.documents[self.docpath]
			editdate = os.path.getmtime(self.sourcepath)
			if editdate <= doccache["lastcompiled"]:
				return

		print(f"Rendering document {self.docpath}")
		extension = PLSResExtension(self.sourcepath, self, extconfig, parameters)
		extension.start()
		md = markdown.Markdown(extensions=["tables", extension])
		with open(self.sourcepath, "r", encoding="utf-8") as mdfile:
			html = md.convert(mdfile.read())

		with open(outpath, "w", encoding="utf-8") as outfile:
			outfile.write(html)
		extension.finish()
