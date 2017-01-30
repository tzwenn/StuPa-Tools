#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys
import tempfile

import yaml

import resources

class NonPublicEntry(yaml.YAMLObject):
	yaml_tag = u"!intern"

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "%s(name=%r)" % (self.__class__.__name__, self.name)

	def __str__(self):
		return self.name

def non_public_constructor(loader, node):
	return NonPublicEntry(loader.construct_scalar(node))

yaml.add_constructor(u"!non-public", non_public_constructor)
yaml.add_constructor(u"!intern"    , non_public_constructor)

########## 

class SitzungsmappenBuilder(object):

	def __init__(self, contentStream, contentDirectory, title):
		self.content = yaml.load(contentStream)
		self.contentDirectory = os.path.abspath(contentDirectory)
		self.title = title

	def _tex_content(self, sections, public, currentDepth="section"):

		def include_that(nameOrObject):
			return not (isinstance(nameOrObject, NonPublicEntry) and public)

		def format_entry(name):
			return resources.section_tex.substitute(
						depth = currentDepth,
						name = str(name))

		def format_subsection(name, subsections):
			sub = self._tex_content(subsections, 
				                    public,
				  				    "sub" + currentDepth)
			included_any = bool(sub)
			if included_any:
				return format_entry(name) + sub
			else:
				return ""

		def format_include(fileName):
			return resources.includepdf_tex.substitute(
					     filename=os.path.join(self.contentDirectory, fileName))

		def traverse():
			for entry in sections:
				(name, fileNameOrSectionContent), = entry.items()
				if not include_that(name):
					continue

				if isinstance(fileNameOrSectionContent, list):
					yield format_subsection(name, fileNameOrSectionContent)
				else:
					yield format_entry(name) + format_include(fileNameOrSectionContent)

		return resources.clearpage_tex.join(traverse())


	def _changeExt(self, fileName, newExtension):
		return os.extsep.join((os.path.splitext(fileName)[0], newExtension))

	def _stripLastPage(self, source, dest):
		# shutil.copyfile(source, dest)
		cmd_line = ["cpdf", source, "1-~2", "-o", dest]
		with subprocess.Popen(cmd_line) as p:
			p.wait()

	def build(self, outputFileName, public=False):
		with tempfile.TemporaryDirectory() as tmpDirName:
			tempFileName = os.path.join(tmpDirName, "Sitzungsmappe.tex")
			with open(tempFileName, "w", encoding="utf-8") as f:
				f.write(resources.document_tex.substitute(
					title = self.title,
					content = self._tex_content(self.content, public)
				))
			with subprocess.Popen(["latexmk", "-pdf"], cwd=tmpDirName) as p:
				p.wait()
			tmpOutputName = self._changeExt(tempFileName, 'pdf')
			self._stripLastPage(tmpOutputName, outputFileName)

########## 

if __name__ == "__main__":
	testfile = "testdata/test.yml" if len(sys.argv) < 2 else sys.argv[1]
	builder = SitzungsmappenBuilder(open(testfile, encoding="utf-8"), 
	                     "/Users/sven/ownCloud/StuPA/201617/17-01-31/Sitzungsmappe",
	                     "Sitzungsmappe der n. ordentlichen Sitzung")
	builder.build("20171438-Sitzungsmappe.pdf", public=False)
