#!/usr/bin/env python

# Author:  David Woolford 10/26/2007 (woolford@bcm.edu)
# Copyright (c) 2000-2006 Baylor College of Medicine
#
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston MA 02111-1307 USA
#
#

from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import Qt
from OpenGL import GL,GLU,GLUT
from OpenGL.GL import *
from OpenGL.GLU import *
from valslider import ValSlider
from math import *
from EMAN2 import *

from emapplication import EMGUIModule,EMQtWidgetModule

try: from PyQt4 import QtWebKit
except: pass

import numpy
import sys
import array

class EMBasicOpenGLObjects:
	"""
	This class is supposed to encapsulate basic and common objects
	used by various other OpenGL classes in EMAN2 pyqt interfaces.
	
	It currently supplies display list ids - one for a sphere, one for
	a cylinder
	
	It's implemented as a singleton
	"""
	class __impl:
		""" Implementation of the singleton interface """

		def __init__(self):
			# this display list ids
			self.cylinderdl = 0
			self.spheredl = 0
		
			# cylinder parameters
			self.cylinder_around_z = 12
			self.cylinder_along_z = 2
			
			# sphere parameters
			self.sphere_around_z = 6
			self.sphere_along_z = 6
			
			self.gq=gluNewQuadric()
			gluQuadricDrawStyle(self.gq,GLU_FILL)
			gluQuadricNormals(self.gq,GLU_SMOOTH)
			gluQuadricOrientation(self.gq,GLU_OUTSIDE)
			gluQuadricTexture(self.gq,GL_FALSE)
		
		def __del__(self):
			if self.cylinderdl != 0:
				glDeleteLists(self.cylinderdl,1)
			if self.spheredl != 0:
				glDeleteLists(self.spheredl,1)
			
		def getSphereDL(self):
			if ( self.spheredl == 0 ):
				self.spheredl=glGenLists(1)
				
				glNewList(self.spheredl,GL_COMPILE)
				glPushMatrix()
				gluSphere(self.gq,.5,self.sphere_along_z,self.sphere_around_z)
				glPopMatrix()
				
				glEndList()
				
			return self.spheredl
		
		def getCylinderDL(self):
			if ( self.cylinderdl == 0 ):
				self.cylinderdl=glGenLists(1)
				
				glNewList(self.cylinderdl,GL_COMPILE)
				glPushMatrix()
				gluCylinder(self.gq,1.0,1.0,1.0,self.cylinder_around_z,self.cylinder_along_z)
				glPopMatrix()
				
				glEndList()
				
			return self.cylinderdl

	# storage for the instance reference
	__instance = None


	def __init__(self):
		""" Create singleton instance """
		# Check whether we already have an instance
		if EMBasicOpenGLObjects.__instance is None:
			# Create and remember instance
			EMBasicOpenGLObjects.__instance = EMBasicOpenGLObjects.__impl()
	
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

def resize_gl():
	view = EMGLProjViewMatrices()
	view.set_update(True)
	
def viewport_height():
	view = EMGLProjViewMatrices()
	return view.viewport_height()
	
def viewport_width():
	view = EMGLProjViewMatrices()
	return view.viewport_width()

class EMGLProjViewMatrices:
	"""
	Controls a static single instance of OpenGL projection and view(port) matrices
	Also stores a static single instance of the inverse of the projection matrix, which
	is calculates using numpy/scipy. Other classes interface with this by calling
	set_update when the viewport or projection matrix has changed (i.e., a resize event)
	"""
	class __impl:
		""" Implementation of the singleton interface """

		def __init__(self):
			self.update = True
			self.proj_matrix = None
			self.inv_proj_matrix = None
			self.view_matrix = None
		
		def update_opengl_matrices(self, val=True):
			self.update_viewport_matrix()
			self.update_projection_matrix()
			self.update_projection_inv_matrix()
			
		def set_update(self,val=True):
			self.update = val
		
		def update_projection_inv_matrix(self):
			P = numpy.matrix(self.proj_matrix)
			self.inv_proj_matrix = P.I
			
		def update_projection_matrix(self):
			self.proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
		
		def update_viewport_matrix(self):
			 self.view_matrix = glGetIntegerv(GL_VIEWPORT)
		
		def check_update(self):
			if (self.update):
				self.update_opengl_matrices()
				self.update = False
		
		def get_viewport_matrix(self):
			self.check_update()
			return self.view_matrix
		
		def get_proj_matrix(self):
			self.check_update()
			return self.proj_matrix
		
		def get_proj_inv_matrix(self):
			self.check_update()
			return self.inv_proj_matrix
		
		def viewport_height(self):
			self.check_update()
			return self.view_matrix[3] - self.view_matrix[1]
		
		def viewport_width(self):
			self.check_update()
			return self.view_matrix[2] - self.view_matrix[0]

			
	# storage for the instance reference
	__instance = None


	def __init__(self):
		""" Create singleton instance """
		# Check whether we already have an instance
		if EMGLProjViewMatrices.__instance is None:
			# Create and remember instance
			EMGLProjViewMatrices.__instance = EMGLProjViewMatrices.__impl()
	
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

class EMViewportDepthTools:
	"""
	This class provides important tools for EMAN2 floating widgets -
	these are either qt widgets that get mapped as textures to
	polygons situated in OpenGL volumes, or are OpenGL objects themselves
	(such as a 2D image texture, or a 3D isosurface), that get drawn
	within a frame somewhere in the 3D world.
	
	These objects need to have mouse events (etc) correctly rerouted to them,
	and this is not trivial (but not difficult) to do, considering that the
	mouse events are always in terms of the viewport, but the texture mapped
	widget is somewhere in 3D space. The function eye_coords_dif is primarily
	for positioning the widgits in 3D space (translation), whereas the 
	mouseinwin function is specifically for mapping the mouse event coordinates
	into the widgit's transformed coordinate system.

	This class also provides important collision detection functionality - it
	does this by mapping the corners of the (widgit mapped) polygon to the viewport,
	and then determing if the (mouse) coordinate is within this area. Mapping 
	polygon vertices to the veiwport is done using gluUnproject, whereas converting
	viewport coordinates into polygon coordinates is done doing something similar to
	gluProject (the opposite operation).

	This class also provides widget frame drawing functionality (which may become redundant)
	It does this by drawing cylinders in terms of how the polygon corners mapped
	to the viewport - this causes the loss of depth information
	
	The only important behaviour expected of something that uses this class is
	1 - you must call update() just before you draw the textured widgit polygon
	other object (i.e. when the contents of the OpenGL modelview matrix reflect 
	all of the operations that are applied before rendering)
	2 - you should call set_update_P_inv() if the OpenGL projection matrix is altered,
	this typically happens when resizeGL is called in the root widgit.
	"""
	def __init__(self, parent):
		self.parent = parent
		
		self.glbasicobjects = EMBasicOpenGLObjects()		# need basic objects for drawing the frame
		self.matrices = EMGLProjViewMatrices()				# an object that stores static instances of the important viewing matrices
		self.borderwidth = 3.0								# effects the border width of the frame decoration
		
	def set_update_P_inv(self,val=True):
		self.matrices.set_update(val)
	
	
	def get_viewport_dimensions(self):
		return self.matrices.get_viewport_matrix()
	
	def draw_frame(self, ftest=False):
		
		if (ftest):
			a = Vec3f(self.mc10[0]-self.mc00[0],self.mc10[1]-self.mc00[1],self.mc10[2]-self.mc00[2])
			b = Vec3f(self.mc01[0]-self.mc00[0],self.mc01[1]-self.mc00[1],self.mc01[2]-self.mc00[2])
			c = a.cross(b)
			if ( c[2] < 0 ):
				#print "facing backward"
				return False
			
		glColor(.9,.2,.8)
		# this is a nice light blue color (when lighting is on)
		# and is the default color of the frame
		glMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,(.2,.2,.8,1.0))
		glMaterial(GL_FRONT,GL_SPECULAR,(.8,.8,.8,1.0))
		glMaterial(GL_FRONT,GL_SHININESS,50.0)
		
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		glOrtho(0.0,viewport_width(),0.0,viewport_height(),-5,5)

		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		
		glColor(.9,.2,.8)
		# this is a nice light blue color (when lighting is on)
		# and is the default color of the frame
		glMaterial(GL_FRONT,GL_AMBIENT,(.2,.2,.8,1.0))
		glMaterial(GL_FRONT,GL_SPECULAR,(.8,.8,.8,1.0))
		glMaterial(GL_FRONT,GL_SHININESS,50.0)
		
		#draw the cylinders around the edges of the frame
		glPushMatrix()
		self.cylinderToFrom(self.mc00,self.mc10)
		glPopMatrix()
		glPushMatrix()
		self.cylinderToFrom(self.mc10,self.mc11)
		glPopMatrix()
		glPushMatrix()
		self.cylinderToFrom(self.mc11,self.mc01)
		glPopMatrix()
		glPushMatrix()
		self.cylinderToFrom(self.mc01,self.mc00)
		glPopMatrix()
		
		# draw spheres as nodes at the corners of the frame
		glPushMatrix()
		self.sphereAt(self.mc00)
		glPopMatrix()
		glPushMatrix()
		self.sphereAt(self.mc10)
		glPopMatrix()
		glPushMatrix()
		self.sphereAt(self.mc11)
		glPopMatrix()
		glPushMatrix()
		self.sphereAt(self.mc01)
		glPopMatrix()
		
		glPopMatrix()
		
		glMatrixMode(GL_PROJECTION)
		# pop the temporary orthographic matrix from the GL_PROJECTION stack
		glPopMatrix()
		glMatrixMode(GL_MODELVIEW)
		
		return True
	def cylinderToFrom(self,To,From):
		#print "To",To[0],To[1]
		#print "From",From[0],From[1]
		# draw a cylinder to To from From
		dx = To[0] - From[0]
		dy = To[1] - From[1]
		
		length = sqrt(dx*dx+dy*dy)
		
		angle = 180.0*atan2(dy,dx)/pi
		
		glTranslated(From[0],From[1],0)
		glRotated(90.0+angle,0.,0.,1.0)
		glRotated(90.,1.,0.,0.)
		glTranslated(0.0,0.0,length/2.0)
		glScaled(self.borderwidth,self.borderwidth,length)
		glTranslated(0.0,0.0,-0.5)
		glCallList(self.glbasicobjects.getCylinderDL())
		
	def sphereAt(self,at):
		glTranslate(at[0],at[1],0)
		glScalef(3.0*self.borderwidth,3.0*self.borderwidth,3.0*self.borderwidth)
		glCallList(self.glbasicobjects.getSphereDL())
	
	def update(self,width,height):
		
		self.wmodel= glGetDoublev(GL_MODELVIEW_MATRIX)
		self.wproj = self.matrices.get_proj_matrix()
		self.wview = self.matrices.get_viewport_matrix()

		try:
			self.mc00=gluProject(-width,-height,0.,self.wmodel,self.wproj,self.wview)
			self.mc10=gluProject( width,-height,0.,self.wmodel,self.wproj,self.wview)
			self.mc11=gluProject( width, height,0.,self.wmodel,self.wproj,self.wview)
			self.mc01=gluProject(-width, height,0.,self.wmodel,self.wproj,self.wview)
			
		except:
			self.mc00 = [0,0,0]
			self.mc10 = [0,0,0]
			self.mc11 = [0,0,0]
			self.mc01 = [0,0,0]
	
	def unproject_points(self,points):
		unprojected = []
		self.wmodel= glGetDoublev(GL_MODELVIEW_MATRIX)
		self.wproj = self.matrices.get_proj_matrix()
		self.wview = self.matrices.get_viewport_matrix()
		for p in points:
			unprojected.append(gluProject(p[0],p[1],p[2],self.wmodel,self.wproj,self.wview))
			
		return unprojected
	
	def set_mouse_coords(self,mc00,mc10,mc11,mc01):
		self.mc00 = mc00
		self.mc10 = mc10
		self.mc11 = mc11
		self.mc01 = mc01
	
	def update_points(self,p1,p2,p3,p4):
		
		self.wmodel= glGetDoublev(GL_MODELVIEW_MATRIX)
		self.wproj = self.matrices.get_proj_matrix()
		self.wview = self.matrices.get_viewport_matrix()

		try:
			self.mc00=gluProject(p1[0],p1[1],p1[2],self.wmodel,self.wproj,self.wview)
			self.mc10=gluProject(p2[0],p2[1],p2[2],self.wmodel,self.wproj,self.wview)
			self.mc11=gluProject(p3[0],p3[1],p3[2],self.wmodel,self.wproj,self.wview)
			self.mc01=gluProject(p4[0],p4[1],p4[2],self.wmodel,self.wproj,self.wview)
			
		except:
			self.mc00 = [0,0,0]
			self.mc10 = [0,0,0]
			self.mc11 = [0,0,0]
			self.mc01 = [0,0,0]
			
	def get_corners(self):
		return [self.mc00,self.mc01,self.mc11,self.mc10]
	
	def getEmanMatrix(self):
	
		t = Transform3D(self.wmodel[0][0], self.wmodel[1][0], self.wmodel[2][0],
						self.wmodel[0][1], self.wmodel[1][1], self.wmodel[2][1],
						self.wmodel[0][2], self.wmodel[1][2], self.wmodel[2][2] )
		return t
	
	def getCurrentScale(self):
		return sqrt(self.wmodel[0][0]**2 + self.wmodel[0][1]**2 + self.wmodel[0][2]**2)
	
	def getModelMatrix(self):
		return self.wmodel
	
	def setModelMatrix(self, model):
		self.wmodel = model
	
	def setCorners(self,points):
		self.mc00 = points[0]
		self.mc01 = points[1]
		self.mc11 = points[2]
		self.mc10 = points[3]
		
	def store_model(self):
		self.wmodel= glGetDoublev(GL_MODELVIEW_MATRIX)
	
	def printUnproj(self,x,y):
		self.wmodel= glGetDoublev(GL_MODELVIEW_MATRIX)
		self.wproj = self.matrices.get_proj_matrix()
		self.wview = self.matrices.get_viewport_matrix()
	
		t = gluProject(x,y,0.,self.wmodel,self.wproj,self.wview)
		print t[0],t[1],t[2]
		
		
	def getMappedWidth(self):
		return int(self.mc11[0]-self.mc00[0])
		
	def getMappedHeight(self):
		return int(self.mc11[1]-self.mc00[1])
	
	def isinwinpoints(self,x,y,points):
		try:
			a = [points[0][0]-x, points[0][1]-y]
			b = [points[1][0]-x, points[1][1]-y]
			c = [points[2][0]-x, points[2][1]-y]
			d = [points[3][0]-x, points[3][1]-y]
			
			aeb = self.getsubtendingangle(a,b)
			bec = self.getsubtendingangle(b,c)
			ced = self.getsubtendingangle(c,d)
			dea = self.getsubtendingangle(d,a)
			if abs(aeb + bec + ced + dea) > 0.1:
				return True 
			else:
				return False
		except:
			return False
	
	def isinwin(self,x,y):
		# this function can be called to determine
		# if the event at x,y (in terms of the viewport)
		# was within the frame of the object being drawn
		
		#print x,y
		#print self.mc00,self.mc11
		
		try:
			a = [self.mc00[0]-x, self.mc00[1]-y]
			b = [self.mc01[0]-x, self.mc01[1]-y]
			c = [self.mc11[0]-x, self.mc11[1]-y]
			d = [self.mc10[0]-x, self.mc10[1]-y]
			
			aeb = self.getsubtendingangle(a,b)
			bec = self.getsubtendingangle(b,c)
			ced = self.getsubtendingangle(c,d)
			dea = self.getsubtendingangle(d,a)
			if abs(aeb + bec + ced + dea) > 0.1:
				return True 
			else:
				return False
		except:
			return False
	
	def getsubtendingangle(self,a,b):
		sinaeb = a[0]*b[1]-a[1]*b[0]
		cosaeb = a[0]*b[0]+a[1]*b[1]
		
		return atan2(sinaeb,cosaeb)
	
	def eye_coords_dif(self,x1,y1,x2,y2,maintaindepth=True):
		self.wview = self.matrices.get_viewport_matrix()
		# get x and y normalized device coordinates
		xNDC1 = 2.0*(x1-self.wview[0])/self.wview[2] - 1
		yNDC1 = 2.0*(y1-self.wview[1])/self.wview[3] - 1
		
		xNDC2 = 2.0*(x2-self.wview[0])/self.wview[2] - 1
		yNDC2 = 2.0*(y2-self.wview[1])/self.wview[3] - 1
		
		self.P_inv = self.matrices.get_proj_inv_matrix()
		
		try:
			M = numpy.matrix(self.wmodel)
		except:
			self.store_model()
			M = numpy.matrix(self.wmodel)
		M_inv = M.I
		
		#PM_inv = numpy.matrixmultiply(P_inv,M_inv)
		PM_inv = self.P_inv*M_inv
		
		# If the widget is planar (which obviosuly holds), and along z=0, then the following holds
		zNDC1 = (PM_inv[0,2]*xNDC1 + PM_inv[1,2]*yNDC1 + PM_inv[3,2])/(-PM_inv[2,2])
		if ( maintaindepth == False):
			zNDC2 = (PM_inv[0,2]*xNDC2 + PM_inv[1,2]*yNDC2 + PM_inv[3,2])/(-PM_inv[2,2])
		else:
			zNDC2 = zNDC1
	
		# We need zprime, which is really 'eye_z' in OpenGL lingo
		zprime1 = 1.0/(xNDC1*self.P_inv[0,3]+yNDC1*self.P_inv[1,3]+zNDC1*self.P_inv[2,3]+self.P_inv[3,3])
		zprime2 = 1.0/(xNDC2*self.P_inv[0,3]+yNDC2*self.P_inv[1,3]+zNDC2*self.P_inv[2,3]+self.P_inv[3,3])

		ex1 = (self.P_inv[0,0]*xNDC1 + self.P_inv[1,0]*yNDC1 + self.P_inv[2,0]*zNDC1+self.P_inv[3,0])*zprime1;
		ey1 = (self.P_inv[0,1]*xNDC1 + self.P_inv[1,1]*yNDC1 + self.P_inv[2,1]*zNDC1+self.P_inv[3,1])*zprime1;
		#ez1 = (self.P_inv[0,2]*xNDC1 + self.P_inv[1,2]*yNDC1 + self.P_inv[2,2]*zNDC1+self.P_inv[3,2])*zprime1;
		
		ex2 = (self.P_inv[0,0]*xNDC2 + self.P_inv[1,0]*yNDC2 + self.P_inv[2,0]*zNDC2+self.P_inv[3,0])*zprime2;
		ey2 = (self.P_inv[0,1]*xNDC2 + self.P_inv[1,1]*yNDC2 + self.P_inv[2,1]*zNDC2+self.P_inv[3,1])*zprime2;
		
		return [ex2-ex1,ey2-ey1]

	def mouseinwin(self,x,y,width,height):
		self.wview = self.matrices.get_viewport_matrix()
		# to determine the mouse coordinates in the window we carefully perform
		# linear algebra similar to what's done in gluUnProject

		# the problem is determining what the z coordinate of the mouse event should have
		# been, given that we know that the widget itself is located in the x,y plane, along z=0.
		
		# get x and y normalized device coordinates
		xNDC = 2.0*(x-self.wview[0])/self.wview[2] - 1
		yNDC = 2.0*(y-self.wview[1])/self.wview[3] - 1
		
		# invert the projection and model view matrices, they will be used shortly
		# note the OpenGL returns matrices are in column major format -  the calculations below 
		# are done with this in  mind - this saves the need to transpose the matrices
		self.P_inv = self.matrices.get_proj_inv_matrix()
		
		try:
			M = numpy.matrix(self.wmodel)
		except:
			self.store_model()
			M = numpy.matrix(self.wmodel)
		M_inv = M.I
		#PM_inv = numpy.matrixmultiply(P_inv,M_inv)
		PM_inv = self.P_inv*M_inv
		
		# If the widget is planar (which obviosuly holds), and along z=0, then the following holds
		zNDC = (PM_inv[0,2]*xNDC + PM_inv[1,2]*yNDC + PM_inv[3,2])/(-PM_inv[2,2])
	
		# We need zprime, which is really 'eye_z' in OpenGL lingo
		zprime = 1.0/(xNDC*self.P_inv[0,3]+yNDC*self.P_inv[1,3]+zNDC*self.P_inv[2,3]+self.P_inv[3,3])
		
		# Now we compute the x and y coordinates - these are precisely what we're after
		xcoord = zprime*(xNDC*PM_inv[0,0]+yNDC*PM_inv[1,0]+zNDC*PM_inv[2,0]+PM_inv[3,0])
		ycoord = zprime*(xNDC*PM_inv[0,1]+yNDC*PM_inv[1,1]+zNDC*PM_inv[2,1]+PM_inv[3,1])

		return (xcoord + width*0.5, 0.5*height-ycoord)

class EMOpenGLFlagsAndTools:
	"""
	This is a singleton class that encapsulates OpenGL flags and tools -
	flags that are important to the functioning of EMAN2 user interfaces.
	 
	It is driven by the idea that it is much more efficient to check whether
	different OpenGL features are available ONLY ONCE
	
	For instance, this class can be asked whether or not 3D texturing
	is supported, whether or not power of two textures are supported,
	and various other things that will be added as development continues.
	
	All OpenGL-related Texture flags and generic operations should end up in this class.
	"""
	class __impl:
		""" Implementation of the singleton interface """

		def __init__(self):
			self.power_of_two_init_check = True 	# an internal flag for forcing a once (and only) OpenGL query about power of 2 textures
			self.use_mipmaps = False				# use mipmaps means power of two-textures are not supported
			self.force_use_mipmaps = False			# This flag is toggled by the developer to force the use of mipmaps
		
			self.threed_texture_check = True		# an internal flag for forcing a once (and only) OpenGL query regarding 3D textures
			self.use_3d_texture = True				# this flag stores whether or not 3D texturing is supported 
			self.disable_3d_texture = False			# This flag is toggled by the developer to force the use of 2D textures
			
			self.blend_equation_check = True 		# an internal flag for forcing a once (and only) OpenGL query about the availability of glBlendEquation
			self.use_blend_equation = True			# an internal flag storing whether or not glBlendEquation is available
			self.force_blend_equation_off = False	# This flag is toggled by the developer to forcibly stop apps from using glBlendEquation
			
		# non power of two
		def npt_textures_unsupported(self):
			if ( self.force_use_mipmaps ): return True
			
			if self.power_of_two_init_check == True:
				try:
					if str("GL_ARB_texture_non_power_of_two") not in glGetString(GL_EXTENSIONS) :
						self.use_mipmaps = True
						#print "EMAN(ALPHA) message: No support for non power of two textures detected. Using mipmaps."
					else:
						self.use_mipmaps = False
						#print "EMAN(ALPHA) message: Support for non power of two textures detected."
				except:
					print "error, OpenGL seems not to be initialized"
					return False
			
				self.power_of_two_init_check = False
			
			return self.use_mipmaps
			
		def threed_texturing_supported(self):
			if ( self.disable_3d_texture ): return False
			
			if ( self.threed_texture_check == True ):
				disable = True
				
				# sigh - I couldn't find an EXTENSION or simple way of testing for this,
				# so I just did it this way. I am worried this approach may not work
				# in all cases because it is not conventional
				# FIXME - 3D textures were introduced in Version 1.2
				# This problem is more convoluted then it seems. I think we may be having problems
				# because of PyOpenGL problems, and/or possibly due to lack of accelerated drivers....
				# needs more investigation.
				try: glEnable(GL_TEXTURE_3D)
				except:
					disable = False
					#print "EMAN(ALPHA) message: disabling use of 3D textures"
					self.use_3d_texture = False
				
				if (disable):
					glDisable(GL_TEXTURE_3D)
					self.use_3d_texture = True
					#print "EMAN(ALPHA) message: 3D texture support detected"
				
				self.threed_texture_check = False
				
			return self.use_3d_texture

		
		def gen_textureName(self,data):
			if ( not data_dims_power_of(data,2) and self.npt_textures_unsupported()):
				return data.gen_glu_mipmaps()
			else:
				return data.gen_gl_texture() 

		def blend_equation_supported(self):
			if (self.force_blend_equation_off): return False
			
			if self.blend_equation_check == True:
				try:
					if str("GL_ARB_imaging") not in glGetString(GL_EXTENSIONS) :
						self.use_blend_equation = False
						#print "EMAN(ALPHA) message: No support for glBlendEquation detected. Disabling."
					else:
						self.use_blend_equation = True
						#print "EMAN(ALPHA) message: Support for glBlendEquation detected."
				except:
					print "error, OpenGL seems not to be initialized"
					return False
			
				self.blend_equation_check = False
			
			return self.use_blend_equation
				
				
	# storage for the instance reference
	__instance = None


	def __init__(self):
		""" Create singleton instance """
		# Check whether we already have an instance
		if EMOpenGLFlagsAndTools.__instance is None:
			# Create and remember instance
			EMOpenGLFlagsAndTools.__instance = EMOpenGLFlagsAndTools.__impl()
	
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)


class Camera2:
	"""\brief A camera object encapsulates 6 degrees of freedom, and a scale factor
	
	The camera object stores x,y,z coordinates and a single transform object.
	For instance, it can be used for positioning and moving the 'camera' in OpenGL,
	however, instead of literally moving a camera, in OpenGL the scene itself is moved
	and the camera is generally thought of as staying still.
	
	Use the public interface of setCamTrans and motion_rotate (which is based on mouse movement)_
	to move the camera position
	
	Then call 'position' in your main OpenGL draw function before drawing anything.
	
	"""
	def __init__(self,parent):
		# The magnification factor influences how the scale (zoom) is altered when a zoom event is received.
		# The equation is scale *= mag_factor or scale /= mag_factor, depending on the event.
		self.parent=parent
		self.mag_factor = 1.1
		
		self.t3d_stack = []
		self.loadIdentity()
		
		self.mmode = 0
		self.debug = False
		
		self.enablerotation = True
		
		self.basicmapping = False
		self.plane = 'xy'
		
		self.motiondull = 8.0
		
		self.mpressx = -1
		self.mpressy = -1

	
	def set_plane(self,plane='xy'):
		'''
		plane should by xy,yx,xz,zx,yz, or zy. It should also be a string
		'''
		self.plane = plane
	
	def allow_camera_rotations(self,bool=True):
		self.enablerotation = bool

		
	def loadIdentity(self):
		self.scale = 1.0
		
		# The camera coordinates
		self.cam_x = 0
		self.cam_y = 0
		self.cam_z = 0
		
		# Camera offsets - generally you want to set default_z to some negative
		# value the OpenGL scene is viewable.
		self.default_x = 0
		self.default_y = 0
		self.default_z = 0
		
		t3d = Transform3D()
		t3d.to_identity()
		self.t3d_stack.append(t3d)
	
	def undoScale(self):
		glScalef(1.0/self.scale,1.0/self.scale,1.0/self.scale)
			
	
	def undoRot(self):
		rot = self.t3d_stack[len(self.t3d_stack)-1].get_rotation()
		if ( self.enablerotation ):
			glRotate(-float(rot["az"]),0,0,1)
			glRotate(-float(rot["alt"]),1,0,0)
			glRotate(-float(rot["phi"]),0,0,1)
		
	
	def position(self,norot=False):
		# position the camera, regualar OpenGL movement.
		if (self.debug):
			print "Camera translational position",self.cam_x,self.cam_y,self.cam_z
		glTranslate(self.cam_x, self.cam_y, self.cam_z)
		
		if ( self.enablerotation and not norot):
			rot = self.t3d_stack[len(self.t3d_stack)-1].get_rotation()
			if (self.debug):
				print "Camera rotation ",float(rot["phi"]),float(rot["alt"]),float(rot["az"])
			glRotate(float(rot["phi"]),0,0,1)
			glRotate(float(rot["alt"]),1,0,0)
			glRotate(float(rot["az"]),0,0,1)
		
		if (self.debug):
			print "Camera scale ",self.scale
		# here is where zoom is applied
		glScale(self.scale,self.scale,self.scale)
		
	def scale_event(self,delta):
		if delta > 0:
			self.scale *= self.mag_factor
		elif delta < 0:
			self.scale *= 1.0/self.mag_factor
	
	def setCamTrans(self,axis,value):
		if ( axis == 'x'):
			self.set_cam_x(value)
		elif ( axis == 'y'):
			self.set_cam_y(value)
		elif ( axis == 'z'):
			self.set_cam_z(value)
		elif ( axis == 'default_x'):
			self.default_x = value
		elif ( axis == 'default_y'):
			self.default_y = value
		elif ( axis == 'default_z'):
			self.default_z = value
			self.set_cam_z(0)
		else:
			print 'Error, the axis (%s) specified is unknown. No action was taken' %axis
	
	def set_cam_z(self,z):
		self.cam_z = self.default_z + z
		
	def set_cam_y(self,y):
		self.cam_y = self.default_y + y
		
	def set_cam_x(self,x):
		self.cam_x = self.default_x + x

	def motion_rotate(self,x,y,fac=1.0):
		# this function implements mouse interactive rotation
		# [x,y] is the vector generating by the mouse movement (in the plane of the screen)
		# Rotation occurs about the vector 90 degrees to [x,y,0]
		# The amount of rotation is linealy proportional to the length of [x,y]
		
		if ( x == 0 and y == 0): return
		
		theta = atan2(-y,x)

		plane = self.plane
		if ( plane == 'xy' ):
			rotaxis_x = sin(theta)
			rotaxis_y = cos(theta)
			rotaxis_z = 0
		elif ( plane == 'yx' ):
			rotaxis_x = -sin(theta)
			rotaxis_y = cos(theta)
			rotaxis_z = 0
		elif ( plane == 'xz' ):
			rotaxis_x = sin(theta)
			rotaxis_y = 0
			rotaxis_z = cos(theta)
		elif ( plane == 'zx' ):
			rotaxis_x = sin(theta)
			rotaxis_y = 0
			rotaxis_z = -cos(theta)
		elif ( plane == 'yz' ):
			rotaxis_x = 0
			rotaxis_y = cos(theta)
			rotaxis_z = -sin(theta)
		elif ( plane == 'zy' ):
			rotaxis_x = 0
			rotaxis_y = cos(theta)
			rotaxis_z = sin(theta)
		
		length = sqrt(x*x + y*y)
		# motiondull is a magic number - things rotate more if they are closer and slower if they are far away in this appproach
		# This magic number could be overcome using a strategy based on the results of get_render_dims_at_depth
		angle = fac*length/self.motiondull*pi
		
		t3d = Transform3D()
		quaternion = {}
		quaternion["Omega"] = angle
		quaternion["n1"] = rotaxis_x
		quaternion["n2"] = rotaxis_y
		quaternion["n3"] = rotaxis_z
		
		t3d.set_rotation( EULER_SPIN, quaternion )
		
		size = len(self.t3d_stack)
		self.t3d_stack[size-1] = t3d*self.t3d_stack[size-1]
		
	def set_scale(self,val):
		self.scale = val
	
	def load_rotation(self,t3d):
		self.t3d_stack.append(t3d)

	def get_thin_copy(self):
		# this is called a thin copy because it does not copy the entire t3d stack, just the last t3d
		cam = Camera()
		size = len(self.t3d_stack)
		cam.load_rotation(self.t3d_stack[size-1])
		
		cam.scale =	self.scale
		cam.cam_x = self.cam_x
		cam.cam_y = self.cam_y
		cam.cam_z = self.cam_z
		
		cam.default_x = self.default_x
		cam.default_y = self.default_y
		cam.default_z = self.default_z
		
		return cam
	
	def mousePressEvent(self, event):
		self.mpressx = event.x()
		self.mpressy = event.y()
		if event.button()==Qt.LeftButton:
			if self.mmode==0:
				if self.enablerotation == False: return
				# this is just a way of duplicating the last copy
				tmp =self.t3d_stack.pop()
				t3d = Transform3D(tmp)
				self.t3d_stack.append(tmp)
				self.t3d_stack.append(t3d)
		
	def mouseMoveEvent(self, event):
		if event.buttons()&Qt.LeftButton:
			if self.mmode==0:
				#if event.modifiers() == Qt.ControlModifier:
					#self.motion_translate(event.x()-self.mpressx, self.mpressy - event.y())
				#else:
				if self.enablerotation == False: return
				self.motion_rotate(self.mpressx - event.x(), self.mpressy - event.y(),sqrt(1.0/self.scale))

				self.mpressx = event.x()
				self.mpressy = event.y()
		elif event.buttons()&Qt.RightButton:
			if self.mmode==0:
				self.motion_translateLA(self.mpressx, self.mpressy,event)
					
				self.mpressx = event.x()
				self.mpressy = event.y()
	
	def mouseReleaseEvent(self, event):
		if event.button()==Qt.LeftButton:
			if self.mmode==0:
				return
		elif event.button()==Qt.RightButton:
			if self.mmode==0:
				return
			
	def wheelEvent(self, event):
		self.scale_event(event.delta())
	
	def motion_translateLA(self,prev_x,prev_y,event):
		if (self.basicmapping == False):
			[dx,dy] = self.parent.eye_coords_dif(prev_x,viewport_height()-prev_y,event.x(),viewport_height()-event.y())
		else:
			[dx,dy] = [event.x()-prev_x,prev_y-event.y()]

		#[wx2,wy2,wz2] = self.parent.eyeCoords(event.x(),self.parent.parentHeight()-event.y())
		#[wx2,wy2,wz2] =  self.parent.mouseViewportMovement(event.x(),self.parent.parentHeight()-event.y(),wx1,wy1,wz1,zprime)
		#self.parent.mouseViewportMovement(1,2,3,4)
		#[wx1,wy1] = self.parent.mouseinwin(prev_x,self.parent.parentHeight()-prev_y)
		#[wx2,wy2] = self.parent.mouseinwin(event.x(),self.parent.parentHeight()-event.y())
		#self.cam_x += dx
		#self.cam_y += dy

		plane = self.plane
		if ( plane == 'xy' ):
			self.cam_x += dx
			self.cam_y += dy
		elif ( plane == 'yx' ):
			self.cam_x -= dx
			self.cam_y += dy
		elif ( plane == 'xz' ):
			self.cam_x += dx
			self.cam_z -= dy
		elif ( plane == 'zx' ):
			self.cam_x += dx
			self.cam_z += dy
		elif ( plane == 'yz' ):
			self.cam_y += dy
			self.cam_z -= dx
		elif ( plane == 'zy' ):
			self.cam_y += dy
			self.cam_z += dx
		

class Camera:
	"""\brief A camera object encapsulates 6 degrees of freedom, and a scale factor
	
	The camera object stores x,y,z coordinates and a single transform object.
	For instance, it can be used for positioning and moving the 'camera' in OpenGL,
	however, instead of literally moving a camera, in OpenGL the scene itself is moved
	and the camera is generally thought of as staying still.
	
	Use the public interface of setCamTrans and motion_rotate (which is based on mouse movement)_
	to move the camera position
	
	Then call 'position' in your main OpenGL draw function before drawing anything.
	
	"""
	def __init__(self):
		# The magnification factor influences how the scale (zoom) is altered when a zoom event is received.
		# The equation is scale *= mag_factor or scale /= mag_factor, depending on the event.
		self.mag_factor = 1.1
		self.scale = 1.0
		
		# The camera coordinates
		self.cam_x = 0
		self.cam_y = 0
		self.cam_z = 0
		
		# Camera offsets - generally you want to set default_z to some negative
		# value the OpenGL scene is viewable.
		self.default_x = 0
		self.default_y = 0
		self.default_z = 0
		
		# The Transform3D object stores the rotation
		t3d = Transform3D()
		t3d.to_identity()
	
		# At the moment there is a stack of Transform3D objects, this is for the purposes
		# of undoing actions. If the undo functionality was not required, the stack could be
		# removed.
		self.t3d_stack = []
		self.t3d_stack.append(t3d)
		
	def printme(self):
		print "translating to",self.cam_x, self.cam_y, self.cam_z
		rot = self.t3d_stack[len(self.t3d_stack)-1].get_rotation()
		print "rotatint",rot["phi"],rot["alt"],rot["az"]
		print "scale",self.scale
		
	def position(self):
		# position the camera, regular OpenGL movement.
		glTranslated(self.cam_x, self.cam_y, self.cam_z)
		
		rot = self.t3d_stack[len(self.t3d_stack)-1].get_rotation()
		glRotate(float(rot["phi"]),0,0,1)
		glRotate(float(rot["alt"]),1,0,0)
		glRotate(float(rot["az"]),0,0,1)
		
		# here is where zoom is applied
		glScalef(self.scale,self.scale,self.scale)
		
	def scale_event(self,delta):
		if delta > 0:
			self.scale *= self.mag_factor
		elif delta < 0:
			self.scale *= 1.0/self.mag_factor
	
	def setCamTrans(self,axis,value):
		if ( axis == 'x'):
			self.set_cam_x(value)
		elif ( axis == 'y'):
			self.set_cam_y(value)
		elif ( axis == 'z'):
			self.set_cam_z(value)
		elif ( axis == 'default_x'):
			self.default_x = value
		elif ( axis == 'default_y'):
			self.default_y = value
		elif ( axis == 'default_z'):
			self.default_z = value
			self.set_cam_z(self.cam_z)
		else:
			print 'Error, the axis (%s) specified is unknown. No action was taken' %axis
	
	def set_cam_z(self,z):
		self.cam_z = self.default_z + z
		
	def set_cam_y(self,y):
		self.cam_y = self.default_y + y
		
	def set_cam_x(self,x):
		self.cam_x = self.default_x + x

	def motion_rotate(self,x,y):
		# this function implements mouse interactive rotation
		# [x,y] is the vector generating by the mouse movement (in the plane of the screen)
		# Rotation occurs about the vector 90 degrees to [x,y,0]
		# The amount of rotation is linealy proportional to the length of [x,y]
		
		if ( x == 0 and y == 0): return
		
		theta = atan2(-y,x)

		rotaxis_x = sin(theta)
		rotaxis_y = cos(theta)
		rotaxis_z = 0
		
		length = sqrt(x*x + y*y)
		# 8.0 is a magic number - things rotate more if they are closer and slower if they are far away in this appproach
		# Or does it?
		# This magic number could be overcome using a strategy based on the results of get_render_dims_at_depth
		angle = length/8.0*pi
		
		t3d = Transform3D()
		quaternion = {}
		quaternion["Omega"] = angle
		quaternion["n1"] = rotaxis_x
		quaternion["n2"] = rotaxis_y
		quaternion["n3"] = rotaxis_z
		
		t3d.set_rotation( EULER_SPIN, quaternion )
		
		size = len(self.t3d_stack)
		self.t3d_stack[size-1] = t3d*self.t3d_stack[size-1]
		
	def set_scale(self,val):
		self.scale = val
	
	def load_rotation(self,t3d):
		self.t3d_stack.append(t3d)

	def get_thin_copy(self):
		# this is called a thin copy because it does not copy the entire t3d stack, just the last t3d
		cam = Camera()
		size = len(self.t3d_stack)
		cam.load_rotation(self.t3d_stack[size-1])
		
		cam.scale =	self.scale
		cam.cam_x = self.cam_x
		cam.cam_y = self.cam_y
		cam.cam_z = self.cam_z
		
		cam.default_x = self.default_x
		cam.default_y = self.default_y
		cam.default_z = self.default_z
		
		return cam

class EMBrightContrastScreen:
	def __init__(self):
		# this class draws a brightness/contrast screen on the zplane,
		# on a square polygon from [0,0] to [1,1]
		self.glcontrast = 1.0
		self.glbrightness = 0.0

	def set_GL_brightness(self,val):
		self.glbrightness = val
		
	def set_GL_contrast(self,val):
		self.glcontrast = val

	def draw_bc_screen(self):
		if (self.glcontrast == 1 and self.glbrightness == 0 ): return
		
		lighting = glIsEnabled(GL_LIGHTING)
		cull = glIsEnabled(GL_CULL_FACE)
		depth = glIsEnabled(GL_DEPTH_TEST)
		blend = glIsEnabled(GL_BLEND)
		
		polygonmode = glGetIntegerv(GL_POLYGON_MODE)

		glDisable(GL_LIGHTING)
		glDisable(GL_CULL_FACE)
		glDisable(GL_DEPTH_TEST)
		
		glShadeModel(GL_SMOOTH)

		glEnable(GL_BLEND)
		glDepthMask(GL_FALSE)
		if ( self.glcontrast > 1 ):
			glBlendFunc(GL_ONE, GL_ONE)
			if self.glbrightness > 0 :
				glBlendEquation(GL_FUNC_ADD);
				glColor4f(self.glbrightness,self.glbrightness,self.glbrightness,1.0)
			else:
				glBlendEquation(GL_FUNC_REVERSE_SUBTRACT);
				glColor4f(-self.glbrightness,-self.glbrightness,-self.glbrightness, 1.0)
			
			glBegin( GL_QUADS )
			glVertex(0, 0)
			glVertex(1, 0)
			glVertex2f(1, 1)
			glVertex2f(0, 1)
			glEnd()
		
			glBlendFunc(GL_DST_COLOR, GL_ONE)
			glBlendEquation(GL_FUNC_ADD)
			
			tmpContrast = self.glcontrast
	
			while ( tmpContrast > 2 ):
				glColor4f(1.0,1.0,1.0,1.0)
				glBegin( GL_QUADS );
				glVertex2f(0, 0)
				glVertex2f(1, 0)
				glVertex2f(1, 1)
				glVertex2f(0, 1)
				glEnd()
				tmpContrast /= 2;
			
	
			glBlendFunc(GL_DST_COLOR, GL_ONE)
			glBlendEquation(GL_FUNC_ADD)
			glColor4f(tmpContrast-1.0,tmpContrast-1.0,tmpContrast-1.0,1.0)
			glBegin( GL_QUADS )
			glVertex2f(0, 0)
			glVertex2f(1, 0)
			glVertex2f(1, 1)
			glVertex2f(0, 1)
			glEnd()
		else:
			if self.glbrightness > 0:
				glBlendEquation(GL_FUNC_ADD)
				glColor4f(self.glbrightness,self.glbrightness,self.glbrightness,self.glcontrast)
			else:
				glBlendEquation(GL_FUNC_REVERSE_SUBTRACT);
				glColor4f(-self.glbrightness,-self.glbrightness,-self.glbrightness,self.glcontrast)
				
			glBlendFunc(GL_ONE, GL_SRC_ALPHA)

			glBegin( GL_QUADS )
			glVertex2f(0, 0)
			glVertex2f(1, 0)
			glVertex2f(1, 1)
			glVertex2f(0, 1)
			glEnd()
		
		glDepthMask(GL_TRUE)
	
		if ( lighting ): glEnable(GL_LIGHTING)
		if ( cull ): glEnable(GL_CULL_FACE)
		if ( depth ): glEnable(GL_DEPTH_TEST)
		if ( not blend ): glDisable(GL_BLEND)
		
		if ( polygonmode[0] == GL_LINE ): glPolygonMode(GL_FRONT, GL_LINE)
		if ( polygonmode[1] == GL_LINE ): glPolygonMode(GL_BACK, GL_LINE)

def draw_volume_bounds(width,height,depth):
	glLineWidth(0.2)
	glNormal(0,1,0)
	glColor(.2,.1,0.4,1.0)
	glColor(1,1,1,1.0)
	glMaterial(GL_FRONT, GL_AMBIENT, [1, 1, 1,1.0])
	glMaterial(GL_FRONT, GL_DIFFUSE, [1, 1, 1,1.0])
	glMaterial(GL_FRONT, GL_SPECULAR, [0.774597, 0.774597, 0.774597,1.0])
	glMaterial(GL_FRONT, GL_SHININESS, 128.0)

	glBegin(GL_LINE_STRIP)
	glVertex(0,0,0)
	glVertex(width,0,0)
	glVertex(width,0,depth)
	glVertex(0,0,depth)
	glVertex(0,0,0)
	glVertex(0,height,0)
	glVertex(width,height,0)
	glVertex(width,height,depth)
	glVertex(0,height,depth)
	glVertex(0,height,0)
	glEnd()
	
	glBegin(GL_LINES)
	glVertex(width,height,depth)
	glVertex(width,0,depth)
	
	glVertex(width,height,0)
	glVertex(width,0,0)
	
	glVertex(0,height,depth)
	glVertex(0,0,depth)
	glEnd()

class EMImage2DGUIModule(EMGUIModule):
	def __init__(self,application=None):
		EMGUIModule.__init__(self,application)
		self.em_qt_inspector_widget = None # shoudl be = EMQtWidgetModule(application) somewher 
		self.suppress_inspector = False # turn on to suppress showing the inspector
		self.inspector = None # this should be a qt widget, otherwise referred to as an inspector in eman
	
	def get_inspector(self): raise # this need to be supplied
	
	def show_inspector(self,force=0):
		
		if self.application == None:
			print "can't show an inspector with having an associated application"
		
		if self.suppress_inspector: return
		if not force and self.inspector==None : return
		if not self.inspector : 
			self.inspector = self.get_inspector()
			if self.inspector == None: return # sometimes this happens
		if not self.em_qt_inspector_widget:
			self.em_qt_inspector_widget = EMQtWidgetModule(self.inspector,self.application)
		
		self.application.show_specific(self.em_qt_inspector_widget)

	def set_parent(self,parent): self.parent = parent
	def get_parent(self): return self.parent
		
		
	def closeEvent(self,event) :
		if self.inspector: self.inspector.close()
		
	def mouseDoubleClickEvent(self,event):
		pass

class EMImage3DGUIModule(EMGUIModule):
	def __init__(self,application=None):
		EMGUIModule.__init__(self,application)
		self.em_qt_inspector_widget = None # shoudl be = EMQtWidgetModule(application) somewher 
		
		self.blendflags = EMOpenGLFlagsAndTools()
		self.bcscreen = EMBrightContrastScreen()
		
		self.inspector = None # this should be a qt widget, otherwise referred to as an inspector in eman lingo
		self.name = None # a name variable, accessed by set and get
		self.rand = None # a rand varaible
		self.cam = None # should be a camera, either Camera or Camera2
		self.cube = False # whether a cube should be drawn
		self.suppress_inspector = False # turn on to suppress showing the inspector
		
		self.parent = None # should be something that accepts UpdateGL calls
		self.data = None # should eventually be an EMData object
		self.file_name = None # stores the file name of the associated EMData, if applicable (use setter/getter)
		self.help_window = None # eventually will become a Qt help widget of some kind
		
	def render(self): pass # should do the main drawing
	def updateGL(self): raise #this needs to be supplied
	def get_type(self): pass #should return a unique string
	def get_inspector(self): raise # this need to be supplied
	
	def set_parent(self,parent): self.parent = parent
	def get_parent(self): return self.parent
	def set_rank(self,rank): self.rank = rank
	def set_name(self, name): self.name = name
	def get_name(self): return self.name
	def set_file_name(self,file_name): self.file_name = file_name
	def get_file_name(self): return self.file_name
	
	def show_inspector(self,force=0):
		
		if self.application == None:
			print "can't show an inspector with having an associated application"
		
		if self.suppress_inspector: return
		if not force and self.inspector==None : return
		
		if not self.inspector : 
			self.inspector = self.get_inspector()
		if not self.em_qt_inspector_widget:
			self.em_qt_inspector_widget = EMQtWidgetModule(self.inspector,self.application)
		
		self.application.show_specific(self.em_qt_inspector_widget)

	
	def get_current_camera(self): return self.cam.get_thin_copy()
	
	def set_camera(self,camera): self.cam = camera
	
	def scale_event(self,delta):
		self.cam.scale_event(delta)
		if self.inspector: self.inspector.set_scale(self.cam.scale)

	def get_translate_scale(self):
	
		[rx,ry] = self.parent.get_render_dims_at_depth(self.cam.cam_z)
		
		#print "render area is %f %f " %(xx,yy)
		xscale = rx/float(self.parent.width())
		yscale = ry/float(self.parent.height())
		
		return [xscale,yscale]
	
	def motion_translate(self,x,y):
		[xscale,yscale] = self.get_translate_scale()
		self.cam.cam_x += x*xscale
		self.cam.cam_y += y*yscale
		self.inspector.set_xy_trans(self.cam.cam_x, self.cam.cam_y)

	
	def get_current_transform(self):
		size = len(self.cam.t3d_stack)
		return self.cam.t3d_stack[size-1]

	def set_cam_z(self,z):
		self.cam.set_cam_z( z )
		self.updateGL()
		
	def set_cam_y(self,y):
		self.cam.set_cam_y( y )
		self.updateGL()
		
	def set_cam_x(self,x):
		self.cam.set_cam_x( x )
		self.updateGL()
		
	def motion_rotate(self,x,y):
		self.cam.motion_rotate(x,y)
		size = len(self.cam.t3d_stack)
		self.update_inspector(self.cam.t3d_stack[size-1])
		
	def set_scale(self,val):
		self.cam.scale = val
		self.updateGL()
	
	def load_rotation(self,t3d):
		self.cam.t3d_stack.append(t3d)
		self.updateGL()
		
	def resizeEvent(self):
		if self.inspector == None: return
		[xscale,yscale] = self.get_translate_scale()
		if ( xscale > yscale ): self.inspector.set_translate_scale(xscale,yscale,yscale)
		else: self.inspector.set_translate_scale(xscale,yscale,xscale)
		
	def draw_bc_screen(self):
		self.bcscreen.draw_bc_screen()

	def set_GL_contrast(self,val):
		self.bcscreen.set_GL_contrast(val)
		try:
			self.updateGL()
		except:
			# the parent may not have been set
			pass
	
	def set_GL_brightness(self,val):
		self.bcscreen.set_GL_brightness(val)
		try:
			self.updateGL()
		except:
			# the parent may not have been set
			pass
		
	def draw_volume_bounds(self):
		# FIXME - should be a display list
		width = self.data.get_xsize()
		height = self.data.get_ysize()
		depth = self.data.get_zsize()
		glTranslate(-width/2.0,-height/2.0,-depth/2.0)
		draw_volume_bounds(width,height,depth)
	
	def toggle_cube(self):
		self.cube = not self.cube
		self.updateGL()
		
		
	def closeEvent(self,event) :
		if self.inspector: self.inspector.close()
		
	def mousePressEvent(self, event):
#		lc=self.scrtoimg((event.x(),event.y()))
		if event.button()==Qt.MidButton:
			if not self.inspector or self.inspector ==None:
				return
			self.inspector.update_rotations(self.cam.t3d_stack[len(self.cam.t3d_stack)-1])
			self.inspector.set_xy_trans(self.cam.cam_x,self.cam.cam_y)
			self.inspector.set_scale(self.cam.scale)
			self.resizeEvent()
			self.show_inspector(1)
		else:
			self.cam.mousePressEvent(event)
			
		
		
		self.updateGL()
	
	def mouseDoubleClickEvent(self,event):
		pass
	
	def mouseMoveEvent(self, event):
		self.cam.mouseMoveEvent(event)
		if self.inspector != None:
			if event.buttons()&Qt.LeftButton:
				self.inspector.update_rotations(self.get_current_transform())
			elif event.buttons()&Qt.RightButton:
				self.inspector.set_xy_trans(self.cam.cam_x,self.cam.cam_y)
				
		self.updateGL()
	
	def mouseReleaseEvent(self, event):
		self.cam.mouseReleaseEvent(event)
		self.updateGL()
			
	def wheelEvent(self, event):
		self.cam.wheelEvent(event)
		if self.inspector != None :
			self.inspector.set_scale(self.cam.scale)
		self.updateGL()
		
	def keyPressEvent(self,event):
		
		if event.key() == Qt.Key_F1:
			if self.help_window == None:
				try:	
					help = QtWebKit.QWebView()
					help.load(QtCore.QUrl("http://blake.bcm.edu/emanwiki/e2display"))
					
				except:
					print "in the middle of getting help working"
					help = QtGui.QTextBrowser()
					#url = QtCore.QUrl("http://blake.bcm.edu/emanwiki/e2display")
					url = QtCore.QUrl("http://www.google.com")
					url.setPort(80)
					#print url.port()
					help.setSource(url)
					#print browser2.port()
	
				self.help_window = EMQtWidgetModule(help,self.application)
				#help.resize(640,640)
		
		self.application.show_specific(self.help_window)
				
		
def get_default_gl_colors():
	ruby = {}
	ruby["ambient"] = [0.1745, 0.01175, 0.01175,1.0]
	ruby["diffuse"] = [0.61424, 0.04136, 0.04136,1.0]
	ruby["specular"] = [0.927811, 0.826959, 0.826959,1.0]
	ruby["shininess"] = 32
	ruby["emission"] = [0,0,0]
	
	emerald = {}
	emerald["ambient"] = [0.0215, 0.1745, 0.0215,1.0]
	emerald["diffuse"] = [0.07568, 0.61424,  0.07568,1.0]
	emerald["specular"] = [0.833, 0.927811, 0.833,1.0]
	emerald["shininess"] = 32
	emerald["emission"] = [0,0,0]
	
	pearl = {}
	pearl["ambient"] = [0.25, 0.20725, 0.20725,1.0]
	pearl["diffuse"] = [1.0, 0.829, 0.829,1.0]
	pearl["specular"] = [0.296648, 0.296648, 0.296648,1.0]
	pearl["shininess"] = 128.0
	pearl["emission"] = [0,0,0]
	
	silver = {}
	silver["ambient"] = [0.25, 0.25, 0.25,1.0]
	silver["diffuse"] = [0.4, 0.4, 0.4,1.0]
	silver["specular"] = [0.974597, 0.974597, 0.974597,1.0]
	silver["shininess"] = 4
	silver["emission"] = [0.1,0.1,0.1]
	
	gold = {}
	gold["ambient"] = [0.24725, 0.2245, 0.0645,1.0]
	gold["diffuse"] = [0.34615, 0.3143, 0.0903,1.0]
	gold["specular"] = [1.000, 0.9079885, 0.26086934,1.0]
	gold["shininess"] = 4
	gold["emission"] = [0,0,0]
	
	copper = {}
	copper["ambient"] = [0.2295, 0.08825, 0.0275,1.0]
	copper["diffuse"] = [0.5508, 0.2118, 0.066,1.0]
	copper["specular"] = [0.9, 0.5, 0.2,1.0]
	copper["shininess"] = 20.0
	copper["emission"] = [0,0,0]
	
	obsidian = {}
	obsidian["ambient"] = [0.05375,  0.05,     0.06625 ,1.0]
	obsidian["diffuse"] = [0.18275,  0.17,     0.22525,1.0]
	obsidian["specular"] = [0.66, 0.65, 0.69]
	obsidian["shininess"] = 128.0
	obsidian["emission"] = [0,0,0]
	
	turquoise = {}
	turquoise["ambient"] = [0.1, 0.18725, 0.1745 ,1.0]
	turquoise["diffuse"] = [0.396, 0.74151, 0.69102,1.0]
	turquoise["specular"] = [0.297254, 0.30829, 0.306678]
	turquoise["shininess"] = 128.0
	turquoise["emission"] = [0,0,0]
	
	yellow = {}
	yellow["ambient"] = [0.3, 0.3, 0.0,1]
	yellow["diffuse"] = [0.5, 0.5, 0.0,1]
	yellow["specular"] = [0.7, 0.7, 0.0,1]
	yellow["shininess"] =  60
	yellow["emission"] = [0,0,0]
	
	custom = {}
	custom["custom"] = [0.3, 0.3, 0.0,1]
	custom["custom"] = [0.5, 0.5, 0.0,1]
	custom["custom"] = [0.7, 0.7, 0.0,1]
	custom["custom"] =  60
	custom["emission"] = [0,0,0]
	
	colors = {}
	colors["ruby"] = ruby
	colors["emerald"] = emerald
	colors["pearl"] = pearl
	colors["silver"] = silver
	colors["gold"] = gold
	colors["copper"] = copper
	colors["obsidian"] = obsidian
	colors["turquoise"] = turquoise
	colors["yellow"] = yellow
	colors["custom"] = yellow
	
	return colors

