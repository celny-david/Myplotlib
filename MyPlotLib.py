#!/usr/bin/env python3
"""
My Plot Lib module conceptualizing the plot into structure that can be saved to JSON file.
 This way a plot can be retained without the need to recalculate. Additionally the data are
 readable and can be changed in the JSON file directly.
Currently supports:
 - simple plot using plot()
 - error plot using errorbar()
"""

# Futures
# from __future__ import print_function

# Built-in/Generic Imports
import os
import sys
import re
from copy import deepcopy
# own
import utilities as util
from utilities import get_curr_figure # useful helpers for user
from line import Line
from errline import ErrLine
from fig_data import Fig_data
# BEWARE importing all for convenience
from wrappers import *

#=== load/save functions ===
def save(filename, figure=None):
	""" save the figure to mpl filename"""
	#NOTE handle the case of saving other figures vs current figure
	figure = util.get_curr_figure_ifnone(figure)
	
	if filename[-4:] != '.mpl':
		filename += '.mpl'

	with open(filename,'w') as f:
		print(figure.to_mpl(),file=f)

def clear(filename):
	""" remove the existing file with .mpl extension"""
	if filename[-4:] != '.mpl':
		filename += '.mpl'
	
	if os.path.exists(filename) and os.path.isfile(filename):
		os.remove(filename)

def get_fig_name(filename):
	""" return the name of figure for preemtive check if figure of that name already exists"""
	if filename[-4:] != '.mpl':
		filename += '.mpl'

	try:
		f = open(filename, 'r')
		is_in_figure_section = False
		for readline in f.readlines():
			if len(readline) < 2:
				continue
			if readline.find('## figure') >-1:
				is_in_figure_section = True
			if is_in_figure_section:
				if readline[:4] == 'num:':
					_,_,val = re.findall(r'([\w\s]*):([\w\s]*)=(.*)',readline)[0]
					#NOTE found - return the name without the trailing whitespaces
					return val.rstrip()
		#NOTE no num found in figure section -> return None
		return None	

	except FileNotFoundError:
		#NOTE case the loading of nonexistent file - perform nothing
		if is_silent is False:
			print(f"WARNING: file {filename} not found -> nothing is loaded.")
		return None

def load(filename, alternative_figname = None, load_as_current=True, plot_self=True, is_silent=False):
	""" load the figure from mpl filename
		plot_self disable plotting part
		if file does not exists this will not crash only messafe is written if not silend"""
	
	#TODO rework this to load the mpl format
	if filename[-4:] != '.mpl':
		filename += '.mpl'

	try:
		f = open(filename, 'r')
		#NOTE create empty figure
		figure = util.setup_curr_figure(is_make_current=load_as_current, is_force=True)
		#NOTE read file and fill the figure
		curr_section = None
		for ind,readline in enumerate(f.readlines()):
			if len(readline) < 2:
				continue
			if readline[0] == '#' and readline[1] != '#': #NOTE comment line
				continue
			if readline[:2] == '##': #NOTE section divisor
				curr_section = readline[3:].strip()
				if curr_section.find('errline') > -1:
					#NOTE case of line
					#NOTE create blank line BEWARE args and its x,y are required, kwrags is required to be present
					new_errline = ErrLine()
					#NOTE add new line to figure
					figure.err_lines.append(new_errline)
				elif curr_section.find('line') > -1:
					#NOTE case of line
					#NOTE create blank line BEWARE args and its x,y are required, kwrags is required to be present
					new_line = Line()
					#NOTE add new line to figure
					figure.lines.append(new_line)
				continue

			if curr_section is not None:
				key,key_type,val = re.findall(r'([\w\s]*):([\w\s]*)=(.*)',readline)[0]
				if curr_section.find('errline') > -1:
					#NOTE case of line adding
					figure.err_lines[-1].line_keys[key] = util.convert_to_type(key_type.rstrip(),val.lstrip())
				elif curr_section.find('line') > -1:
					#NOTE case of line adding
					figure.lines[-1].line_keys[key] = util.convert_to_type(key_type.rstrip(),val.lstrip())
				elif curr_section == 'figure':
					#NOTE figure is special not in sections
					if alternative_figname is not None and key == 'num':
						#NOTE if alternative name is supplied then num is overwriten
						figure.figure_keys[key] = util.convert_to_type('str',alternative_figname)
					else:
						figure.figure_keys[key] = util.convert_to_type(key_type.rstrip(),val.lstrip())
				else:
					#NOTE regular section
					figure.sections[curr_section][key] = util.convert_to_type(key_type.rstrip(),val.lstrip())
			else:
				raise RuntimeError(f'Error processing file {filename} on line {ind}')

		if plot_self is True:
			figure.plot_self()
		return figure

	except FileNotFoundError:
		#NOTE case the loading of nonexistent file - perform nothing
		if is_silent is False:
			print(f"WARNING: file {filename} not found -> nothing is loaded.")
		return None
		
def load_and_show(files):
	""" load selected files [str/list] and show their plots"""

	if type(files) is str:
		files_to_load = (files,)
	else:
		files_to_load = files

	load_names = {}
	for file in files:		
		try:
			#NOTE resolve multiple figures have same fig name
			load_name = get_fig_name(file)
			if load_name not in load_names.keys():
				load_names[load_name] = 1
				load(file)
			else:
				#NOTE todo change the name to bypass this issue
				load_names[load_name] += 1 
				new_name = load_name + f'<{load_names[load_name]}>'
				print(f"WARNING: '{load_name}' exist ->rename it to {new_name} !")
				load(file,alternative_figname=new_name)

		except RuntimeError as e:
			print(f"Loading failed with:\n{e}")
	show()

if __name__ == '__main__':
	argv = sys.argv
	argc = len(argv)
	if argc == 1:
		print("Not enough arguments supplied for loading *.mpl file")
		exit(-1)

	load_and_show(argv[1:])
