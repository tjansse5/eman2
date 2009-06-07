#!/usr/bin/env python
#
# Author: David Woolford 11/10/08 (woolford@bcm.edu)
# Copyright (c) 2000-2008 Baylor College of Medicine
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


from emsprworkflow import *
from emform import *
from emsave import EMFileTypeValidator

class EMTomoRawDataReportTask(EMRawDataReportTask):
	'''This form displays tomograms that are associated with the project. You browse to add raw data, or right click and choose Add.''' 
	def __init__(self):
		EMRawDataReportTask.__init__(self)
		self.project_list = "global.tpr_tomograms"
		
	def get_raw_data_table(self):
		'''
		Gets an EMTomographicFileTable - this is type of class that the emform knows how to handle 
		'''
		project_db = db_open_dict("bdb:project")
		project_names = project_db.get(self.project_list,dfl=[])
		self.project_files_at_init = project_names # so if the user hits cancel this can be reset

		from emform import EMTomographicFileTable,EMFileTable
		table = EMTomographicFileTable(project_names,desc_short="Tomograms",desc_long="")
		context_menu_data = EMRawDataReportTask.ProjectListContextMenu(self.project_list)
		table.add_context_menu_data(context_menu_data)
		table.add_button_data(EMRawDataReportTask.ProjectAddRawDataButton(table,context_menu_data))
	
		#p.append(pdims) # don't think this is really necessary
		return table,len(project_names)

class EMReconstructAliFile(WorkFlowTask):
	'''Use this task for reconstructing IMOD ali into 3D volumes using EMAN2's Fourier reconstructor. This requires you to supply the tlt file and ali files that are generated by IMOD.'''

	def __init__(self):
		WorkFlowTask.__init__(self)
		self.window_title = "Reconstruct ALI File"
		self.preferred_size = (640,480)
		self.form_db_name = "bdb:emform.reconstruct_ali"
		
	def get_params(self):
		params = []
		db = db_open_dict(self.form_db_name)
		
		plot_table = EMPlotTable(name="tltfile",desc_short="TLT file",desc_long="Use this tool to browse for your tlt file",single_selection=True)
		ali_table = EMTomographicFileTable(name="alifile",desc_short="ALI file",desc_long="Use this tool to browse for your ali file",single_selection=True)
		
		
		context_menu_data = ParticleWorkFlowTask.DataContextMenu(EMFileTypeValidator("ali"))
		ali_table.add_context_menu_data(context_menu_data)
		ali_table.add_button_data(ParticleWorkFlowTask.AddDataButton(ali_table,context_menu_data))
		
		context_menu_data2 = ParticleWorkFlowTask.DataContextMenu(EMFileTypeValidator("tlt"))
		plot_table.add_context_menu_data(context_menu_data2)
		plot_table.add_button_data(ParticleWorkFlowTask.AddDataButton(plot_table,context_menu_data2))

		ali_table.add_column_data(EMFileTable.EMColumnData("Image Dims",ParticleReportTask.get_particle_dims,"The dimensions of the image on disk"))
		plot_table.add_column_data(EMFileTable.EMColumnData("Rows",EMPlotTable.num_plot_entries,"The number of lines in the file"))
		
		xsample = ParamDef(name="xsample",vartype="int",desc_short="X Sampling",desc_long="The size of the x dimension of the reconstructed volume",property=None,defaultunits=db.get("xsample",dfl=0),choices=None)
		ysample = ParamDef(name="ysample",vartype="int",desc_short="Y Sampling",desc_long="The size of the y dimension of the reconstructed volume",property=None,defaultunits=db.get("ysample",dfl=0),choices=None)
		zsample = ParamDef(name="zsample",vartype="int",desc_short="Z Sampling",desc_long="The size of the z dimension of the reconstructed volume",property=None,defaultunits=db.get("zsample",dfl=0),choices=None)
		
		params.append(ParamDef(name="blurb",vartype="text",desc_short="Reconstructing and ALI file",desc_long="",property=None,defaultunits=self.__doc__,choices=None))
		params.append([ali_table,plot_table])
		params.append([xsample,ysample,zsample])
		return params

	
	def check_params(self,params):
		error_msg = []
		for sample in ["xsample","ysample","zsample"]:
			if params[sample] <= 0:
				error_msg.append("%s must be greater than zero" %sample)
				
		tltok = True
		if not params.has_key("tltfile") or len(params["tltfile"]) != 1:
			error_msg.append("You have to supply a single TLT file")
			tltok = False
		else:
			try:
				f = file(params["tltfile"][0],"r")
				lines = f.readlines()
				n_lines = len(lines)
			except:
				error_msg.append("The TLT file is not recognized")
				tltok = False
		
		aliok = True
		if not params.has_key("alifile") or len(params["alifile"]) != 1:
			error_msg.append("You have to supply a single ALI file")
			aliok = False
		else:
			try:
				nx,ny,nz = gimme_image_dimensions3D(params["alifile"][0])
			except:
				error_msg.append("The ALI file is not recognized")
				aliok = False
			
		if aliok and tltok:
			if nz != n_lines:
				error_msg.append("The z dimension of the ALI file (%d) has to match the number of lines in the TLT file (%d)" %(nz,n_lines))
	
		return error_msg
	
	def get_output_name(self):
		tag = "bdb:tomograms#tomogram_"
		
		if not os.path.isdir("tomograms"):
			os.makedirs("tomograms") 
		
		idx = 0
		while 1:
			sidx = str(idx)
			if len(sidx) == 1:
				sidx = "0" + sidx
				
			name = tag + sidx
			print name
			if not db_check_dict(name): break
			
		return name
	
	def on_form_ok(self,params):
		
		error_message = self.check_params(params)
		if len(error_message):
			self.show_error_message(error_message)
			return
		
		options = EmptyObject()
		options.input = params["alifile"][0]
		options.tlt = params["tltfile"][0]
		options.dbls = "global.tpr_tomograms"
		options.output = self.get_output_name()
		options.recon = "fourier:xsample=%s:ysample=%s:zsample=%s" %(params["xsample"],params["ysample"],params["zsample"])
		options.preprocess = "normalize.edgemean"
		options.iter = "0"
		options.sym = "c1"
		
		string_args = ["input","tlt","recon","preprocess","iter","sym","output","dbls"]
		bool_args = []
		additional_args = ["--lowmem"]
		temp_file_name = "e2make3d_stdout.txt"
		self.spawn_single_task('e2make3d.py',options,string_args,bool_args,additional_args,temp_file_name)
		
		
		self.write_db_entries(params)
		self.emit(QtCore.SIGNAL("task_idle"))
		self.form.closeEvent(None)
		self.form = None

class EMTomohunterTask(WorkFlowTask):
	'''Use this task for running e2tomohunter.py from the workflow'''
	
	# written by Grant Tang
	documentation_string = "This is useful information about this task."

	def __init__(self):
		WorkFlowTask.__init__(self)
		self.window_title = "Tomohunter Input Form"
		self.preferred_size = (640,480)
	def get_params(self):
		params = []
		project_db = db_open_dict("bdb:tomography")
		params.append(ParamDef(name="blurb",vartype="text",desc_short="SPR",desc_long="Information regarding this task",property=None,defaultunits=self.__doc__,choices=None))
		targetimage = ParamDef(name="targetimage",vartype="url",desc_short="target image file name",desc_long="target image file name",property=None,defaultunits=project_db.get("targetimage",dfl=[]),choices=[])
		probeimage = ParamDef(name="probeimage",vartype="url",desc_short="probe image file name",desc_long="probe image file name",property=None,defaultunits=project_db.get("probeimage",dfl=[]),choices=[])
		norm = ParamDef(name="normalization",vartype="int",desc_short="normalization",desc_long="if the normalization needed",property=None,defaultunits=0,choices=[0,1])
		nsoln = ParamDef(name="nsoln",vartype="int",desc_short="#solution",desc_long="number of solution",property=None,defaultunits=1,choices=None)
		thresh = ParamDef(name="thresh",vartype="float",desc_short="threshold",desc_long="threshold",property=None,defaultunits=1.0,choices=None)
		searchx = ParamDef(name="searchx",vartype="int",desc_short="searchx",desc_long="searchx",property=None,defaultunits=0,choices=None)
		searchy = ParamDef(name="searchy",vartype="int",desc_short="searchy",desc_long="searchy",property=None,defaultunits=0,choices=None)
		searchz = ParamDef(name="searchz",vartype="int",desc_short="searchz",desc_long="searchz",property=None,defaultunits=0,choices=None)
		ralt = ParamDef(name="ralt",vartype="float",desc_short="ralt",desc_long="Altitude range",property=None,defaultunits=180.0,choices=None)
		dalt = ParamDef(name="dalt",vartype="float",desc_short="dalt",desc_long="Altitude delta",property=None,defaultunits=10.0,choices=None)
		daz = ParamDef(name="daz",vartype="float",desc_short="daz",desc_long="Azimuth delta",property=None,defaultunits=10.0,choices=None)
		rphi = ParamDef(name="rphi",vartype="float",desc_short="rphi",desc_long="Phi range",property=None,defaultunits=180.0,choices=None)
		dphi = ParamDef(name="dphi",vartype="float",desc_short="dphi",desc_long="Phi delta",property=None,defaultunits=10.0,choices=None)
		params.append([targetimage,probeimage])
		params.append([norm,thresh,nsoln])
		params.append([searchx,searchy,searchz])
		params.append([ralt,dalt,daz,rphi,dphi])
		#db_close_dict("bdb:project")
		return params

	def write_db_entry(self,key,value):
		WorkFlowTask.write_db_entry(self,key,value)
	
	def check_params(self,params):
		error_msg = []
		if len(params["targetimage"]) != 1: error_msg.append("Please choose a single target file to proceed")
		if len(params["probeimage"]) != 1: error_msg.append("Please choose a single probe file to proceed")
		return error_msg
	
	def on_form_ok(self,params):
		print params
		
		error_message = self.check_params(params)
		if len(error_message):
			self.show_error_message(error_message)
			return
		
		self.write_db_entries(params) # will only write filenames
		options = EmptyObject()
		string_args = ["dalt","ralt","dphi","rphi","raz","daz","thresh","nsoln","searchx","searchy","searchz"]
		options.filenames = [params['targetimage'][0], params['probeimage'][0]]
		options.dalt = params['dalt']
		options.ralt = params['ralt']
		options.dphi = params['dphi']
		options.rphi = params['rphi']
		options.raz = params['ralt']
		options.daz = params['dalt']
		options.thresh = params['thresh']
		options.nsoln = params['nsoln']
		options.searchx = params['searchx']
		options.searchy = params['searchy']
		options.searchz = params['searchz']
		bool_args = []
		additional_args = []
		temp_file_name = "e2tomohunter_stdout.txt"
		self.spawn_single_task('e2tomohunter.py',options,string_args,bool_args,additional_args,temp_file_name)
		self.emit(QtCore.SIGNAL("task_idle"))
		self.form.closeEvent(None)
		self.form = None
		
class EMTomoParticleReportTask(WorkFlowTask):
	"""This form display the boxed tomographic particles that you currently have associated with the project"""
	def __init__(self):
		WorkFlowTask.__init__(self)

	def get_project_particle_table(self):
		project_db = db_open_dict("bdb:project")
		particle_list_name = "global.tpr_ptcls"
		particle_names = project_db.get(particle_list_name,dfl=[])
		self.project_files_at_init = particle_names # so if the user hits cancel this can be reset

		from emform import EM3DFileTable,EMFileTable
		table = EM3DFileTable(particle_names,desc_short="Boxed Tomographic Particles",desc_long="")
		context_menu_data = EMRawDataReportTask.ProjectListContextMenu(particle_list_name)
		table.add_context_menu_data(context_menu_data)
		table.add_button_data(EMRawDataReportTask.ProjectAddRawDataButton(table,context_menu_data))
	#	table.insert_column_data(1,EMFileTable.EMColumnData("Particles On Disk",ParticleReportTask.get_num_ptcls,"Particles currently stored on disk that are associated with this image"))
		table.insert_column_data(2,EMFileTable.EMColumnData("Particle Dims",ParticleReportTask.get_particle_dims,"The dimensions of the particles that are stored on disk"))
		
		return table
	
	def get_params(self):
		params = []
		
	
		table = self.get_project_particle_table()
		
		params.append(ParamDef(name="blurb",vartype="text",desc_short="",desc_long="",property=None,defaultunits=self.__doc__,choices=None))
		params.append(table)  
		
		return params

class E2TomoBoxerGuiTask(WorkFlowTask):
	"""Select the file you want to process and hit okay, this will launch e2tomoboxer"""
	
	def __init__(self):
		WorkFlowTask.__init__(self)
		self.tomo_boxer_module = None
	
	def get_tomo_boxer_basic_table(self):
		'''
		'''
		
		self.report_task = EMTomoRawDataReportTask()
		table,n = self.report_task.get_raw_data_table()# now p is a EMParamTable with rows for as many files as there in the project
		from emform import EMFileTable
		table.insert_column_data(0,EMFileTable.EMColumnData("Stored Boxes",E2TomoBoxerGuiTask.get_tomo_boxes_in_database,"Boxes currently stored in the EMAN2 database"))
		
		return table, n

	def get_tomo_boxes_in_database(name):
		from e2tomoboxer import tomo_db_name
		if db_check_dict(tomo_db_name):
			tomo_db = db_open_dict(tomo_db_name)
			image_dict = tomo_db.get(get_file_tag(name),dfl={})
			print "name is ",name
			if image_dict.has_key("coords"):
				return str(len(image_dict["coords"]))
		
		return "0"
	
	get_tomo_boxes_in_database = staticmethod(get_tomo_boxes_in_database)
	
	def get_params(self):
		params = []
		
		p,n = self.get_tomo_boxer_basic_table() # note n is unused, it's a refactoring residual		
		params.append(ParamDef(name="blurb",vartype="text",desc_short="Interactive use of e2tomoboxer",desc_long="",property=None,defaultunits=self.__doc__,choices=None))
		params.append(p)
#		db = db_open_dict(self.form_db_name)
#		params.append(ParamDef(name="interface_boxsize",vartype="int",desc_short="Box size",desc_long="An integer value",property=None,defaultunits=db.get("interface_boxsize",dfl=128),choices=[]))
#		#db_close_dict(self.form_db_name)
		return params
	
	def on_form_ok(self,params):
		
		if not params.has_key("filenames"):
			EMErrorMessageDisplay.run(["Please select files for processing"])
			return
		
		if  params.has_key("filenames") and len(params["filenames"]) == 0:
			EMErrorMessageDisplay.run(["Please select files for processing"])
			return

		self.write_db_entries(params)

		from e2tomoboxer import EMTomoBoxerModule
		self.tomo_boxer_module = EMTomoBoxerModule(params["filenames"][0])
		self.emit(QtCore.SIGNAL("gui_running"),"e2TomoBoxer",self.tomo_boxer_module) # The controlled program should intercept this signal and keep the E2BoxerTask instance in memory, else signals emitted internally in boxer won't work
		
		QtCore.QObject.connect(self.tomo_boxer_module, QtCore.SIGNAL("module_idle"), self.on_boxer_idle)
		QtCore.QObject.connect(self.tomo_boxer_module, QtCore.SIGNAL("module_closed"), self.on_boxer_closed)
		self.form.closeEvent(None)
		self.tomo_boxer_module.show_guis()
		self.form = None
			
	def write_db_entires(self,params):
		pass

	def on_boxer_idle(self):pass
	def on_boxer_closed(self):pass
	