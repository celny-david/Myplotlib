# -*- coding: utf-8 -*-
"""
provide helper and utility functions, usefull get,set and convertors
"""
# Built-in/Generic Imports
import ast
from copy import deepcopy
#own
from fig_data import Fig_data, curr_figure


#=== utility functions ===
def get_section_key_text(section_dict,preferential_keys=[]):
	""" return the text formatted from directory supplied to it
		suport preferential print of selected keys"""
	str_out = ''
	for key in preferential_keys:
		val = section_dict[key]
		val_type = str(type(val))
		val_type = val_type[val_type.find("'")+1:val_type.rfind("'")]
		# print(val, str(type(val)), val_type) #DEBUG
		str_out += f"{key}:{val_type} = {val}\n"

	for key in section_dict.keys():
		if key in preferential_keys:
			continue
		val = section_dict[key]
		val_type = str(type(val))
		val_type = val_type[val_type.find("'")+1:val_type.rfind("'")]
		# print(val, str(type(val)), val_type) #DEBUG
		str_out += f"{key}:{val_type} = {val}\n"
	return str_out

def setup_curr_figure(is_make_current, is_force=False):
	""" initial setup of current figure global value to either current if available
		or make a new one the current one"""
	global curr_figure
	#NOTE TODO temporarry fix in situation when requested figure of existing name to retain the original fig_data of that figure as in plt case
	if curr_figure is None or is_force is True:
		figure = Fig_data()
		if is_make_current is True:
			curr_figure = figure
		# print(curr_figure) #DEBUG
	else:
		figure = curr_figure
	# print("setup_curr_figure: ",figure) #DEBUG
	return deepcopy(figure)

def get_curr_figure():
	""" return the current figure
		if curr_figure is None raise RuntimeError"""
	if curr_figure is None:
		raise RuntimeError(f"No mytplotlib figure created yet. Initialize figure first.")
	return curr_figure

def get_curr_figure_ifnone(figure=None):
	""" return the current figure if none is passed in
		if curr_figure is None raise RuntimeError"""
	global curr_figure
	# print("get_curr_figure_ifnone: ",curr_figure) #DEBUG
	if figure is None:
		figure = get_curr_figure()
	return figure

def set_val_to_figure_dict(target_dict, source_dict):
	""" set the values to target dict from source dict they exist """
	for key in target_dict.keys():
		if key in source_dict.keys():
			target_dict[key] = source_dict[key]

def set_val_from_plt_line(line2d, target_dict, keys_to_set):
	""" set keys to set values to target dict from line2d_object """
	
	for key in keys_to_set:
		# get_func = getattr("",f'get_{key}')
		# res = line2d.get_func()
		res = eval(f"line2d.get_{key}()")
		# print(res) #DEBUG
		if type(res) is str:
			target_dict[key] = res
		elif hasattr(res, '__iter__'):
			#NOTE should be iterable -> convert to list
			target_dict[key] = list(res)
		else:
			#NOTE process the rest normally
			target_dict[key] = res

def enable_figure_feature(target_dict):
	""" enable feature if possible to enable it"""
	if 'is_used' in target_dict.keys():
		target_dict['is_used'] = True

def convert_to_type(type_specifier,value):
	""" evaluate the string value into desired type_specification
		supports int,float,str,bool,list,tuple,NoneType """
	supported_types = {
		'int':int,\
		'float':float,\
		'str':lambda s: str(s).replace("\n",""),\
		'bool':lambda s: s.strip() in ('True','true'),\
		'list':lambda s: list(ast.literal_eval(s)),\
		'tuple':lambda s: tuple(ast.literal_eval(s)),\
		'dict':lambda s: dict(ast.literal_eval(s)),\
		'NoneType':lambda s: None,\
	}
	if type_specifier not in supported_types.keys():
		raise ValueError(f"Invalid unsupported type encountered:{type_specifier}")
	else:
		#NOTE default conversion
		#BEWARE str case remove all newline characters
		#BEWARE type correction for list case to result in list
		#BEWARE type correction for tuple case to result in tuple
		#BEWARE NoneType only returns None without conversion
		res = supported_types[type_specifier](value)		
		return res
