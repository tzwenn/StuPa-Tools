# -*- coding: utf-8 -*-

import string

document_tex = string.Template(r"""
\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[pdfusetitle]{hyperref}
\usepackage[all]{hypcap}
\usepackage{pdfpages}
\usepackage{pdflscape}

\usepackage[top=0pt]{geometry}

\author{StuPa-Präsidium}
\title{$title}

\pagestyle{empty}

\begin{document}

\clearpage\phantomsection
$content

\clearpage\phantomsection
\tiny 
Bitte diese Seite löschen (Preview.app, cpdf, pdftk, \ldots)
\tableofcontents

\end{document}""")

clearpage_tex = r"""

\clearpage\phantomsection"""

section_tex = string.Template(r"""
\addcontentsline{toc}{$depth}{$name}""")

includepdf_tex = string.Template(r"""
\includepdf[pages=-,linktodoc=false,fitpaper]{$filename}""")


