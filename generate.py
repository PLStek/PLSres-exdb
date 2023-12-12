import os
import sys
import yaml
import markdown
from plsres.site import Site
from plsres.util import Attributes


if __name__ == "__main__":
	with open("generate.yml", "r", encoding="utf-8") as paramfile:
		parameters = Attributes(yaml.load(paramfile.read(), yaml.Loader))

	if not os.path.exists(parameters.temporary):
		os.makedirs(parameters.temporary)
	if not os.path.exists(parameters.output):
		os.makedirs(parameters.output)

	site = Site(parameters, quick=("-q" in sys.argv), full=("-f" in sys.argv))
	site.load()
	site.render()
