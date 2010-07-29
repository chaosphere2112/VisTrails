############################################################################
##
## Copyright (C) 2006-2010 University of Utah. All rights reserved.
##
## This file is part of VisTrails.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following to ensure GNU General Public
## Licensing requirements will be met:
## http://www.opensource.org/licenses/gpl-license.php
##
## If you are unsure which license is appropriate for your use (for
## instance, you are interested in developing a commercial derivative
## of VisTrails), please contact us at vistrails@sci.utah.edu.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

import os
from xml.dom import minidom, Node
from auto_gen_objects import Object, Property, Choice

class AutoGenParser:
    def __init__(self):
	pass

    def parse(self, dir):
	objects = {}
	for file in os.listdir(dir):
	    if file.endswith('.xml'):
		filename = os.path.join(dir, file)
		print filename
		dom = minidom.parse(filename)
		domObjects = dom.getElementsByTagName('object')
		for node in domObjects:
		    curObject = self.parseObject(node)
		    objects[curObject.getName()] = curObject

        # set the referenced objects here
        for obj in objects.itervalues():
            for prop in obj.properties:
                if prop.getReference():
                    try:
                        prop.setReferencedObject(objects[prop.getReference()])
                    except KeyError:
                        print 'error:', prop.getReference()
            for choice in obj.choices:
                for prop in choice.properties:
                    if prop.getReference():
                        try:
                            prop.setReferencedObject(
                                objects[prop.getReference()])
                        except KeyError:
                            print 'error:', prop.getReference()
                
	return objects

    def parseObject(self, node):
	params = {}
	properties = []
	choices = []
	layouts = None
	for attr in node.attributes.keys():
	    params[attr] = node.attributes.get(attr).value
	for child in node.childNodes:
	    if child.nodeType == Node.ELEMENT_NODE:
		if child.nodeName == 'layout':
		    layouts = self.parseLayouts(child)
		elif child.nodeName == 'property':
		    property = self.parseProperty(child)
		    properties.append(property)
		elif child.nodeName == 'choice':
		    choice = self.parseChoice(child)
		    choices.append(choice)
	return Object(params, properties, layouts, choices)
    
    def parseLayouts(self, node):
	layouts = {}
	for child in node.childNodes:
	    if child.nodeType == Node.ELEMENT_NODE:
		layouts[child.nodeName] = self.parseDataToDict(child)
	return layouts

    def parseProperty(self, node):
	params = {}
	specs = {}
	for attr in node.attributes.keys():
	    params[attr] = node.attributes.get(attr).value
	for child in node.childNodes:
	    if child.nodeType == Node.ELEMENT_NODE:
		specs[child.nodeName] = self.parseDataToDict(child)
	return Property(params, specs)

    def parseChoice(self, node):
	params = {}
	properties = []
	for attr in node.attributes.keys():
	    params[attr] = node.attributes.get(attr).value
	for child in node.childNodes:
	    if child.nodeType == Node.ELEMENT_NODE and \
		    child.nodeName == 'property':
		properties.append(self.parseProperty(child))
	return Choice(params, properties)

    def parseDataToDict(self, node):
	dict = {}
	if node.nodeType == Node.ELEMENT_NODE:
	    for attr in node.attributes.keys():
		dict[attr] = node.attributes.get(attr).value
	    for child in node.childNodes:
		if child.nodeType == Node.ELEMENT_NODE:
		    dict[child.nodeName] = child.childNodes[0].data
	return dict
