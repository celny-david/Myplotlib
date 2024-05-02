# -*- coding: utf-8 -*-
"""
Fig_data provides the encapsulation of the figure data that is recognised in MyPlotLib. Class provide passing mechanism to matplotlib commands,
"""

# Built-in/Generic Imports
from sigtools import specifiers
# import re
from copy import deepcopy
# Libs
import matplotlib.pyplot as plt
# own
import utilities as util

#=== GLOBAL ===
curr_figure = None
curr_axes = None

class Fig_data:

	def _fill_sections(self):
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html
		self.figure_keys = {
						'num':'',\
						'figsize':None,\
					    'dpi':None,\
					    'layout':None,\
					    'linewidth':0.0,\
						'facecolor':None,\
						'edgecolor':None,\
						'frameon':True,\
						'clear':False,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xlim.html
		self.xlim_keys = {
						'is_used':False,\
						'left':None,\
						'right':None,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.ylim.html
		self.ylim_keys = {
						'is_used':False,\
						'top':None,\
						'bottom':None,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xticks.html
		self.xticks_keys = {
						'is_used':False,\
						'ticks':None,\
						'labels':None,\
						'minor':False,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.yticks.html
		self.yticks_keys = {
						'is_used':False,\
						'ticks':None,\
						'labels':None,\
						'minor':False,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xlabel.html
		self.xlabel_keys = {
						'is_used':False,\
						'xlabel':'Default',\
						'loc':'center',\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.ylabel.html
		self.ylabel_keys = {
						'is_used':False,\
						'ylabel':'Default',\
						'loc':'center',\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.title.html
		self.title_keys = { 
						'is_used':False,\
						'label':'Default title',\
						'loc':'center',\
						'pad':6.0,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.suptitle.html
		self.suptitle_keys = {
						'is_used':False,\
						't':'Default suptitle',\
						'x':0.5,\
						'y':0.98,\
		}
		#NOTE default taken from: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
		self.legend_keys = {
						'is_used':False,\
						'loc':'best',\
						#BEWARE bbox_to_anchor has unknown deafult value -> may break when not set 
						'bbox_to_anchor':None,\
						'title_fontsize':None,\
						'alignment':'center',\
		}
		#NOTE append axes 
		self.append_axes_keys = {
						'position':'right',\
						'size': '5%',\
						'pad': None,\
		}
		
		#NOTE additional colorbar
		self.append_axes_keys = {
						'position':'right',\
						'size': '5%',\
						'pad': None,\
		}

		#NOTE auxiliarry options
		self.other_keys = {
						'is_used':False,\
						'is_tight_layout': False,\
		}
		""" set up the subsection dictionary """
		self.sections = {
						'figure': self.figure_keys,\
						'xlim': self.xlim_keys,\
						'ylim': self.ylim_keys,\
						'xticks': self.xticks_keys,\
						'yticks': self.yticks_keys,\
						'xlabel': self.xlabel_keys,\
						'ylabel': self.ylabel_keys,\
						'title': self.title_keys,\
						'suptitle': self.suptitle_keys,\
						'legend': self.legend_keys,\
						'other': self.other_keys,\
		}

	@specifiers.forwards_to_function(plt.figure)
	def __init__(self):
		""" """
		#NOTE use the global variable
		# print(type(kwargs)) #DEBUG
		# print(kwargs) #DEBUG

		self.lines = []
		self.err_lines = []
		self._fill_sections()

	def to_mpl(self):
		""" provide own print to mpl"""
		str_out = "## figure\n"
		str_out += util.get_section_key_text(self.figure_keys)
		
		for section_name,section_dict in self.sections.items():
			if section_name == 'figure':
				#NOTE already printed preferentailly before
				continue
			str_out += "\n"
			str_out += f"## {section_name}\n"
			str_out += util.get_section_key_text(section_dict, preferential_keys = ['is_used']) 
		
		for cnt,line in enumerate(self.lines):
			str_out += "\n"
			str_out += line.to_mpl(cnt+1)

		for errcnt,errline in enumerate(self.err_lines):
			str_out += "\n"
			str_out += errline.to_mpl(errcnt+1)
		
		return str_out

	def plot_self(self):
		""" call the particular plt functions with the values in sections"""
		#NOTE handle situation with plt not realizing which figure is current
		#BEWARE hsi does not work
		# tmp_figure_keys = deepcopy(self.figure_keys)
		# tmp_figure_keys['clear'] = True
		#NOTE figure section
		plt.figure(**self.figure_keys)
		
		#NOTE line section
		for line in self.lines:
			line.plot_self()

		#NOTE errorline section
		for errline in self.err_lines:
			errline.plot_self()

		#NOTE xlim section
		kwargs = deepcopy(self.xlim_keys)
		if kwargs.pop("is_used"):			
			left = kwargs.pop('left')
			right = kwargs.pop('right')
			plt.xlim(left=left,right=right,**kwargs)
		#NOTE ylim section
		kwargs = deepcopy(self.ylim_keys)
		if kwargs.pop("is_used"):			
			bottom = kwargs.pop('bottom')
			top = kwargs.pop('top')
			plt.ylim(bottom=bottom,top=top,**kwargs)
		#NOTE xlim section
		kwargs = deepcopy(self.xticks_keys)
		if kwargs.pop("is_used"):			
			ticks = kwargs.pop('ticks')
			labels = kwargs.pop('labels')
			minor = kwargs.pop('minor')
			#BUG kwargs is not accepted and keyword args need to be used
			if bool(kwargs) is True:
				plt.xticks(kwargs,ticks=ticks,labels=labels,minor=minor) 
			else:
				plt.xticks(ticks=ticks,labels=labels,minor=minor) 
			# plt.xticks(kwargs)
		#NOTE yticks section
		kwargs = deepcopy(self.yticks_keys)
		if kwargs.pop("is_used"):			
			ticks = kwargs.pop('ticks')
			labels = kwargs.pop('labels')
			minor = kwargs.pop('minor')
			#BUG kwargs is not accepted and keyword args need to be used
			if bool(kwargs) is True:
				plt.yticks(kwargs,ticks=ticks,labels=labels,minor=minor) 
			else:
				plt.yticks(ticks=ticks,labels=labels,minor=minor) 
		#NOTE xlabel section
		kwargs = deepcopy(self.xlabel_keys)
		if kwargs.pop("is_used"):			
			xlabel = kwargs.pop('xlabel')
			plt.xlabel(fr"{xlabel}", **kwargs)
		#NOTE ylabel section
		kwargs = deepcopy(self.ylabel_keys)
		if kwargs.pop("is_used"):			
			ylabel = kwargs.pop('ylabel')
			plt.ylabel(fr"{ylabel}", **kwargs)
		#NOTE title section
		kwargs = deepcopy(self.title_keys)
		if kwargs.pop("is_used"):			
			label = kwargs.pop('label')
			plt.title(fr"{label}", **kwargs)
		#NOTE suptitle section
		kwargs = deepcopy(self.suptitle_keys)
		if kwargs.pop("is_used"):			
			t = kwargs.pop('t')
			plt.suptitle(fr"{t}", **kwargs)
		#NOTE legend section
		kwargs = deepcopy(self.legend_keys)
		# print("legend: ",kwargs['is_used']) #DEBUG
		if kwargs.pop("is_used") is True:
			#BEWARE args are not supported 
			try:
				# print(kwargs) #DEBUG
				# ax = plt.gca()
				# ax.legend_ = None
				plt.legend(**kwargs)
			except Exception as e:
				print(e)
				raise NotImplemented("Args are not yet supported by loading the mpl.legend")
		#NOTE tight layout swithc
		if self.other_keys['is_tight_layout'] is True:
			plt.tight_layout()

	# BUG cant currently handle the line processing
	# def from_mpl(self, section_name, line):
	# 	""" load section from mpl"""
	# 	if section_name not in self.sections.keys():
	# 		if section_name == 'figure':
	# 			#NOTE case of figure section
	# 			key,key_type,val,*rest = re.split(r':|=',line)
	# 			self.sections[section_name][key] = util.convert_to_type(key_type.rstrip(),val.lstrip()) 
	# 		elif section_name.find('## line') > -1: #NOTE it is line section
	# 			#NOTE case of line section
	# 			new_line = line()

	# 			self.lines.append(new_line)
	# 		else:
	# 			raise ValueError(f"Unknown section name {section_name}")
	# 	else:
	# 		key,key_type,val,*rest = re.split(r':|=',line)
	# 		self.sections[section_name][key] = util.convert_to_type(key_type.rstrip(),val.lstrip())
