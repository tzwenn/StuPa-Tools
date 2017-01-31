#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import io
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
			shutil.copyfile(tmpOutputName, outputFileName)

########## 

def parseArguments():
	parser = argparse.ArgumentParser(description="Tool zur Erstellung einer Sitzungsmappe aus einer YAML Beschreibung.")
	parser.add_argument("inputfile", nargs='?',
				type=argparse.FileType("r", encoding="utf-8"), 
				default=io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8'),
				help="Die Eingabedatei (Standardeingabe wenn unspezifiziert)")
	parser.add_argument("--public", "-p", action="store_true", help="Erzeuge die oeffentliche Version")

	title_group = parser.add_mutually_exclusive_group()
	title_group.add_argument("--nummer", "-n", type=int, default=None, help="Nummer der ordentlichen Sitzung (kommt in den Titel)")
	title_group.add_argument("--titel", "-t", type=str, help="Der im PDF eingebundene Titel")

	parser.add_argument("--ausgabe", "-o", type=str, default="Sitzungsmappe.pdf", help="Ausgabedatei")
	parser.add_argument("--datenordner", "-d", type=str, default=".", help="Verzeichnis mit den Eingabedateien (Standard: Aktuelles Arbeitsverzeichnis)")

	args = parser.parse_args()
	if args.titel is None:
		args.titel = "Sitzungsmappe" if args.nummer is None else ("Sitzungsmappe der %d. ordentlichen Sitzung" % args.nummer)

	return args

if __name__ == "__main__":
	args = parseArguments()
	try:
		builder = SitzungsmappenBuilder(args.inputfile, args.datenordner, args.titel)
		builder.build(args.ausgabe, public=args.public)
	except KeyboardInterrupt:
		pass


