class Node (object):
	def __init__(self, type, params={}, baseindent=0):
		self.type = type
		self.params = params
		self.children = []
		self.text = ""
		self.baseindent = baseindent

	def __repr__(self):
		dic = self.__dict__.copy()
		dic["children"] = [child.type for child in self.children]
		return str(dic)

class Exercise (object):
	def __init__(self, node):
		self.name = None
		self.title = None
		self.tags = []
		self.courses = None
		self.source = None
		self.todo = None
		self.questions = []
		for child in node.children:
			if child.type == "question":
				question = Question(child)
				self.questions.append(question)
			elif child.type == "exercise":
				self.name = child.params[None][0]
			elif child.type == "title":
				self.title = " ".join(child.params[None])
			elif child.type == "tags":
				self.tags = child.params[None]
			elif child.type == "courses":
				self.courses = child.params[None]
			elif child.type == "source":
				self.source = " ".join(child.params[None])
			elif child.type == "todo":
				self.todo = " ".join(child.params[None])
			else:
				raise ValueError(f"Bad node type at exercise level : {child.type} (expected `question`)")
	
	def serialize(self):
		return {
			"name": self.name,
			"title": self.title,
			"tags": self.tags,
			"courses": self.courses,
			"source": self.source,
			"questions": [question.serialize() for question in self.questions],
		}

class Question (object):
	def __init__(self, node):
		self.type = node.params["type"] if "type" in node.params else "simple"
		self.difficulty = int(node.params["difficulty"]) if "difficulty" in node.params else None
		self.hints = []
		self.choices = []
		self.title = None
		self.text = None
		self.answer = None

		for child in node.children:
			if child.type == "text":
				self.text = child.text
			elif child.type == "title":
				self.title = child.text
			elif child.type == "answer":
				self.answer = child.text
			elif child.type == "hint":
				self.hints.append(Hint(child))
			elif self.type == "choices" and child.type == "choice":
				self.choices.append(Choice(child))
			else:
				raise ValueError(f"Bad node type at question level : {child.type}")
	
	def serialize(self):
		return {
			"type": self.type,
			"difficulty": self.difficulty,
			"hints": [hint.serialize() for hint in self.hints],
			"choices": [choice.serialize() for choice in self.choices],
			"title": self.title,
			"text": self.text,
			"answer": self.answer,
		}

class Hint (object):
	def __init__(self, node):
		self.level = int(node.params[None][0])
		self.text = node.text
	
	def serialize(self):
		return {
			"level": self.level,
			"text": self.text,
		}

class Choice (object):
	def __init__(self, node):
		self.value = node.params[None][0]
		self.text = self.answer = None
		for child in node.children:
			if child.type == "text":
				self.text = child.text
			elif child.type == "answer":
				self.answer = child.text
	
	def serialize(self):
		return {
			"value": self.value,
			"text": self.text,
			"answer": self.answer,
		}

def parse_exercise(file):
	indentchars = None
	nodestack = [Node("root"), None]
	for line in file:
		linecontent = line.lstrip(" \t")
		if indentchars is None and line != linecontent:
			indentchars = line[:-len(linecontent)]

		if len(line) - len(linecontent) == 0:
			indent = 0
		else:
			indent = (len(line) - len(linecontent)) // len(indentchars)

		if linecontent.startswith("::"):
			while indent < len(nodestack) - 2:
				nodestack.pop()

			nodeparams = linecontent.lstrip(":").split()
			type = nodeparams[0]
			params = {None: []}
			for paramstring in nodeparams[1:]:
				if "=" in paramstring:
					key, value = paramstring.split("=")
					params[key] = value
				else:
					params[None].append(paramstring)
			node = Node(type, params, indent)

			if indent == len(nodestack) - 1:
				nodestack[-1].children.append(node)
				nodestack.append(node)
			else:
				nodestack.pop()
				nodestack[-1].children.append(node)
				nodestack.append(node)
		else:
			textindent = indent - nodestack[-1].baseindent - 1
			textline = indentchars*textindent + linecontent
			nodestack[-1].text += textline
	return Exercise(nodestack[0])
