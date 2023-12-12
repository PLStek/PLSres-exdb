import os
import sys
import yaml
import markdown
import argparse
from plsres.util import Attributes
from plsres.extension import PLSResExtension

def load_licenses(parameters):
	with open(os.path.join(parameters.template, "licenses.yml"), "r", encoding="utf-8") as licensefile:
		licenselist = yaml.load(licensefile.read(), yaml.Loader)

	licenses = {}
	for item in licenselist["licenses"]:
		for id in item["id"]:
			licenses[id] = item
	return licenses

def load_parameters(filename):
	with open(filename, "r", encoding="utf-8") as paramfile:
		return Attributes(yaml.load(paramfile.read(), yaml.Loader))

def load_exercise_config(parameters):
	attrpath = os.path.join(parameters.template, "exercises.yml")
	with open(attrpath, "r", encoding="utf-8") as attrfile:
		return Attributes(yaml.load(attrfile.read(), yaml.Loader))

def load_extconfig(parameters):
	return Attributes(
		pathtable = {},
		documenttree = {},
		linktable = {},
		parenttable = {},
		template = "{=__content}",
		licenses = load_licenses(parameters),
		globals = {},
		cache = Attributes(documents={}),
		quick = False,
		updateall = True,
		exerciseconfig = load_exercise_config(parameters),
	)

def default_document(parameters):
	return Attributes(docpath="")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--parameters", "-p", default="generate.yml")
	args = parser.parse_args()

	input_md = sys.stdin.read()
	parameters = load_parameters(args.parameters)
	extension = PLSResExtension("", default_document(parameters), load_extconfig(parameters), parameters, ispage=False)
	extension.start()
	md = markdown.Markdown(extensions=["tables", extension])
	html = md.convert(input_md)
	print(html)
	extension.finish()
