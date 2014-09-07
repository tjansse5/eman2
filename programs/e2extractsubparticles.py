#!/usr/bin/env python

#
# Author: Steven Ludtke, 08/26/14 (sludtke@bcm.edu)
# Copyright (c) 2014- Baylor College of Medicine
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  2111-1307 USA
#
#

import os
import sys
import random
import time
import string
import math
from os import system
from os import unlink
from sys import argv
import traceback
from EMAN2 import *
from EMAN2db import db_open_dict

def main():
	progname = os.path.basename(sys.argv[0])
	usage = """prog [options] <refine_xx folder> <iteration number> <3D excluded region mask>

This program modifies raw particle data to subtract-away undesired portions of the density on a per-particle basis.
For example, one could take GroEL particles with D7 symmetry and extract the top and bottom heptamers as separate
particles for reconstruction. In this example there would be 2x as many output particles as input particles. The 
portion of the map identified by the excluded region mask will be subtracted from each particle as optimally as
possible, taking CTF, normalization and other factors into account. 

To use this program you should first run a complete refinement to the best possible resolution. Refinement parameters
will be examined automatically to extract the corresponding particles and projections.
"""
	parser = EMArgumentParser(usage=usage,version=EMANVERSION)
	parser.add_argument("--verbose", "-v", dest="verbose", action="store", metavar="n", type=int, default=0, help="verbose level [0-9], higner number means higher level of verboseness")
	parser.add_argument("--sym", dest = "sym", default="c1",help = "Specify symmetry - choices are: c<n>, d<n>, tet, oct, icos.", guitype='strbox', row=10, col=1, rowspan=1, colspan=1, mode="refinement")
	parser.add_argument("--debug",action="store_true",default=False,help="Enable debugging mode with verbose output and image display. Not suitable for real runs.")
	parser.add_argument("--ppid", type=int, help="Set the PID of the parent process, used for cross platform PPID",default=-1)
	#parser.add_argument("--ncls","-N",type=int,help="Number of classes to generate",default=-1)
	#parser.add_argument("--average","-A",action="store_true",help="Average the particles within each class",default=False)

	(options, args) = parser.parse_args()
	args[1]=int(args[1])
#	if len(args)<4 : parser.error("Please specify <raw particle file> <class mx> <projections> <mask> <output file> ")

	# each of these classmx variables becomes a 2 element list with even and odd particles respectively
	try:
		pathmx="{}/classmx_{:02d}_even.hdf".format(args[0],args[1])
		classmx=[EMData(pathmx,0)]
		nptcl=[classmx[0]["ny"]]
		cmxtx=[EMData(pathmx,2)]
		cmxty=[EMData(pathmx,3)]
		cmxalpha=[EMData(pathmx,4)]
		cmxmirror=[EMData(pathmx,5)]

		pathmx="{}/classmx_{:02d}_odd.hdf".format(args[0],args[1])
		classmx.append(EMData(pathmx,0))
		nptcl.append(classmx[1]["ny"])
		cmxtx.append(EMData(pathmx,2))
		cmxty.append(EMData(pathmx,3))
		cmxalpha.append(EMData(pathmx,4))
		cmxmirror.append(EMData(pathmx,5))
	except:
		traceback.print_exc()
		print "====\nError reading classification matrix. Must be full classification matrix with alignments"
		sys.exit(1)

	# path to the even/odd particles used for the refinement
	cptcl=js_open_dict("{}/0_refine_parms.json".format(args[0]))["input"]
	cptcl=[str(i) for i in cptcl]

	# this reads all of the EMData headers from the projections, should be same for even and odd
	pathprj="{}/projections_{:02d}_even.hdf".format(args[0],args[1])
	nref=EMUtil.get_image_count(pathprj)
	eulers=[EMData(pathprj,i,1)["xform.projection"] for i in range(nref)]

	# The 3D reference volume we are using for subtraction
	threed=EMData("{}/threed_{:02d}.hdf".format(args[0],args[1]),0)

	# The mask in "neutral" orientation
	mask=EMData(args[2],0)
	
	# The mask applied to the reference volume, used for 2-D masking of particles for better power spectrum matching
	ptclmask=EMData(args[0]+"/mask.hdf",0)

	logid=E2init(sys.argv, options.ppid)

	# We will need masked versions of our volume for all symmetric orientations
	# generate the symmetry transforms here for convenience
	xf = Transform()
	xf.to_identity()
	nsym=xf.get_nsym(options.sym)
	symxfs=[xf.get_sym(options.sym,i) for i in xrange(nsym)]

	# now we loop over the classes, and subtract away a projection of the reference with the exclusion mask in
	# each symmetry-related orientation, after careful scaling. Note that we don't have a list of which particle is in each class,
	# but rather a list of which class each particle is in, so we do this a bit inefficiently for now
	for i in xrange(nref):
		if options.verbose>1 : print "--- Class %d"%i
		
		# The first projection is unmasked, used for scaling
		# We regenerate the masked volumes for each class to avoid using too much RAM
		projs=[threed.project("standard",{"transform":eulers[i]})]
		for xf in symxfs:
			maskx=mask.process("xform",{"transform":xf})
			masked=threed.copy()
			masked.mult(maskx)
			projs.append(masked.project("standard",{"transform":eulers[i]}))
		
		projmask=ptclmask.project("standard",eulers[i])		# projection of the 3-D mask for the reference volume to apply to particles
#		proj.process_inplace("normalize.circlemean")
#		proj.mult(softmask)

		for eo in range(2):
			for j in range(nptcl[eo]):
				if classmx[eo][0,j]!=i : continue		# only proceed if the particle is in this class

				ptcl=EMData(cptcl[eo],j)
				
				# Find the transform for this particle (2d) and apply it to the unmasked/masked projections
				ptclxf=Transform({"type":"2d","alpha":cmxalpha[eo][0,j],"mirror":int(cmxmirror[eo][0,j]),"tx":cmxtx[eo][0,j],"ty":cmxty[eo][0,j]}).inverse()
				projc=[i.process("xform",{"transform":ptclxf}) for i in projs]		# we transform the projections, not the particle (as in the original classification)
				projmaskc=projmask.process("xform",{"transform":ptclxf})

				# we make a filtered copy of the particle filtered such that it's power spectrum is roughly that of a noise-free particle
				# we do this using an approximate filter from the particle set based CTF estimate, but apply this filter to the actual
				# particle image, so it will retain some of the detailed features of the actual particle power spectrum
				# The filter is basically (1-N/(N+S))
				ctf=ptcl["ctf"]
				ds=1.0/(ctf.apix*ptcl["ny"])
				filt=ctf.compute_1d(ptcl["ny"],ds,Ctf.CtfType.CTF_NOISERATIO,None)
				plot(filt)
				ptclr=ptcl.process("filter.radialtable",{"table":filt})		# reference particle for scaling
				ptclr.mult(projmaskc)
				
				# Now we match the radial structure factor of the total projection to the filtered particle, then scale
				# we will use the filter curve returned by this process to scale the masked projections, since theoretically
				# they should not match the whole particle
				projf=projc[0].process("filter.matchto",{"to":ptclr,"return_radial":1})
#				projf.process_inplace("normalize.toimage",{"to":ptcl})
				ptcl2=ptcl-projf
				
				display((projc[0],projf,ptclr,ptcl,ptcl2),True)






if __name__ == "__main__":
	main()