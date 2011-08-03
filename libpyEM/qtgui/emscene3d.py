#!/usr/bin/env python
#
# Author: John Flanagan (jfflanag@bcm.edu)
# Copyright (c) 2000-2006 Baylor College of Medicine


# This software is issued under a joint BSD/GNU license. You may use the
# source code in this file under either license. However, note that the
# complete EMAN2 and SPARX software packages have some GPL dependencies,
# so you are responsible for compliance with the licenses of these packages
# if you opt to use BSD licensing. The warranty disclaimer below holds
# in either instance.
#
# This complete copyright notice must be included in any revised version of the
# source code. Additional authorship citations may be added, but existing
# author citations must be preserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  2111-1307 USA
#
#

from EMAN2 import *
from OpenGL.GL import *
from OpenGL import GLU
from PyQt4 import QtCore, QtGui, QtOpenGL 
from PyQt4.QtCore import Qt
from emapplication import EMGLWidget
from emitem3d import EMItem3D, EMItem3DInspector
from libpyGLUtils2 import GLUtil
from valslider import ValSlider, EMLightControls, CameraControls, EMSpinWidget, EMQTColorWidget, EMANToolButton
import math, weakref, os, pickle
from emshapeitem3d import *
from emdataitem3d import EMDataItem3D, EMIsosurface
# XPM format Cursors

visibleicon = [
    '16 12 3 1',
    'a c #0000ff',
    'b c #000000',
    'c c None',
    'cccccccccccccccc',
    'ccccccbbbbcccccc',
    'ccccbbbbbbbbcccc',
    'ccbbbccccccbbbcc',
    'cbbccccaaccccbbc',
    'cbccccaaaaccccbc',
    'cbccccaaaaccccbc',
    'cbbccccaaccccbbc',
    'ccbbbccccccbbbcc',
    'ccccbbbbbbbbcccc',
    'ccccccbbbbcccccc',
    'cccccccccccccccc'
]
    
invisibleicon = [
    '16 12 2 1',
    'b c #000000',
    'c c None',
    'cbbcccccccccbbcc',
    'ccbbcccccccbbccc',
    'cccbbcccccbbcccc',
    'ccccbbcccbbccccc',
    'cccccbbcbbcccccc',
    'ccccccbbbccccccc',
    'ccccccbbbccccccc',
    'cccccbbcbbcccccc',
    'ccccbbcccbbccccc',
    'cccbbcccccbbcccc',
    'ccbbcccccccbbccc',
    'cbbcccccccccbbcc'
]

zrotatecursor = [
    '15 14 2 1',
    'b c #00ff00',
    'c c None',
    'ccccccccccccccc',
    'ccccbbbbbbccbcc',
    'ccbbbbbbbbbbbbc',
    'cbbbcccccbbbbbc',
    'bbbcccccbbbbbbb',
    'bbcccccbbbbbbbc',
    'ccccccccccccccc',
    'ccccccccccccccc',
    'cbbbbbbbcccccbb',
    'bbbbbbbcccccbbb',
    'cbbbbbcccccbbbc',
    'cbbbbbbbbbbbbcc',
    'ccbccbbbbbbcccc',
    'ccccccccccccccc'
]

xyrotatecursor = [
    '14 13 2 1',
    'b c #00ff00',
    'c c None',
    'cccccccccccccc',
    'ccccbbbbbbcccc',
    'ccbbbbbbbbbbcc',
    'cbbbccccccbbbc',
    'bbbccccccccbbb',
    'bbbccccccccbbb',
    'bbbccccccccbbb',
    'bbbccccccccbbb',
    'bbbccccccccbbb',
    'cbbbccccccbbbc',
    'ccbbbbbbbbbbcc',
    'ccccbbbbbbcccc',
    'cccccccccccccc'
]

crosshairscursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'cccccccbbcccccccc',
    'ccccccbbbbccccccc',
    'cccccbbbbbbcccccc',
    'cccccccbbcccccccc',
    'cccccccbbcccccccc',
    'ccbccccbbccccbccc',
    'cbbccccbbccccbbcc',
    'bbbbbbbbbbbbbbbbb',
    'bbbbbbbbbbbbbbbbb',
    'cbbccccbbccccbbcc',
    'ccbccccbbccccbccc',
    'cccccccbbcccccccc',
    'cccccccbbcccccccc',
    'cccccbbbbbbcccccc',
    'ccccccbbbbccccccc',
    'cccccccbbcccccccc'
]   

zhaircursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'ccccccccccccccccc',
    'cccbccccccccccccc',
    'ccbbbcccccccccccc',
    'cbcbcbccccccccccc',
    'cccbccccccccccccc',
    'cccbccccccccccccc',
    'cccbccccccbbccccc',
    'cccbccccbbccccccc',
    'cccbccbbccccccccc',
    'cccbbbccccccccccc',
    'cccbccccccccccccc',
    'ccccbbccccccccccc',
    'ccccccbbccccccccc',
    'ccccccccbbccccccc',
    'ccccccccccbbccccc',
    'ccccccccccccccccc'
]

scalecursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'bbbbbbbbcccccccc',
    'bccccccccccccccc',
    'bccccccccccccccc',
    'bccccccccccccccc',
    'bccccccccccccccc',
    'bccccbbbbbbccccc',
    'bccccbccccbccccc',
    'bccccbccccbccccc',
    'cccccbccccbccccb',
    'cccccbccccbccccb',
    'cccccbbbbbbccccb',
    'cccccccccccbcccb',
    'ccccccccccccbccb',
    'cccccccccccccbcb',
    'ccccccccccccccbb',
    'ccccccccbbbbbbbb'
]   

selectorcursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'cbbbbbbbbbcccccc',
    'bcccccccccbccccc',
    'cbbbbbbbcccbcccc',
    'cccbccccccccbccc',
    'ccccbbbbccccbccc',
    'cccbccccccccbccc',
    'ccccbbbbcccbcbcc',
    'cccbccccccbcccbc',
    'ccccbbbbbbcccccb',
    'cccccccbccbcccbc',
    'ccccccccbccccbcc',
    'cccccccccbccbccc',
    'ccccccccccbbcccc',
    'cccccccccccccccc',
    'cccccccccccccccc',
    'cccccccccccccccc'
]

cubecursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'cccccccccccccccccc',
    'cccccccccccccccccc',
    'ccccccbbbbbbbbbccc',
    'cccccbbbbbbbbbbccc',
    'ccccbbbbbbbbbbbccc',
    'cccbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbcccc',
    'ccbbbbbbbbbbbccccc',
    'ccbbbbbbbbbbcccccc',
    'ccbbbbbbbbbccccccc',
    'cccccccccccccccccc',
    'cccccccccccccccccc'
]

spherecursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'ccccccccccccccccc',
    'cccccccbbbccccccc',
    'cccccbbbbbbbccccc',
    'ccccbbbbbbbbbcccc',
    'cccbbbbbbbbbbbccc',
    'cccbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'cccbbbbbbbbbbbccc',
    'cccbbbbbbbbbbbccc',
    'ccccbbbbbbbbbcccc',
    'cccccbbbbbbbccccc',
    'cccccccbbbccccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc'
]

cylindercursor = [
    '16 16 2 1',
    'b c #00ff00',
    'c c None',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'cccccbbbbbbbccccc',
    'cccbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'cccbbbbbbbbbbbccc',
    'cccccbbbbbbbccccc',
    'ccccccccccccccccc'
] 

cubeicon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'cccccccccccccccccc',
    'cccccccccccccccccc',
    'ccccccbbbbbbbbbccc',
    'cccccbbbbbbbbbbccc',
    'ccccbbbbbbbbbbbccc',
    'cccbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbcccc',
    'ccbbbbbbbbbbbccccc',
    'ccbbbbbbbbbbcccccc',
    'ccbbbbbbbbbccccccc',
    'cccccccccccccccccc',
    'cccccccccccccccccc'
] 

sphereicon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'cccccccbbbccccccc',
    'cccccbbbbbbbccccc',
    'ccccbbbbbbbbbcccc',
    'cccbbbbbbbbbbbccc',
    'cccbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'cccbbbbbbbbbbbccc',
    'cccbbbbbbbbbbbccc',
    'ccccbbbbbbbbbcccc',
    'cccccbbbbbbbccccc',
    'cccccccbbbccccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc'
] 

cylindericon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'cccccbbbbbbbccccc',
    'cccbbbbbbbbbbbccc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'cccbbbbbbbbbbbccc',
    'cccccbbbbbbbccccc',
    'ccccccccccccccccc'
] 

texticon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbbbbbbbbbbbbcc',
    'ccbbcccbbbcccbbcc',
    'ccbccccbbbccccbcc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'cccccccbbbccccccc',
    'ccccccbbbbbcccccc',
    'cccccbbbbbbbccccc',
    'ccccccccccccccccc'
] 

isosurfaceicon = [
    '17 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'bbbccbbbbcccbbbbc',
    'cbccbccccbcbccccb',
    'cbccbccccbcbccccb',
    'cbcccbcccccbccccb',
    'cbccccbccccbccccb',
    'cbcccccbcccbccccb',
    'cbccccccbccbccccb',
    'cbccbccccbcbccccb',
    'cbccbccccbcbccccb',
    'bbbccbbbbcccbbbbc',
    'ccccccccccccccccc',
    'ccccccccccccccccc'
] 

rotateicon = [
    '15 14 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccc',
    'ccccbbbbbbccbcc',
    'ccbbbbbbbbbbbbc',
    'cbbbcccccbbbbbc',
    'bbbcccccbbbbbbb',
    'bbcccccbbbbbbbc',
    'ccccccccccccccc',
    'ccccccccccccccc',
    'cbbbbbbbcccccbb',
    'bbbbbbbcccccbbb',
    'cbbbbbcccccbbbc',
    'cbbbbbbbbbbbbcc',
    'ccbccbbbbbbcccc',
    'ccccccccccccccc'
]

crosshairsicon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'cccccccbbcccccccc',
    'ccccccbbbbccccccc',
    'cccccbbbbbbcccccc',
    'cccccccbbcccccccc',
    'cccccccbbcccccccc',
    'ccbccccbbccccbccc',
    'cbbccccbbccccbbcc',
    'bbbbbbbbbbbbbbbbb',
    'bbbbbbbbbbbbbbbbb',
    'cbbccccbbccccbbcc',
    'ccbccccbbccccbccc',
    'cccccccbbcccccccc',
    'cccccccbbcccccccc',
    'cccccbbbbbbcccccc',
    'ccccccbbbbccccccc',
    'cccccccbbcccccccc'
] 

multiselectoricon = [
    '17 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc',
    'cbcbcbcbcbcbcbccc',
    'ccccccccccccccccc',
    'cbcccccccccccbccc',
    'ccccccccccccccccc',
    'cbcccccccccccbccc',
    'ccccccccccccccccc',
    'cbcccccccccccbccc',
    'cccccccccccccbbbc',
    'cbcbcbcbcbcbcbbbc',
    'cccccccccccccbbbb',
    'ccccccccccccccccb',
    'ccccccccccccccccc'
] 

scaleicon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'bbbbbbbbcccccccc',
    'bccccccccccccccc',
    'bccccccccccccccc',
    'bccccccccccccccc',
    'bccccccccccccccc',
    'bccccbbbbbbccccc',
    'bccccbccccbccccc',
    'bccccbccccbccccc',
    'cccccbccccbccccb',
    'cccccbccccbccccb',
    'cccccbbbbbbccccb',
    'cccccccccccbcccb',
    'ccccccccccccbccb',
    'cccccccccccccbcb',
    'ccccccccccccccbb',
    'ccccccccbbbbbbbb'
]

ztransicon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'cccbccccccccccccc',
    'ccbbbcccccccccccc',
    'cbcbcbccccccccccc',
    'cccbccccccccccccc',
    'cccbccccccccccccc',
    'cccbccccccbbccccc',
    'cccbccccbbccccccc',
    'cccbccbbccccccccc',
    'cccbbbccccccccccc',
    'cccbccccccccccccc',
    'ccccbbccccccccccc',
    'ccccccbbccccccccc',
    'ccccccccbbccccccc',
    'ccccccccccbbccccc',
    'ccccccccccccccccc'
] 

selectionicon = [
    '16 16 2 1',
    'b c #000055',
    'c c None',
    'ccccccccccccccccc',
    'ccbcccccccccccccc',
    'ccbbccccccccccccc',
    'ccbcbbccccccccccc',
    'ccbcccbcccccccccc',
    'ccbccccbbcccccccc',
    'ccbccccccbccccccc',
    'ccbcccccccbbccccc',
    'ccbcccccbbbbbcccc',
    'ccbccbccbcccccccc',
    'ccbcbcbccbccccccc',
    'ccbbccbccbccccccc',
    'ccbccccbccbcccccc',
    'ccccccccbbbcccccc',
    'ccccccccccccccccc',
    'ccccccccccccccccc'
] 
class EMScene3D(EMItem3D, EMGLWidget):
	"""
	Widget for rendering 3D objects. Uses a scne graph for rendering
	"""
	def __init__(self, parentwidget=None, SGactivenodeset=set(), scalestep=0.5):
		"""
		@param parent: The parent of the widget
		@param SGnodelist: a list enumerating all the SGnodes
		@param SGactivenodeset: a set enumerating the list of active nodes
		@param scalestep: The step to increment the object scaling
		"""
		EMItem3D.__init__(self, parent=None, transform=Transform())
		EMGLWidget.__init__(self,parentwidget)
		QtOpenGL.QGLFormat().setDoubleBuffer(True)
		self.camera = EMCamera(1.0, 500.0)	# Default near,far, and zclip values
		self.clearcolor = [0.0, 0.0, 0.0, 0.0]	# Back ground color
		self.main_3d_inspector = None
		self.item_inspector = None				# Get the inspector GUI
		self.reset_camera = False				# Toogle flag to deterine if the clipping plane has changed and needs redrawing
		#self.SGactivenodeset = SGactivenodeset			# A set of all active nodes (currently not used)
		self.scalestep = scalestep				# The scale factor stepsize
		self.toggle_render_selectedarea = False			# Don't render the selection box by default
		self.mousemode = "Selection"				# The mouse mode
		self.zrotatecursor = QtGui.QCursor(QtGui.QPixmap(zrotatecursor),-1,-1)
		self.xyrotatecursor = QtGui.QCursor(QtGui.QPixmap(xyrotatecursor),-1,-1)
		self.crosshaircursor = QtGui.QCursor(QtGui.QPixmap(crosshairscursor),-1,-1)
		self.scalecursor = QtGui.QCursor(QtGui.QPixmap(scalecursor),-1,-1)
		self.zhaircursor = QtGui.QCursor(QtGui.QPixmap(zhaircursor),-1,-1)
		self.selectorcursor = QtGui.QCursor(QtGui.QPixmap(selectorcursor),-1,-1)
		self.cubecursor = QtGui.QCursor(QtGui.QPixmap(cubecursor),-1,-1)
		self.spherecursor = QtGui.QCursor(QtGui.QPixmap(spherecursor),-1,-1)
		self.cylindercursor = QtGui.QCursor(QtGui.QPixmap(cylindercursor),-1,-1)

	def getEvalString(self):
		"""
		Retrun a string that after eval can reinstatiate the object
		"""
		return "SG"
		
	def initializeGL(self):
		glClearColor(self.clearcolor[0], self.clearcolor[1], self.clearcolor[2], self.clearcolor[3])		# Default clear color is black
		glShadeModel(GL_SMOOTH)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_NORMALIZE)
		self.firstlight = EMLight(GL_LIGHT0)
		self.firstlight.enableLighting()
        
	def paintGL(self):
		if self.reset_camera: self.camera.update()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)		
		glColor3f(1.0, 1.0, 1.0)	# Default color is white
		#Call rendering
		self.renderSelectedArea() 	# Draw the selection box if needed
		self.render()			# SG nodes must have a render method
		glFlush()			# Finish rendering
		self.reset_camera = False
		
	def resizeGL(self, width, height):
		self.camera.update(width, height)
		if self.main_3d_inspector: self.main_3d_inspector.updateInspector()
	
	def getItemInspector(self):
		"""
		Return a Qt widget that controls the scene item
		"""	
		if not self.item_inspector: self.item_inspector = EMItem3DInspector("All Objects", self)
		return self.item_inspector
		
	def renderNode(self):
		pass
	
	def setInspector(self, inspector):
		"""
		Set the main 3d inspector
		"""
		self.main_3d_inspector = inspector
		
	def pickItem(self):
		"""
		Pick an item on the screen using openGL's selection mechanism
		"""
		self.makeCurrent()	# This is needed so we use openGL for the correct widget!!!
		viewport = glGetIntegerv(GL_VIEWPORT)
		glSelectBuffer(1024)	# The buffer size for selection
		glRenderMode(GL_SELECT)
		glInitNames()
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		
		# Find the selection box. Go from Volume view coords to viewport coords. sa = selection area
		dx = self.sa_xf - self.sa_xi
		dy = self.sa_yf - self.sa_yi 
		x = (self.sa_xi + self.camera.getWidth()/2) 
		y = (self.camera.getHeight()/2 - self.sa_yi)

		# Apply selection box, and center it in the green box
		GLU.gluPickMatrix(x - dx/2, (viewport[3] - y) + dy/2, dx, dy, viewport)
		self.camera.setProjectionMatrix()
		
		#drawstuff, but first we need to remove the influence of any previous xforms which ^$#*$ the selection
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		self.camera.setCameraPosition(sfactor=1) # Factor of two to compensate for the samera already being set
		self.render()
		glPopMatrix()
		
		# Return to default state
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		glMatrixMode(GL_MODELVIEW)
		records = glRenderMode(GL_RENDER)
		
		# process records
		self.processSelection(records)
	
	def selectArea(self, xi, xf, yi, yf):
		"""
		Set an area for selection. Need to switch bewteen viewport coords, where (0,0 is bottom left) to
		volume view coords where 0,0) is center of the screen.
		"""
		self.sa_xi = xi - self.camera.getWidth()/2
		self.sa_xf = xf - self.camera.getWidth()/2
		self.sa_yi = -yi + self.camera.getHeight()/2
		self.sa_yf = -yf + self.camera.getHeight()/2
		self.toggle_render_selectedarea = True
		
	def deselectArea(self):
		"""
		Turn off selectin box
		"""
		self.sa_xi = 0.0
		self.sa_xf = 0.0
		self.sa_yi = 0.0
		self.sa_yf = 0.0
		self.toggle_render_selectedarea = False
		
	def renderSelectedArea(self):
		"""
		Draw the selection box, box is always drawn orthographically
		"""
		if self.toggle_render_selectedarea: 
			glMatrixMode(GL_PROJECTION)
			glPushMatrix()
			glLoadIdentity()
			self.camera.setOrthoProjectionMatrix()
			glColor3f(0.0,1.0,0.0)
			glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
			glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0,0.0,0.0,1.0])
			glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0,0.0,0.0,1.0])
			glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,1.0,0.0,1.0])
			glBegin(GL_LINE_LOOP)
			# set the box just in front of the cliping plane
			z = -self.camera.getClipNear() - self.camera.getZclip()
			glVertex3f(self.sa_xi, self.sa_yi, z)
			glVertex3f(self.sa_xi, self.sa_yf, z)
			glVertex3f(self.sa_xf, self.sa_yf, z)
			glVertex3f(self.sa_xf, self.sa_yi, z)
			glEnd()
			glPopMatrix()
			glMatrixMode(GL_MODELVIEW)
			glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
		
	def processSelection(self, records):
		"""
		Process the selection records
		"""
		# Remove old selection if not in append mode
		if not self.appendselection:
			for selected in self.getAllSelectedNodes():
				selected.setSelectedItem(False)
				# Inspector tree management
				if EMQTreeWidgetItem:
					selected.EMQTreeWidgetItem.setSelectionStateBox()
					self.main_3d_inspector.tree_widget.setCurrentItem(selected.EMQTreeWidgetItem)
		# Select the desired items	
		closestitem = None
		bestdistance = 1.0
		for record in records:
			if self.multiselect:
				selecteditem = EMItem3D.selection_idx_dict[record.names[len(record.names)-1]]()
				# Extending toggling to multiple item makes for bonkers bahaviour
				#if selecteditem.isSelectedItem(): self.itemstodeselect.append(selecteditem) # This will toogle any presiouly selected items in the item list, provided we don't move it.
				selecteditem.setSelectedItem(True)
				# Inspector tree management
				if self.main_3d_inspector: self.main_3d_inspector.updateInspectorTree(selecteditem)
			else:
				if record.near < bestdistance:
					bestdistance = record.near
					closestitem = record
		if closestitem:
			selecteditem = EMItem3D.selection_idx_dict[closestitem.names[len(closestitem.names)-1]]()
			if selecteditem.isSelectedItem(): self.itemstodeselect.append(selecteditem) # This will toogle any presiouly selected items in the item list, provided we don't move it.
			selecteditem.setSelectedItem(True)
			# Inspector tree management
			if self.main_3d_inspector: self.main_3d_inspector.updateInspectorTree(selecteditem)
	
	def insertNewNode(self, name, node):
		"""
		Insert a new node in the SG
		"""
		insertionpoint = None
		if self.main_3d_inspector: insertionpoint = self.main_3d_inspector.insertNewNode(name, node)
		if insertionpoint:
			insertionpoint[0].insertChild(node, (insertionpoint[1] + 1))
		else:
			self.addChild(node)
		
	# Event subclassing
	def mousePressEvent(self, event):
		"""
		QT event handler. Records the coords when a mouse button is pressed and sets the cursor depending on what button(s) are pressed
		"""
		# The previous x,y records where the mouse was prior to mouse move, rest upon mouse move
		self.previous_x = event.x()
		self.previous_y = event.y()
		# The first x,y records where the mouse was first pressed
		self.first_x = self.previous_x
		self.first_y = self.previous_y
		# Process mouse events
		self.itemstodeselect = []
		if (event.buttons()&Qt.LeftButton and self.mousemode == "cube"):
			self.setCursor(self.cubecursor)
			self.newnode = EMCube(2.0)
			x = event.x() - self.camera.getWidth()/2
			y = -event.y() + self.camera.getHeight()/2
			self.newnode.setTransform(Transform({"type":"eman","tx":x,"ty":y}))
			self.insertNewNode("Cube", self.newnode)
			self.updateSG()
		if (event.buttons()&Qt.LeftButton and self.mousemode == "sphere"):
			self.setCursor(self.spherecursor)
			self.newnode = EMSphere(2.0)
			x = event.x() - self.camera.getWidth()/2
			y = -event.y() + self.camera.getHeight()/2
			self.newnode.setTransform(Transform({"type":"eman","tx":x,"ty":y}))
			self.insertNewNode("Sphere", self.newnode)
			self.updateSG()
		if (event.buttons()&Qt.LeftButton and self.mousemode == "cylinder"):
			self.setCursor(self.cylindercursor)
			self.newnode = EMCylinder(2.0,2.0)
			x = event.x() - self.camera.getWidth()/2
			y = -event.y() + self.camera.getHeight()/2
			self.newnode.setTransform(Transform({"type":"eman","tx":x,"ty":y}))
			self.insertNewNode("Cylinder", self.newnode)
			self.updateSG()	
		if event.buttons()&Qt.RightButton or (event.buttons()&Qt.LeftButton and self.mousemode == "rotate"):
			if  event.y() > 0.95*self.size().height():
				self.setCursor(self.zrotatecursor)
			else:
				self.setCursor(self.xyrotatecursor)
		if (event.buttons()&Qt.LeftButton and self.mousemode == "selection") and not event.modifiers()&Qt.ControlModifier: 
			#self.setCursor(self.selectorcursor)
			self.multiselect = False
			self.appendselection = False
			if event.modifiers()&Qt.ShiftModifier:
				self.appendselection = True
			# 5 seems a big enough selection box
			self.sa_xi = event.x() - self.camera.getWidth()/2
			self.sa_xf = event.x() + 5 - self.camera.getWidth()/2
			self.sa_yi = -event.y() + self.camera.getHeight()/2
			self.sa_yf = -event.y() + 5 + self.camera.getHeight()/2
			self.pickItem()
			self.updateSG()
		if (event.buttons()&Qt.LeftButton and self.mousemode == "multiselection") or (event.buttons()&Qt.LeftButton and event.modifiers()&Qt.ControlModifier and self.mousemode == "selection"):
			#self.setCursor(self.selectorcursor)
			self.multiselect = True
			self.appendselection = False
			if event.modifiers()&Qt.ShiftModifier:
				self.appendselection = True
		if (event.buttons()&Qt.LeftButton and self.mousemode == "ztranslate"):
			self.setCursor(self.zhaircursor)
		if (event.buttons()&Qt.LeftButton and self.mousemode == "xytranslate"):
			self.setCursor(self.crosshaircursor)
		if event.buttons()&Qt.MidButton or (event.buttons()&Qt.LeftButton and self.mousemode == "scale"):
			self.setCursor(self.scalecursor)		
			
	def mouseMoveEvent(self, event):
		"""
		Qt event handler. Scales the SG depending on what mouse button(s) are pressed when dragged
		"""
		dx = event.x() - self.previous_x
		dy = event.y() - self.previous_y
		if (event.buttons()&Qt.LeftButton and self.mousemode == "cube"):
			self.setCursor(self.cubecursor)
			self.newnode.setSize(math.sqrt((event.x() - self.first_x)**2 + (event.y() - self.first_y)**2))
		if (event.buttons()&Qt.LeftButton and self.mousemode == "sphere"):
			self.setCursor(self.spherecursor)
			self.newnode.setRadius(math.sqrt((event.x() - self.first_x)**2 + (event.y() - self.first_y)**2))
		if (event.buttons()&Qt.LeftButton and self.mousemode == "cylinder"):
			self.setCursor(self.cylindercursor)
			self.newnode.setRadiusAndHeight(math.fabs(event.x() - self.first_x), math.fabs(event.y() - self.first_y))
			sign = -(event.y() - self.first_y)
			self.newnode.getTransform().set_rotation({"type":"eman","alt":math.copysign(90,sign)})
		if event.buttons()&Qt.RightButton or (event.buttons()&Qt.LeftButton and self.mousemode == "rotate"):
			magnitude = math.sqrt(dx*dx + dy*dy)
			#Check to see if the cursor is in the 'virtual slider pannel'
			if  event.y() > 0.95*self.size().height(): # The lowest 5% of the screen is reserved from the Z spin virtual slider
				self.setCursor(self.zrotatecursor)
				self.update_matrices([magnitude,0,0,-dx/magnitude], "rotate")
			else:
				self.setCursor(self.xyrotatecursor) 
				self.update_matrices([magnitude,-dy/magnitude,-dx/magnitude,0], "rotate")
		if (event.buttons()&Qt.LeftButton and self.mousemode == "selection") and not event.modifiers()&Qt.ControlModifier:
			#self.setCursor(self.selectorcursor)
			self.update_matrices([dx,-dy,0], "translate")
			self.itemstodeselect = []	# The user means to move not toggle the item
		if (event.buttons()&Qt.LeftButton and self.mousemode == "multiselection") or (event.buttons()&Qt.LeftButton and event.modifiers()&Qt.ControlModifier and self.mousemode == "selection"):
			#self.setCursor(self.selectorcursor)
			self.selectArea(self.first_x, event.x(), self.first_y, event.y())
		if (event.buttons()&Qt.LeftButton and self.mousemode == "ztranslate"):
			self.update_matrices([0,0,(dx+dy)], "translate")
		if (event.buttons()&Qt.LeftButton and self.mousemode == "xytranslate"):
			self.update_matrices([dx,-dy,0], "translate")
		if event.buttons()&Qt.MidButton or (event.buttons()&Qt.LeftButton and self.mousemode == "scale"):
			self.update_matrices([self.scalestep*0.1*(dx+dy)], "scale")
			self.setCursor(self.scalecursor)
		self.previous_x =  event.x()
		self.previous_y =  event.y()
		self.updateSG()	
			
	def mouseReleaseEvent(self, event):
		"""
		Qt event handler. Returns the cursor to arrow unpon mouse button release
		"""
		self.setCursor(Qt.ArrowCursor)
		# Select using the selection box
		if self.toggle_render_selectedarea:
			self.pickItem()
			self.deselectArea()
			self.updateSG()
		for item in self.itemstodeselect: 
			item.setSelectedItem(False)
			if self.main_3d_inspector: self.main_3d_inspector.updateInspectorTree(item)
			self.updateSG()
			
	def wheelEvent(self, event):
		"""
		QT event handler. Scales the SG unpon wheel movement
		"""
		if event.orientation() & Qt.Vertical:
			if event.delta() > 0:
				self.update_matrices([self.scalestep], "scale")
			else:
				self.update_matrices([-self.scalestep], "scale")
			self.updateSG()
			
	def mouseDoubleClickEvent(self,event):
		print "Mouse Double Click Event"
	
	def keyPressEvent(self,event):
		print "Mouse KeyPress Event"
	
	def setMouseMode(self, mousemode):
		"""
		Sets the mouse mode, used by the inpsector
		"""
		self.mousemode = mousemode
		
	def getMouseMode(self):
		"""
		Return the mouse mode
		"""
		return self.mousemode
		
	def saveSnapShot(self, filename, format="tiff"):
		image = self.grabFrameBuffer()
		image.save(filename, format)
		
	def setZclip(self, zclip):
		""" Set the Z clipping plane """
		self.camera.setZclip(zclip)
		self.reset_camera = True
		
	def setZslice(self):
		"""
		Get a Z slice to display in the camera widget, only works for orthoganal mode
		"""
		# Getting the Z slice will have problems when using perspective viewing
		self.setAutoBufferSwap(False)
		oldnear = self.camera.getClipNear() 
		oldfar = self.camera.getClipFar()
		# We want to see the full volume data rather than a clip, so move clipping planes to BIG
		# BIG is a bit differnt for perspective and orthgraphic volumes
		if self.camera.usingortho:
			self.camera.setClipNear(-1000)
			self.camera.setClipFar(1000)
		else:
			self.camera.setClipNear(1)
			self.camera.setClipFar(1000)
		self.reset_camera = True
		current_xform = self.getTransform()
		current_xform_side = Transform({"type":"spin","Omega":90,"n1":0,"n2":1,"n3":0})*current_xform
		self.setTransform(current_xform_side)
		QtOpenGL.QGLWidget.updateGL(self)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		pixeldata = glReadPixels(1,1,self.camera.width,self.camera.height,GL_RGB,GL_UNSIGNED_BYTE)
		# Then move back
		self.setTransform(current_xform)
		self.camera.setClipNear(oldnear)
		self.camera.setClipFar(oldfar)
		self.reset_camera = True	# Reset the camera when redering the real scene
		self.setAutoBufferSwap(True)
		self.pixels = []
		self.pixels.append(0)
		self.pixels.append(0)
		self.pixels.append(self.camera.width)
		self.pixels.append(self.camera.height)
		self.pixels.append(pixeldata)
	
	def loadSession(self, tree):
		"""
		Loads a session begining 
		"""
		self.parentnodestack = [self]
		self._process_session_load(tree)
		if self.main_3d_inspector: self.main_3d_inspector.loadSG()
		
	def _process_session_load(self, line):
		"""
		Helper function to load a session. 
		This is a recursive function
		"""
		if type([]) == type(line):
			if len(line) > 1:
				for cline in line:
					self._process_session_load(cline)
				self.parentnodestack.pop()
				#if self.main_3d_inspector: self.parentitemstack.pop()
				
			else:
				# These nodes are leaves
				item3dobject = eval(line[0]["CONSTRUCTOR"])
				if line[0]["NODETYPE"] == "DataChild": # Data child need to have a parent set
					item3dobject.setParent(self.parentnodestack[-1:][0])
				self._constructitem3d(line[0], item3dobject)

		else:
			# These nodes have children to process
			if line["CONSTRUCTOR"] != "SG": 
				item3dobject = eval(line["CONSTRUCTOR"])
				self._constructitem3d(line, item3dobject)
				self.parentnodestack.append(item3dobject)
			else:
				# This is the SG, so treat special
				self.setTransform(Transform(line["TRANSFORMATION"]))
				self.setVisibleItem(line["VISIBLE"])
				self.setSelectedItem(line["SELECTED"])
				# Set up the light
				self.firstlight.setAmbient(line["AMBIENTLIGHT"][0],line["AMBIENTLIGHT"][1],line["AMBIENTLIGHT"][2],line["AMBIENTLIGHT"][3])
				self.firstlight.setPosition(line["LIGHTPOSITION"][0], line["LIGHTPOSITION"][1], line["LIGHTPOSITION"][2], line["LIGHTPOSITION"][3])
				# Set up the Camera
				self.camera.setClipNear(line["CAMERACLIP"][0])
				self.camera.setClipFar(line["CAMERACLIP"][1])
				if line["CAMERAPM"]: 
					self.camera.useOrtho(self.camera.getZclip(disregardvv=True))
				else:
					objectsize = 50
					self.camera.usePrespective(objectsize, 0.25, 60.0)
				self.cameraNeedsanUpdate()
				# Set up the utils
				self.setClearColor(line["CLEARCOLOR"][0],line["CLEARCOLOR"][1],line["CLEARCOLOR"][2])
			
	def _constructitem3d(self, datadict, item3dobject):
		"""
		Helper function for _process_session_load
		"""
		if datadict.has_key("TRANSFORMATION"):
			item3dobject.setTransform(Transform(datadict["TRANSFORMATION"]))
		if datadict.has_key("COLOR"):
			item3dobject.setAmbientColor(datadict["COLOR"][0][0], datadict["COLOR"][0][1], datadict["COLOR"][0][2], datadict["COLOR"][0][3])
			item3dobject.setDiffuseColor(datadict["COLOR"][1][0], datadict["COLOR"][1][1], datadict["COLOR"][1][2], datadict["COLOR"][1][3])
			item3dobject.setSpecularColor(datadict["COLOR"][2][0], datadict["COLOR"][2][1], datadict["COLOR"][2][2], datadict["COLOR"][2][3])
			item3dobject.setShininess(datadict["COLOR"][3])
		if datadict.has_key("ISOPARS"):
			item3dobject.wire = datadict["ISOPARS"][0]
			item3dobject.cullbackfaces = datadict["ISOPARS"][0]
			item3dobject.cullbackfaces = datadict["ISOPARS"][1]
			item3dobject.setThreshold(datadict["ISOPARS"][2])	
		item3dobject.setVisibleItem(datadict["VISIBLE"])
		item3dobject.setSelectedItem(datadict["SELECTED"])
		self.parentnodestack[-1:][0].addChild(item3dobject)
		item3dobject.setLabel(datadict["NAME"])
	
	def saveSession(self, filename):
		"""
		Save the SG as a session
		"""
		wfile = open(filename, 'wb')
		treelist = self.getTreeAsList(self)
		pickle.dump(treelist, wfile)
		wfile.close()
		
	def getTreeAsList(self, item):
		"""
		Returns the SG as a list along with all metadata. Used for saving a session
		item is the item you want to start at.
		This is a recursive function
		"""
		childlist = []
		dictionary = {"CONSTRUCTOR":item.getEvalString(),"NAME":str(item.getLabel()),"VISIBLE":item.isVisibleItem(),"SELECTED":item.isSelectedItem(),"NODETYPE":item.nodetype}
		if item.getTransform(): dictionary["TRANSFORMATION"] = item.getTransform().get_params("eman")
		# Process specific node types
		if item.nodetype == "ShapeNode" or item.nodetype == "DataChild":
			dictionary["COLOR"] = [item.ambient, item.diffuse, item.specular, item.shininess]
		if item.name == "Isosurface": dictionary["ISOPARS"] = [item.wire, item.cullbackfaces, item.isothr]
		
		# Process a SceneGraph if needed
		if item.getEvalString() == "SG":	
			dictionary["AMBIENTLIGHT"] = self.firstlight.getAmbient()
			dictionary["LIGHTPOSITION"] = self.firstlight.getPosition()
			dictionary["CAMERACLIP"] = [self.camera.getClipNear(), self.camera.getClipFar()]
			dictionary["CAMERAPM"] = self.camera.getUseOrtho()
			dictionary["CLEARCOLOR"] = self.getClearColor()
			
		# Now do the recursion to build tree
		childlist.append(dictionary)
		for ichild in item.getChildren():
			ichildlist = self.getTreeAsList(ichild)
			childlist.append(ichildlist)
		
		return childlist
		
	def cameraNeedsanUpdate(self):
		"""
		Tell the SG to restet the camera
		"""
		self.reset_camera = True
		
	def setClearColor(self, r, g, b):
		"""
		Set the background colorambient
		"""
		self.clearcolor = [r, g, b, 0.0]
		glClearColor(r, g, b, 0.0)
	
	def getClearColor(self):
		"""
		Return the clear color
		"""
		return self.clearcolor
		
	def updateSG(self):
		"""
		Update the SG
		"""
		self.update()
		if self.main_3d_inspector: self.main_3d_inspector.updateInspector()
	# Maybe add methods to control the lights

class EMLight:
	def __init__(self, light):
		"""
		@type light: GL_LIGHTX, where 0 =< X <= 8
		@param light: an OpenGL light
		The light properties are set to reasnonale defaults.
		"""
		self.light = light
		self.setAmbient(0.3, 0.3, 0.3, 1.0)		# Default ambient color is light grey
		self.setGlobalAmbient(0.0, 0.0, 0.0, 1.0)		# Default global ambient
		self.setDiffuse(1.0, 1.0, 1.0, 1.0)		# Default diffuse color is white
		self.setSpecualar(1.0, 1.0, 1.0, 1.0)		# Default specular color is white
		self.setPosition(0.0, 0.0, 1.0, 0.0)		# Defulat position is 0, 0, 1.0 and light is directional (w=0)
		if not glIsEnabled(GL_LIGHTING):
			glEnable(GL_LIGHTING)

	def setAmbient(self, r, g, b, a):
		"""
		@param r: the red component of the ambient light
		@param g: the green component of the ambient light
		@param b: the blue component of the ambient light
		@param a: the alpha component of the ambient light
		Set the ambient light color
		"""
		self.colorambient = [r, g, b, a]
		glLightfv(self.light, GL_AMBIENT, self.colorambient)
		

	def setGlobalAmbient(self, r, g, b, a):
		"""
		@param r: the red component of the ambient light
		@param g: the green component of the ambient light
		@param b: the blue component of the ambient light
		@param a: the alpha component of the ambient light
		Set the global ambient light color
		"""
		self.colorglobalambient = [r, g, b, a]
		glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.colorglobalambient)	# We want no global ambient light
		
	def setDiffuse(self, r, g, b, a):
		"""
		@param r: the red component of the diffuse and specular light
		@param g: the green component of the diffuse and specular light
		@param b: the blue component of the diffuse and specular light
		@param a: the alpha component of the diffuse and specular light
		Set the diffuse light color
		"""
		self.colordiffuse = [r, g, b, a]
		glLightfv(self.light, GL_DIFFUSE, self.colordiffuse)
		
	def setSpecualar(self, r, g, b, a):
		"""
		@param r: the red component of the diffuse and specular light
		@param g: the green component of the diffuse and specular light
		@param b: the blue component of the diffuse and specular light
		@param a: the alpha component of the diffuse and specular light
		Set the specualr light color
		"""
		self.colorspecular = [r, g, b, a]
		glLightfv(self.light, GL_SPECULAR, self.colorspecular)

	def setPosition(self, x, y, z, w):
		"""
		@param x: The x component of the light position
		@param y: The y component of the light position
		@param z: The z component of the light position
		@param w: The w component of the light position
		Set the light position, in gomogenious corrds
		"""
		self.position = [x, y, z, w]
		glLightfv(self.light, GL_POSITION, self.position)

	def getAmbient(self):
		"""
		Return the ambient lighting
		"""
		return self.colorambient
	
	def getGlobalAmbient(self):
		"""
		Return the global ambient color
		"""
		return self.colorglobalambient
		
	def getDiffuse(self):
		"""
		Return the diffuse lighting
		"""
		return self.colordiffuse
		
	def getSpecular(self):
		"""
		Return the specular lighting
		"""
		returnself.colorspecular
	
	def getPosition(self):
		"""
		Return the light position
		"""
		return self.position
		
	def enableLighting(self):
		"""
		Enables this light
		"""
		if not glIsEnabled(self.light):
			glEnable(self.light)

	def disableLighting(self):
		"""
		Disables this light
		"""
		if glIsEnabled(self.light):
			glDisable(self.light)
			
	def updateGLlighting(self):
		"""
		With open GL, Stupid is a stupid does :)
		Sometimes we need to re-issue glLighting commands to get GLto execute them, I don't know why this happens......
		"""
		self.setAmbient(self.colorambient[0], self.colorambient[1], self.colorambient[2], self.colorambient[3])
		self.setGlobalAmbient(self.colorglobalambient[0], self.colorglobalambient[1], self.colorglobalambient[2], self.colorglobalambient[3])
		
class EMCamera:
	"""Implmentation of the camera"""
	def __init__(self, near, far, usingortho=True, fovy=60.0, boundingbox=50.0, screenfraction=0.5):
		"""
		@param fovy: The field of view angle
		@param near: The volume view near position
		@param far: The volume view far position
		@param usingortho: Use orthographic projection
		@param boundingbox: The dimension of the bounding for the object to be rendered
		@param screenfraction: The fraction of the screen height to occupy
		"""
		self.far = far
		self.near = near
		self.fovy = fovy
		zclip = (self.near-self.far)/2.0	# Puts things in the center of the viewing volume
		if usingortho:
			self.useOrtho(zclip)
		else:
			self.usePrespective(boundingbox, screenfraction, fovy)

	def update(self, width=None, height=None):
		"""
		@param width: The width of the window in pixels
		@param height: The height of the window in pixels
		updates the camera and viewport after windowresize
		"""
		if width: self.width = width
		if height: self.height = height
		if self.usingortho:
			glViewport(0,0,self.width,self.height)
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			self.setOrthoProjectionMatrix()
			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()
			self.setCameraPosition()
		else:
			# This may need some work to get it to behave
			glViewport(0,0,self.width,self.height)
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			self.setPerspectiveProjectionMatrix()
			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()
			self.setCameraPosition()
	
	def setCameraPosition(self, sfactor=1):
		"""
		Set the default camera position
		"""
		glTranslate(0,0,sfactor*self.getZclip())
		
	def setProjectionMatrix(self):
		"""
		Set the projection matrix
		"""
		if self.usingortho:
			self.setOrthoProjectionMatrix()
		else:
			self.setPerspectiveProjectionMatrix()
			
	def setOrthoProjectionMatrix(self):
		"""
		Set the orthographic projection matrix. Volume view origin (0,0) is center of screen
		"""
		glOrtho(-self.width/2, self.width/2, -self.height/2, self.height/2, self.near, self.far)
		
	def setPerspectiveProjectionMatrix(self):
		"""
		Set the perspective projection matrix. Volume view origin (0,0) is center of screen
		"""
		GLU.gluPerspective(self.fovy, (float(self.width)/float(self.height)), self.near, self.far)
			
	def usePrespective(self, boundingbox, screenfraction, fovy=60.0):
		""" 
		@param boundingbox: The dimension of the bounding for the object to be rendered
		@param screenfraction: The fraction of the screen height to occupy
		Changes projection matrix to perspective
		"""
		self.fovy = fovy
		self.perspective_z = -(boundingbox*2/screenfraction)/(2*math.tan(math.radians(self.fovy/2)))  + boundingbox
		self.usingortho = False
		
	def useOrtho(self, zclip):
		"""
		Changes projection matrix to orthographic
		"""
		self.usingortho = True
		self.zclip = zclip
		
	def getUseOrtho(self):
		"""
		Returns the projectrion state
		"""
		return self.usingortho
		
	def setClipFar(self, far):
		"""
		Set the far aspect of the viewing volume
		"""
		self.far = far

	def setClipNear(self, near):
		"""
		Set the near aspect of the viewing volume
		"""
		self.near = near

	def getClipNear(self):
		"""
		Get the near clipping plane
		"""
		return self.near
		
	def getClipFar(self):
		"""
		Get the far clipping plane
		"""
		return self.far
		
	def setFovy(self, fovy):
		"""
		Set the field of view angle aspect of the viewing volume
		"""
		self.fovy = fovy
	
	def getFovy(self):
		""" Return FOVY """
		return self.fovy
		
	def getHeight(self):
		""" Get the viewport height """
		return self.height
	
	def getWidth(self):
		""" Get the viewport width """
		return self.width
		
	def getZclip(self, disregardvv=False):
		""" Get the zclip """
		if self.usingortho or disregardvv:
			return self.zclip
		else:
			return self.perspective_z
			
	def setZclip(self, clip):
		""" Set the Z clip """
		if self.usingortho:
			self.zclip = clip
		else:
			self.perspective_z = clip
	# Maybe other methods to control the camera

###################################### Inspector Code #########################################################################################

class EMInspector3D(QtGui.QWidget):
	def __init__(self, scenegraph):
		"""
		The inspector for the 3D widget. The inspector is a strict observer of the SceneGraph, and is updated by calling update inspector
		"""
		QtGui.QWidget.__init__(self)
		self.scenegraph = scenegraph
		self.mintreewidth = 200		# minimum width of the tree
		self.mincontrolwidth = 250
		
		vbox = QtGui.QVBoxLayout(self)
		self.inspectortab = QtGui.QTabWidget()
		self.inspectortab.addTab(self.getTreeWidget(), "Tree View")
		self.inspectortab.addTab(self.getLightsWidget(), "Lights")
		self.inspectortab.addTab(self.getCameraWidget(), "Camera")
		self.inspectortab.addTab(self.getUtilsWidget(), "Utils")
		toolframe = QtGui.QFrame()
		toolframe.setFrameShape(QtGui.QFrame.StyledPanel)
		toolframe.setLayout(self._get_toolbox_layout())
		vbox.addWidget(self.inspectortab)
		vbox.addWidget(toolframe)
		
		QtCore.QObject.connect(self.inspectortab, QtCore.SIGNAL("currentChanged(int)"), self._on_load_camera)
		
		self.setLayout(vbox)
		self.updateGeometry()
		
	def _recursiveAdd(self, parentitem, parentnode):
		"""
		Helper function to laod the SG
		"""
		for child in parentnode.getChildren():
			if not child.getLabel(): child.setLabel(child.name)
			addeditem = self.addTreeNode(child.getLabel(), child, parentitem)
			self._recursiveAdd(addeditem, child)
		# Expand the data items
		if parentitem.childCount() > 0: parentitem.setExpanded(True)
		
	def loadSG(self):
		"""
		Load the SG
		"""
		rootitem = self.addTreeNode("All Objects", self.scenegraph)
		self._recursiveAdd(rootitem, self.scenegraph)
			
	
	def getTreeWidget(self):
		"""
		This returns the treeview-control panel widget
		"""
		widget = QtGui.QWidget()
		hbox = QtGui.QHBoxLayout(widget)
		treeframe = QtGui.QFrame()
		treeframe.setFrameShape(QtGui.QFrame.StyledPanel)
		treeframe.setLayout(self._get_tree_layout(widget))
		treeframe.setMinimumWidth(self.mintreewidth)
		hbox.addWidget(treeframe)
		self.stacked_widget = QtGui.QStackedWidget()
		self.stacked_widget.setFrameShape(QtGui.QFrame.StyledPanel)
		hbox.addWidget(self.stacked_widget)
		widget.setLayout(hbox)
		
		return widget
		
	def _get_tree_layout(self, parent):
		"""
		Returns the tree layout
		"""
		tvbox = QtGui.QVBoxLayout()
		self.tree_widget = EMQTreeWidget(parent)
		self.tree_widget.setHeaderLabel("Choose a item")
		tvbox.addWidget(self.tree_widget)
		self.tree_node_button_add = QtGui.QPushButton("Add Node")
		self.tree_node_button_remove = QtGui.QPushButton("Remove Node")
		tvbox.addWidget(self.tree_node_button_add)
		tvbox.addWidget(self.tree_node_button_remove)
		
		QtCore.QObject.connect(self.tree_widget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self._tree_widget_click)
		QtCore.QObject.connect(self.tree_widget, QtCore.SIGNAL("visibleItem(QTreeWidgetItem*)"), self._tree_widget_visible)
		QtCore.QObject.connect(self.tree_widget, QtCore.SIGNAL("editItem(QTreeWidgetItem*)"), self._tree_widget_edit)
		QtCore.QObject.connect(self.tree_node_button_remove, QtCore.SIGNAL("clicked()"), self._tree_widget_remove)
		QtCore.QObject.connect(self.tree_node_button_add, QtCore.SIGNAL("clicked()"), self._on_add_button)
		
		return tvbox
	
	def updateInspectorTree(self, selecteditem):
		"""
		Update the inspector tree_item
		"""
		if selecteditem.EMQTreeWidgetItem:
			selecteditem.EMQTreeWidgetItem.setSelectionStateBox()
			self.tree_widget.setCurrentItem(selecteditem.EMQTreeWidgetItem)
		try:
			self.stacked_widget.setCurrentWidget(selecteditem.getItemInspector())
			self.tree_widget.setCurrentItem(selecteditem.getItemInspector().treeitem)
		except:
			pass
		self.ensureUniqueTreeLevelSelection(selecteditem)
		
	def ensureUniqueTreeLevelSelection(self, item):
		"""
		Make sure that we don't select both an ancestor and child at the same time
		"""
		for ancestor in item.getSelectedAncestorNodes():
			if ancestor.EMQTreeWidgetItem:			# Not al ancestors are listed on the inspector tree (such as a data node)
				ancestor.EMQTreeWidgetItem.setSelectionState(False)
		for child in item.getAllSelectedNodes()[1:]: 	# Lop the node itself off
			child.EMQTreeWidgetItem.setSelectionState(False)
			
	def _get_toolbox_layout(self):
		tvbox = QtGui.QHBoxLayout()
		font = QtGui.QFont()
		font.setBold(True)
		toollabel = QtGui.QLabel("Tools")
		toollabel.setFont(font)
		self.rotatetool = EMANToolButton()
		self.rotatetool.setIcon(QtGui.QIcon(QtGui.QPixmap(rotateicon)))
		self.rotatetool.setToolTip("Rotate X/Y\nMouse: Right 'n' drag")
		self.translatetool =EMANToolButton()
		self.translatetool.setIcon(QtGui.QIcon(QtGui.QPixmap(crosshairsicon)))
		self.translatetool.setToolTip("Translate X/Y\nMouse: Left 'n' drag")
		self.ztranslate = EMANToolButton()
		self.ztranslate.setIcon(QtGui.QIcon(QtGui.QPixmap(ztransicon)))
		self.ztranslate.setToolTip("Translate Z")
		self.scaletool = EMANToolButton()
		self.scaletool.setIcon(QtGui.QIcon(QtGui.QPixmap(scaleicon)))
		self.scaletool.setToolTip("Scale\nMouse: Middle 'n' drag")
		self.selectiontool = EMANToolButton()
		self.selectiontool.setIcon(QtGui.QIcon(QtGui.QPixmap(selectionicon)))
		self.selectiontool.setToolTip("Select objects\nMouse: Left 'n' drag\nMultiple = + Shift")
		self.multiselectiontool = EMANToolButton()
		self.multiselectiontool.setIcon(QtGui.QIcon(QtGui.QPixmap(multiselectoricon)))
		self.multiselectiontool.setToolTip("Select multiple objects\nMouse: Left 'n' drag")
		self.cubetool = EMANToolButton()
		self.cubetool.setIcon(QtGui.QIcon(QtGui.QPixmap(cubeicon)))
		self.cubetool.setToolTip("Insert Cube")
		self.spheretool = EMANToolButton()
		self.spheretool.setIcon(QtGui.QIcon(QtGui.QPixmap(sphereicon)))
		self.spheretool.setToolTip("Insert Sphere")
		self.cylindertool = EMANToolButton()
		self.cylindertool.setIcon(QtGui.QIcon(QtGui.QPixmap(cylindericon)))
		self.cylindertool.setToolTip("Insert Cylinder")
		self.texttool = EMANToolButton()
		self.texttool.setIcon(QtGui.QIcon(QtGui.QPixmap(texticon)))
		self.texttool.setToolTip("Insert Text")
		self.isotool = EMANToolButton()
		self.isotool.setIcon(QtGui.QIcon(QtGui.QPixmap(isosurfaceicon)))
		self.isotool.setToolTip("Insert IsoSurface")
		
		tvbox.addWidget(toollabel)
		tvbox.addWidget(self.selectiontool)
		tvbox.addWidget(self.multiselectiontool)
		tvbox.addWidget(self.translatetool)
		tvbox.addWidget(self.ztranslate)
		tvbox.addWidget(self.rotatetool)
		tvbox.addWidget(self.scaletool)

		tvbox.addWidget(self.cubetool)
		tvbox.addWidget(self.spheretool)
		tvbox.addWidget(self.cylindertool)
		tvbox.addWidget(self.texttool)
		tvbox.addWidget(self.isotool)
		tvbox.setAlignment(QtCore.Qt.AlignLeft)
		
		QtCore.QObject.connect(self.rotatetool, QtCore.SIGNAL("clicked(int)"), self._rotatetool_clicked)
		QtCore.QObject.connect(self.translatetool, QtCore.SIGNAL("clicked(int)"), self._transtool_clicked)
		QtCore.QObject.connect(self.ztranslate, QtCore.SIGNAL("clicked(int)"), self._ztranstool_clicked)
		QtCore.QObject.connect(self.scaletool, QtCore.SIGNAL("clicked(int)"), self._scaletool_clicked)
		QtCore.QObject.connect(self.selectiontool, QtCore.SIGNAL("clicked(int)"), self._seltool_clicked)
		QtCore.QObject.connect(self.multiselectiontool, QtCore.SIGNAL("clicked(int)"), self._multiseltool_clicked)
		QtCore.QObject.connect(self.cubetool, QtCore.SIGNAL("clicked(int)"), self._cubetool_clicked)
		QtCore.QObject.connect(self.spheretool, QtCore.SIGNAL("clicked(int)"), self._spheretool_clicked)
		QtCore.QObject.connect(self.cylindertool, QtCore.SIGNAL("clicked(int)"), self._cylindertool_clicked)
		QtCore.QObject.connect(self.texttool, QtCore.SIGNAL("clicked(int)"), self._texttool_clicked)
		QtCore.QObject.connect(self.isotool, QtCore.SIGNAL("clicked(int)"), self._isotool_clicked)
		
		# Set the default tool
		self.selectiontool.setDown(True)
		
		return tvbox
	
	def _rotatetool_clicked(self, state):
		self.scenegraph.setMouseMode("rotate")
		
	def _transtool_clicked(self, state):
		self.scenegraph.setMouseMode("xytranslate")
		
	def _ztranstool_clicked(self, state):
		self.scenegraph.setMouseMode("ztranslate")
		
	def _scaletool_clicked(self, state):
		self.scenegraph.setMouseMode("scale")
	
	def _seltool_clicked(self, state):
		self.scenegraph.setMouseMode("selection")
		
	def _multiseltool_clicked(self, state):
		self.scenegraph.setMouseMode("multiselection")
	
	def _cubetool_clicked(self, state):
		self.scenegraph.setMouseMode("cube")
		
	def _spheretool_clicked(self, state):
		self.scenegraph.setMouseMode("sphere")
		
	def _cylindertool_clicked(self, state):
		self.scenegraph.setMouseMode("cylinder")
		
	def _texttool_clicked(self, state):
		self.scenegraph.setMouseMode("text")
		
	def _isotool_clicked(self, state):
		self.scenegraph.setMouseMode("isosurface")
				
		
	def addTreeNode(self, name, item3d, parentitem=None, insertionindex=-1):
		"""
		Add a node (item3d) to the TreeWidget if not parent node, otherwise add a child to parent node
		We need to get a GUI for the treeitem. The treeitem and the GUI need know each other so they can talk
		The Treeitem also needs to know the node, so it can talk to the node.
		You can think of this as a three way conversation (the alterative it to use a mediator, but that is not worth it w/ only three players)
		"""
		tree_item = EMQTreeWidgetItem(QtCore.QStringList(name), item3d, parentitem)	# Make a QTreeItem widget, and let the TreeItem talk to the scenegraph node and its GUI
		item3d.setEMQTreeWidgetItem(tree_item)				# Reference to the EMQTreeWidgetItem
		item_inspector = item3d.getItemInspector()				# Get the node GUI controls 
		item_inspector.setInspector(self)					# Associate the item GUI with the inspector
		self.stacked_widget.addWidget(item_inspector)			# Add a widget to the stack
		item3d.setLabel(name)						# Set the label
		# Set icon status
		tree_item.setSelectionStateBox()
		# Set parent if one exists	
		if not parentitem:
			self.tree_widget.insertTopLevelItem(0, tree_item)
		else:
			if insertionindex >= 0:
				parentitem.insertChild(insertionindex, tree_item)
			else:
				parentitem.addChild(tree_item)
		return tree_item
	
	def removeTreeNode(self, parentitem, childindex):
		# I am using the parent item rather than the item itself b/c the stupid widget has no , remove self function...
		# Remove both the QTreeWidgetItem and the widget from the WidgetStack, otherwise we'll get memory leaks 
		if parentitem.child(childindex).item3d(): self.stacked_widget.removeWidget(parentitem.child(childindex).item3d().getItemInspector())
		parentitem.takeChild(childindex)
	
	def insertNewNode(self, node_name, insertion_node):
		"""
		Insert a node at the highlighted location
		"""
		currentitem = self.tree_widget.currentItem()
		if currentitem:
			itemparentnode = currentitem.parent
			if itemparentnode:
				thisnode_index = itemparentnode().indexOfChild(currentitem)
				addeditem = self.addTreeNode(node_name, insertion_node, parentitem=itemparentnode(), insertionindex=(thisnode_index+1))
				self.tree_widget.setCurrentItem(addeditem)
				self._tree_widget_click(addeditem, 0)
				return [itemparentnode().item3d(), thisnode_index]
		# Otherwise add the node to the Root
		addeditem = self.addTreeNode(node_name, insertion_node, parentitem=self.tree_widget.topLevelItem(0))
		self.tree_widget.setCurrentItem(addeditem)
		self._tree_widget_click(addeditem, 0)
		
		return None
		
	def _tree_widget_click(self, item, col):
		"""
		When a user clicks on the selection tree check box
		"""
		self.stacked_widget.setCurrentWidget(item.item3d().getItemInspector())
		item.setSelectionState(item.checkState(0))
		# This code is to prevent both decendents and childer from being selected....
		self.ensureUniqueTreeLevelSelection(item.item3d())
		self.updateSceneGraph()
		
	def _tree_widget_visible(self, item):
		"""
		When a user clicks on the visible icon
		"""
		item.toggleVisibleState()
		self.updateSceneGraph()
	
	def _tree_widget_edit(self):
		"""
		When a use middle clicks
		"""
		nodedialog = NodeEditDialog(self, self.tree_widget.currentItem())
		nodedialog.exec_()
		self.activateWindow()
	
	def _on_add_button(self):
		nodedialog =  NodeDialog(self, self.tree_widget.currentItem())
		nodedialog.exec_()
		self.activateWindow()
		
	def _tree_widget_remove(self):
		"""
		When a use wants to remove a node_name
		"""
		item = self.tree_widget.currentItem()
		if item.parent:
			self.removeTreeNode(item.parent(), item.parent().indexOfChild(item)) 
			item.parent().item3d().removeChild(item.item3d())
			self.updateSceneGraph()
		else:
			print "Error cannot remove root node!!"
		
	def getLightsWidget(self):
		"""
		Returns the lights control widget
		"""
		self.lighttab_open = False
		lwidget = QtGui.QWidget()
		lvbox = QtGui.QVBoxLayout()
		lightslabel = QtGui.QLabel("Lights", lwidget)
		lightslabel.setAlignment(QtCore.Qt.AlignCenter)
		lightslabel.setMaximumHeight(30.0)
		font = QtGui.QFont()
		font.setBold(True)
		lightslabel.setFont(font)
		lvbox.addWidget(lightslabel)
		self.lightwidget = EMLightControls(GL_LIGHT1)
		positionlabel = QtGui.QLabel("Position", lwidget)
		positionlabel.setMaximumHeight(20.0)
		positionlabel.setAlignment(QtCore.Qt.AlignCenter)
		valslidersplitter = QtGui.QFrame()
		valslidersplitter.setFrameShape(QtGui.QFrame.StyledPanel)
		valslidersplitter.setMaximumHeight(80)
		valvbox = QtGui.QVBoxLayout()
		self.hvalslider = ValSlider(lwidget,(0.0,360.0),"Horizontal")
		self.vvalslider = ValSlider(lwidget,(0.0,360.0),"Vertical")
		valvbox.addWidget(self.hvalslider)
		valvbox.addWidget(self.vvalslider)
		valslidersplitter.setLayout(valvbox)
		lvbox.addWidget(self.lightwidget)
		lvbox.addWidget(positionlabel)
		lvbox.addWidget(valslidersplitter)
		self.ambientlighting = ValSlider(lwidget,(0.0,1.0),"Ambient Lighting")
		self.ambientlighting.setMaximumHeight(30)
		lvbox.addWidget(self.ambientlighting)
		lwidget.setLayout(lvbox)
		
		QtCore.QObject.connect(self.lightwidget, QtCore.SIGNAL("lightPositionMoved"), self._light_position_moved)
		QtCore.QObject.connect(self.hvalslider,QtCore.SIGNAL("valueChanged"),self._on_light_slider)
		QtCore.QObject.connect(self.vvalslider,QtCore.SIGNAL("valueChanged"),self._on_light_slider)
		QtCore.QObject.connect(self.ambientlighting,QtCore.SIGNAL("valueChanged"),self._on_light_ambient)

		return lwidget
	
	def _light_position_moved(self, position): 
		self.scenegraph.firstlight.setPosition(position[0], position[1], position[2], position[3])
		self.scenegraph.updateSG()
	
	def _on_light_slider(self, value):
		self.lightwidget.setAngularPosition(self.hvalslider.getValue(), self.vvalslider.getValue())
		position = self.lightwidget.getPosition()
		self.scenegraph.firstlight.setPosition(position[0], position[1], position[2], position[3])
		self.scenegraph.update()
	
	def _on_light_ambient(self):
		ambient = self.ambientlighting.getValue()
		self.scenegraph.firstlight.setAmbient(ambient, ambient, ambient, 1.0)
		self.scenegraph.update()
	
	def getCameraWidget(self):
		"""
		Returns the camera control widget
		"""
		self.cameratab_open = False
		cwidget = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		self.camerawidget = CameraControls(scenegraph=self.scenegraph)
		grid.addWidget(self.camerawidget, 0, 0, 1, 2)
		nlabel = QtGui.QLabel("Near clipping plane", cwidget)
		nlabel.setMaximumHeight(30.0)
		nlabel.setAlignment(QtCore.Qt.AlignCenter)
		self.near = EMSpinWidget(self.scenegraph.camera.getClipNear(), 1.0)
		self.near.setToolTip("In the Window above:\nClick 'n' drag, near the near clipping, to move near clipping plane")
		self.near.setMaximumHeight(40.0)
		grid.addWidget(nlabel, 1, 0)
		grid.addWidget(self.near ,1, 1)
		flabel = QtGui.QLabel("Far clipping plane", cwidget)
		flabel.setMaximumHeight(30.0)
		flabel.setAlignment(QtCore.Qt.AlignCenter)
		self.far = EMSpinWidget(self.scenegraph.camera.getClipFar(), 1.0)
		self.far.setToolTip("In the Window above:\nClick 'n' drag, near the far clipping, to move far clipping plane")
		self.far.setMaximumHeight(40.0)
		grid.addWidget(flabel, 2, 0)
		grid.addWidget(self.far, 2, 1)
		frame = QtGui.QFrame()
		frame.setMaximumHeight(40.0)
		frame.setFrameShape(QtGui.QFrame.StyledPanel)
		hbox = QtGui.QHBoxLayout()
		vvlabel = QtGui.QLabel("Viewing Volume")
		self.orthoradio = QtGui.QRadioButton("Orthographic")
		self.perspectiveradio = QtGui.QRadioButton("Perspective")
		hbox.addWidget(vvlabel)
		hbox.addWidget(self.orthoradio)
		hbox.addWidget(self.perspectiveradio)
		frame.setLayout(hbox)
		grid.addWidget(frame, 3, 0,1,2)
		cwidget.setLayout(grid)

		QtCore.QObject.connect(self.near,QtCore.SIGNAL("valueChanged(int)"),self._on_near)
		QtCore.QObject.connect(self.far,QtCore.SIGNAL("valueChanged(int)"),self._on_far)
		QtCore.QObject.connect(self.camerawidget,QtCore.SIGNAL("nearMoved(int)"),self._on_near_move)
		QtCore.QObject.connect(self.camerawidget,QtCore.SIGNAL("farMoved(int)"),self._on_far_move)
		QtCore.QObject.connect(self.orthoradio,QtCore.SIGNAL("clicked()"),self._on_radio_click)
		QtCore.QObject.connect(self.perspectiveradio,QtCore.SIGNAL("clicked()"),self._on_radio_click)
		
		return cwidget
	
	def _on_near(self, value):
		if not self.scenegraph.camera.usingortho and value <= 0:
			return
		if self.scenegraph.camera.getClipFar() > value:
			self.scenegraph.camera.setClipNear(value)
			self.scenegraph.updateSG()
	
	def _on_far(self, value):
		if value > self.scenegraph.camera.getClipNear():
			self.scenegraph.camera.setClipFar(value)
			self.scenegraph.updateSG()
		
	def _on_near_move(self, movement):
		value = self.scenegraph.camera.getClipNear() + movement
		if not self.scenegraph.camera.usingortho and value <= 0:
			return
		if self.scenegraph.camera.getClipFar() > value:
			self.scenegraph.camera.setClipNear(value)
			self.scenegraph.updateSG()
		
	def _on_far_move(self, movement):
		value = self.scenegraph.camera.getClipFar() + movement
		if value > self.scenegraph.camera.getClipNear():
			self.scenegraph.camera.setClipFar(value)
			self.scenegraph.updateSG()
		
	def _on_load_camera(self, idx):
		"""
		Load the SG Z slice and only update widgets that are open
		"""
		if idx == 2: # '2' is the camera tab
			self.scenegraph.setZslice()
			self.cameratab_open = True
			self.updateInspector()
			return
		if idx == 1: # '1' is the  light tab
			self.lighttab_open = True
			self.updateInspector()
			return
			
		self.cameratab_open = False
		self.lighttab_open = False
			
	def _get_vv_state(self):
		"""
		Get the viewing volume of the camera
		"""
		if self.scenegraph.camera.usingortho: 
			self.orthoradio.setChecked(True)
		else:
			self.perspectiveradio.setChecked(True)
	
	def _on_radio_click(self):
		"""
		set the viewing volume. objectsize is the size of the bounding box of the largest displayed object
		"""
		objectsize = 50
		if self.orthoradio.isChecked(): self.scenegraph.camera.useOrtho(self.scenegraph.camera.getZclip(disregardvv=True))
		if self.perspectiveradio.isChecked(): self.scenegraph.camera.usePrespective(objectsize, 0.25, 60.0)
		self.scenegraph.updateSG()
		
	def getUtilsWidget(self):
		"""
		Return the utilites widget
		"""
		uwidget = QtGui.QWidget()
		uvbox = QtGui.QVBoxLayout()
		frame = QtGui.QFrame()
		frame.setFrameShape(QtGui.QFrame.StyledPanel)
		fvbox = QtGui.QHBoxLayout()
		backgroundcolor_label = QtGui.QLabel("Background Color", frame)
		self.backgroundcolor = EMQTColorWidget(parent=frame)
		fvbox.addWidget(backgroundcolor_label)
		fvbox.addWidget(self.backgroundcolor)
		fvbox.setAlignment(QtCore.Qt.AlignCenter)
		frame.setLayout(fvbox)
		uvbox.addWidget(frame)
		self.opensession_button = QtGui.QPushButton("Open Session")
		self.savesession_button = QtGui.QPushButton("Save Session")
		self.savebutton = QtGui.QPushButton("Save Image Snapshot")
		uvbox.addWidget(self.opensession_button)
		uvbox.addWidget(self.savesession_button)
		uvbox.addWidget(self.savebutton)
		uwidget.setLayout(uvbox)
		
		QtCore.QObject.connect(self.backgroundcolor,QtCore.SIGNAL("newcolor(QColor)"),self._on_bg_color)
		QtCore.QObject.connect(self.savebutton, QtCore.SIGNAL("clicked()"),self._on_save)
		QtCore.QObject.connect(self.savesession_button, QtCore.SIGNAL("clicked()"),self._on_save_session)
		QtCore.QObject.connect(self.opensession_button, QtCore.SIGNAL("clicked()"),self._on_open_session)
		
		return uwidget
				
	def _on_open_session(self):
		"""
		Open a session
		"""
		# Open the file
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Session', os.getcwd(), "*.eman")
		self.loadSession(filename)
	
	def loadSession(self, filename):
		"""
		Load a session
		"""
		rfile = open(filename, 'rb')
		try:
			tree = pickle.load(rfile)
		except:
			print "ERROR!!! Couldn't load the session file"
			rfile.close()
			return	
		rfile.close()
		# Clear the current tree
		self.tree_widget.topLevelItem(0).removeAllChildren(self)
		self.tree_widget.takeTopLevelItem(0)
		# Load the new data
		self.scenegraph.makeCurrent()
		self.scenegraph.loadSession(tree)
		self.updateSceneGraph()
		
	def _on_save_session(self):
		"""
		Return a list of all the child items (actually a tree of sorts)
		"""
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Session', os.getcwd(), "*.eman")
		if filename: # if we cancel
			self.scenegraph.saveSession(filename)

	def _on_save(self):
		"""
		Save a snapshot of the scene
		"""
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Image', os.getcwd(), "*.tiff")
		if filename: # if we cancel
			self.scenegraph.saveSnapShot(filename)
			print "Saved %s to disk"%os.path.basename(str(filename))
	
	def _on_bg_color(self, color):
		rgb = color.getRgb()
		self.scenegraph.makeCurrent()
		self.scenegraph.setClearColor(float(rgb[0])/255.0, float(rgb[1])/255.0, float(rgb[2])/255.0)
		self.updateSceneGraph()
		
	def updateInspector(self):
		"""
		Update Inspector,is called whenever the scence changes
		"""
		#tool buttons
		if self.scenegraph.getMouseMode() == "selection": self.selectiontool.setDown(True)
		if self.scenegraph.getMouseMode() == "multiselection": self.multiselectiontool.setDown(True)
		if self.scenegraph.getMouseMode() == "rotate": self.rotatetool.setDown(True)
		if self.scenegraph.getMouseMode() == "xytranslate": self.translatetool.setDown(True)
		if self.scenegraph.getMouseMode() == "ztranslate": self.ztranslate.setDown(True)
		if self.scenegraph.getMouseMode() == "scale": self.scaletool.setDown(True)
		if self.scenegraph.getMouseMode() == "cube": self.scaletool.setDown(True)
		if self.scenegraph.getMouseMode() == "sphere": self.scaletool.setDown(True)
		if self.scenegraph.getMouseMode() == "cylinder": self.scaletool.setDown(True)
		# Lights
		if self.lighttab_open:
			angularposition = self.lightwidget.getAngularPosition()
			self.hvalslider.setValue(angularposition[0], quiet=1)
			self.vvalslider.setValue(angularposition[1], quiet=1)
			al = self.scenegraph.firstlight.getAmbient()
			ambient = (al[0] + al[1] + al[2])/3
			self.ambientlighting.setValue(ambient, quiet=1)
		# camera
		if self.cameratab_open:
			self.near.setValue(self.scenegraph.camera.getClipNear(), quiet=1)
			self.far.setValue(self.scenegraph.camera.getClipFar(), quiet=1)
			self._get_vv_state()
			self.scenegraph.setZslice()
			self.camerawidget.updateWidget()
		# utils
		self.backgroundcolor.setColor(QtGui.QColor(255*self.scenegraph.clearcolor[0],255*self.scenegraph.clearcolor[1],255*self.scenegraph.clearcolor[2]))
			
	def updateSceneGraph(self):
		""" 
		Updates SG, in the near future this will be improved to allow for slow operations
		"""
		self.scenegraph.updateSG()

class EMQTreeWidget(QtGui.QTreeWidget):
	"""
	Subclassing the QTreeWidget to enable is_visible toggling
	"""
	def __init__(self, parent=None):
		QtGui.QTreeWidget.__init__(self, parent)
			
	def mousePressEvent(self, e):
		QtGui.QTreeWidget.mousePressEvent(self, e)
		if e.button()==Qt.RightButton:
			self.emit(QtCore.SIGNAL("visibleItem(QTreeWidgetItem*)"), self.currentItem())
		if e.button()==Qt.MidButton:
			self.emit(QtCore.SIGNAL("editItem(QTreeWidgetItem*)"), self.currentItem())
			
			
class EMQTreeWidgetItem(QtGui.QTreeWidgetItem):
	"""
	Subclass of QTreeWidgetItem
	adds functionality
	"""
	def __init__(self, qstring, item3d, parentnode):
		QtGui.QTreeWidgetItem.__init__(self, qstring)
		self.name = qstring.join('')
		self.item3d = weakref.ref(item3d)
		if parentnode: self.parent = weakref.ref(parentnode)
		else: self.parent = None
		self.setCheckState(0, QtCore.Qt.Unchecked)
		self.visible = QtGui.QIcon(QtGui.QPixmap(visibleicon))
		self.invisible = QtGui.QIcon(QtGui.QPixmap(invisibleicon))
		self.getVisibleState()
		self.setToolTip(0, 'Click on the checkbox to select\nMiddle click to edit\nRight click to toogle visible')
	
	def setSelectionState(self, state):
		""" 
		Toogle selection state on and off
		"""
		if state == QtCore.Qt.Checked:
			self.item3d().setSelectedItem(True)
		else:
			self.item3d().setSelectedItem(False)
		self.setSelectionStateBox() # set state of TreeItemwidget
		
	def toggleVisibleState(self):
		self.item3d().setVisibleItem(not self.item3d().isVisibleItem())
		self.getVisibleState()
		
	def getVisibleState(self):
		"""
		Toogle the visble state
		"""
		if self.item3d().isVisibleItem():
			self.setIcon(0, self.visible)
		else:
			self.setIcon(0, self.invisible)
	
	def setSelectionStateBox(self):
		"""
		Set the selection state icon
		"""
		if self.item3d().isSelectedItem():
			self.setCheckState(0, QtCore.Qt.Checked)
		else:
			self.setCheckState(0, QtCore.Qt.Unchecked)
	
	def removeAllChildren(self, inspector):
		"""
		Remove all children from the SG
		"""
		for i in xrange(self.childCount()):
			self.child(0).removeAllChildren(inspector)
			self.item3d().removeChild(self.child(0).item3d())
			inspector.removeTreeNode(self, 0) 

class NodeEditDialog(QtGui.QDialog):
	"""
	A dialog for editing the node
	"""
	def __init__(self, inspector, item):
		QtGui.QDialog.__init__(self)
		self.item = item
		self.inspector = weakref.ref(inspector)
		grid = QtGui.QGridLayout(self)
		label = QtGui.QLabel("Node Name")
		self.nodename = QtGui.QLineEdit()
		grid.addWidget(label, 0, 0, 1, 2)
		grid.addWidget(self.nodename, 1, 0, 1, 2)
		self.ok_button = QtGui.QPushButton("Ok")
		self.cancel_button = QtGui.QPushButton("Cancel")
		grid.addWidget(self.ok_button, 2, 0, 1, 1)
		grid.addWidget(self.cancel_button, 2, 1, 1, 1)
		self.setLayout(grid)
		
		self.connect(self.ok_button, QtCore.SIGNAL('clicked()'), self._on_ok)
		self.connect(self.cancel_button, QtCore.SIGNAL('clicked()'), self._on_cancel)
	
	def _on_ok(self):
		self.item.item3d().setLabel(self.nodename.text())
		self.item.setText(0, self.nodename.text())
		self.done(0)
		
	def _on_cancel(self):
		self.done(1)
		
class NodeDialog(QtGui.QDialog):
	"""
	Generate a dialog to add or remove node. If reome is chosen 'item' node is removed
	If add node is chosen, a node is inserted just below this node.
	"""
	def __init__(self, inspector, item):
		QtGui.QDialog.__init__(self)
		self.item = item
		self.inspector = weakref.ref(inspector)
		self.setWindowTitle('Node Controler')
		#grid = QtGui.QGridLayout()
		vbox = QtGui.QVBoxLayout(self)
		# Stuff within the frame
		frame = QtGui.QFrame()
		frame.setFrameStyle(QtGui.QFrame.StyledPanel)
		fvbox = QtGui.QVBoxLayout(frame)
		label = QtGui.QLabel("Node Type to add")
		self.node_type_combo = QtGui.QComboBox() 
		self.node_stacked_widget = QtGui.QStackedWidget()
		self.node_stacked_widget.setFrameStyle(QtGui.QFrame.StyledPanel)
		self.addnode_button = QtGui.QPushButton("Add Node")
		fvbox.addWidget(label)
		fvbox.addWidget(self.node_type_combo)
		fvbox.addWidget(self.node_stacked_widget)
		fvbox.addWidget(self.addnode_button)
		frame.setLayout(fvbox)
		# vbox widgets
		vbox.addWidget(frame)
		self.cancel_button = QtGui.QPushButton("Cancel")
		vbox.addWidget(self.cancel_button)
		self.setLayout(vbox)
		
		# Populate node types		
		self.node_type_combo.addItem("Cube")
		self.node_stacked_widget.addWidget(self.getCubeWidget())
		self.node_type_combo.addItem("Sphere")
		self.node_stacked_widget.addWidget(self.getSphereWidget())
		self.node_type_combo.addItem("Cylinder")
		self.node_stacked_widget.addWidget(self.getCylinderWidget())
		self.node_type_combo.addItem("Data")
		self.node_stacked_widget.addWidget(self.getDataWidget())
		if self.item.item3d().name == "Data":
			self.node_type_combo.addItem("Isosurface")
			self.node_stacked_widget.addWidget(self.getIsosurfaceWidget())
		
		self.connect(self.addnode_button, QtCore.SIGNAL('clicked()'), self._on_add_node)
		self.connect(self.cancel_button, QtCore.SIGNAL('clicked()'), self._on_cancel)
		self.connect(self.node_type_combo, QtCore.SIGNAL("activated(int)"), self._node_combobox_changed)
	
	def getCubeWidget(self):
		"""
		Return a cube control widget for the stacked_widget
		"""
		cubewidget = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		cube_dim_label = QtGui.QLabel("Cube Dimension")
		self.cube_dim = QtGui.QLineEdit()
		node_name_label = QtGui.QLabel("Cube Name")
		self.node_name_cube = QtGui.QLineEdit()
		grid.addWidget(cube_dim_label, 0, 0)
		grid.addWidget(self.cube_dim, 0, 1)
		grid.addWidget(node_name_label , 1, 0)
		grid.addWidget(self.node_name_cube, 1, 1)
		cubewidget.setLayout(grid)
		return cubewidget
		
	def getSphereWidget(self):
		"""
		Return a sphere control widget for the stacked_widget
		"""
		spherewidget = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		sphere_dim_label = QtGui.QLabel("Sphere Dimension")
		self.sphere_dim = QtGui.QLineEdit()
		node_name_label = QtGui.QLabel("Sphere Name")
		self.node_name_sphere = QtGui.QLineEdit()
		grid.addWidget(sphere_dim_label, 0, 0)
		grid.addWidget(self.sphere_dim, 0, 1)
		grid.addWidget(node_name_label , 1, 0)
		grid.addWidget(self.node_name_sphere, 1, 1)
		spherewidget.setLayout(grid)
		return spherewidget
		
	def getCylinderWidget(self):
		"""
		Return a cylider control widget for the stacked_widget
		"""
		cyliderwidget = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		cylider_radius_label = QtGui.QLabel("Cylider Radius")
		self.cylider_radius = QtGui.QLineEdit()
		grid.addWidget(cylider_radius_label, 0, 0)
		grid.addWidget(self.cylider_radius, 0, 1)
		cylider_height_label = QtGui.QLabel("Cylider Height")
		self.cylider_height = QtGui.QLineEdit()
		node_name_label = QtGui.QLabel("Cylider Name")
		self.node_name_cylinder = QtGui.QLineEdit()
		grid.addWidget(cylider_height_label, 1, 0)
		grid.addWidget(self.cylider_height, 1, 1)
		grid.addWidget(node_name_label , 2, 0)
		grid.addWidget(self.node_name_cylinder, 2, 1)
		cyliderwidget.setLayout(grid)
		return cyliderwidget
	
	def getDataWidget(self):
		"""
		Get Data Widget
		"""
		datawidget = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		node_name_data_label = QtGui.QLabel("Data Label")
		self.node_name_data = QtGui.QLineEdit()
		data_path_label = QtGui.QLabel("Data Path")
		self.data_path = QtGui.QLineEdit()
		self.browse_button = QtGui.QPushButton("Browse")
		grid.addWidget(node_name_data_label, 0, 0)
		grid.addWidget(self.node_name_data, 0, 1)
		grid.addWidget(data_path_label, 1, 0)
		grid.addWidget(self.data_path, 1, 1)
		grid.addWidget(self.browse_button, 2, 0, 1, 2)
		datawidget.setLayout(grid)
		
		self.connect(self.browse_button, QtCore.SIGNAL('clicked()'), self._on_browse)
		
		return datawidget
	
	def getIsosurfaceWidget(self):
		"""
		Get Isosurface Widget
		"""
		isosurfacewidget = QtGui.QWidget()
		grid = QtGui.QGridLayout()
		node_name_data_label = QtGui.QLabel("Isosurface Name")
		self.node_name_data = QtGui.QLineEdit()
		grid.addWidget(node_name_data_label, 0, 0)
		grid.addWidget(self.node_name_data, 0, 1)
		isosurfacewidget.setLayout(grid)
		
		return isosurfacewidget
		
	def _on_browse(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Get file', os.getcwd())
		self.data_path.setText(filename)
		name = os.path.basename(str(filename))
		self.node_name_data.setText(name)
	
	def _on_add_node(self):
		if not self.item.parent:
			print "Cannot add another top level node!!!"
			self.done(0)
			return
		insertion_node = None
		node_name = "default"
		itemparentnode = self.item.parent()
		# Cube
		if self.node_type_combo.currentText() == "Cube":
			insertion_node = EMCube(float(self.cube_dim.text()))
			if self.node_name_cube.text() != "": node_name = self.node_name_cube.text()
		# Sphere
		if self.node_type_combo.currentText() == "Sphere":
			insertion_node = EMSphere(float(self.sphere_dim.text()))
			if self.node_name_sphere.text() != "": node_name = self.node_name_sphere.text()
		# Cylinder
		if self.node_type_combo.currentText() == "Cylinder":
			insertion_node = EMCylinder(float(self.cylider_radius.text()), float(self.cylider_height.text()))
			if self.node_name_cylinder.text() != "": node_name = self.node_name_cylinder.text()
		# Data
		if self.node_type_combo.currentText() == "Data": 
			if str(self.data_path.text()) == "": self._on_browse()
			insertion_node =  EMDataItem3D(str(self.data_path.text()), transform=Transform())
			if self.node_name_data.text() != "": node_name = self.node_name_data.text()
		# Isosurface
		if self.node_type_combo.currentText() == "Isosurface": 
			insertion_node =  EMIsosurface(self.item.item3d(), transform=Transform())
			if self.node_name_data.text() != "": node_name = self.node_name_data.text()
			itemparentnode=self.item
			
		thisnode_index = itemparentnode.indexOfChild(self.item)
		self.inspector().addTreeNode(node_name, insertion_node, parentitem=itemparentnode, insertionindex=(thisnode_index+1))
		itemparentnode.item3d().addChild(insertion_node)
		self.inspector().updateSceneGraph()
		self.done(0)
	
	def _on_cancel(self):
		self.done(1)
	
	def _node_combobox_changed(self, nodetype):
		self.node_stacked_widget.setCurrentIndex(nodetype)
		
###################################### TEST CODE, THIS WILL NOT APPEAR IN THE WIDGET3D MODULE ##################################################
		
# All object that are rendered inherit from abstractSGnode and implement the render method

class GLdemo(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.widget = EMScene3D()
		#self.widget.camera.usePrespective(50, 0.5)
		self.cube = EMCube(50.0)
		self.widget.addChild(self.cube)    # Something to Render something..... (this could just as well be one of Ross's SGnodes)
		self.sphere = EMSphere(50.0)
		self.widget.addChild(self.sphere)
		self.cylider = EMCylinder(50.0, 50.0)
		self.widget.addChild(self.cylider)
		#self.emdata = EMDataItem3D("/home/john/Bo_data/simulated_data/3DmapIP3R1_small.mrc", transform=Transform())
		#self.widget.addChild(self.emdata)
		#self.isosurface = EMIsosurface(self.emdata, transform=Transform())
		#self.emdata.addChild(self.isosurface)
		
		self.inspector = EMInspector3D(self.widget)
		self.widget.setInspector(self.inspector)
		self.inspector.loadSG()
		
		# QT stuff to display the widget
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.widget)
		self.setLayout(vbox)
		self.setGeometry(300, 300, 600, 600)
		self.setWindowTitle('BCM EM Viewer')
		
	def show_inspector(self):
		self.inspector.show()
		
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	window = GLdemo()
	window.show()
	window.show_inspector()
	app.exec_()
