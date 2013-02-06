#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on Dec 5, 2012

A script that takes SVG files output from programs like Inkscape and outputs
files with what seems to be the minimal amount of code needed to copy and embed
into HTML files.

This script requires Python 3 and BeautifulSoup 4.

@author: Chris
@copy: 2012-2013 eBook Architects, 2013- Firebrand Technologies
@python-ver: 3.2.3
'''

from bs4 import BeautifulSoup
import os
import sys

sourcedir = os.path.abspath(os.curdir)
outdir = r"%s\output" % sourcedir

if not os.path.exists(outdir):
    os.mkdir(outdir)


def clean(source):
    if source.metadata:
        source.metadata.decompose()
    if source.defs:
        source.defs.decompose()
    for tag in source.find_all(True):
        if tag.name.lower() == 'sodipodi:namedview':
            tag.extract()

    height = source['height']
    width = source['width']

    # The attribute dictionary can't be simply deleted, so a list of the keys is created
    attr_list = list(source.attrs.keys())
    for attr in attr_list:
        del source[attr]

    source['viewBox'] = "0 0 %s %s" % (width, height)
    source['preserveAspectRatio'] = "xMinYMin"
    source['version'] = "1.1"
    source['xmlns'] = "http://www.w3.org/2000/svg"
    source['xmlns:svg'] = "http://www.w3.org/2000/svg"

for file in os.listdir(sourcedir):
    # print(file)
    if file.endswith('svg'):
        svg_file = open(os.path.join(sourcedir, file))
        svg_soup = BeautifulSoup(svg_file)
        svg_file.close()
        svg_tag = svg_soup.svg
        clean(svg_tag)
        svg = svg_soup.svg.prettify()
        svg_out = open(os.path.join(outdir, file), 'w')
        svg_out.write(str(svg))
        svg_out.close()

print("SVGs been cleaned.")
sys.exit()
