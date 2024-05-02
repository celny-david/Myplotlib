# -*- coding: utf-8 -*-
"""
Line provides the encapsulation for simple line plot
"""

# Built-in/Generic Imports
from copy import deepcopy
# Libs
import matplotlib.pyplot as plt
# own
import utilities as util

class ErrLine:

	def __init__(self, show_label=True):
		""" initialize line and plot it using matplotlib"""
		# print(args) #DEBUG
		self.line_keys = {
					'xdata':None,\
					'ydata':None,\
					'xerr':None,\
					'yerr':None,\
					'fmt':'',\
					'is_used':True,\
					'color':None,\
					'ecolor':None,\
					'linestyle':None,\
					'linewidth':None,\
					'elinewidth':None,\
					'marker':None,\
					'markersize':None,\
					'capsize':None,\
					'barsabove':False,\
					'lolims':False,\
					'xlolims':False,\
					'uplims':False,\
					'xuplims':False,\
					'label':None,\
					'show_label':True,\
		}

		self.line_keys['show_label'] = show_label

	def to_mpl(self, count=None):
		""" provide own print to mpl"""
		str_out = f"## errline {count if count is not None else ''}\n"
		str_out += util.get_section_key_text(self.line_keys, preferential_keys=['is_used','xdata','ydata','xerr','yerr','fmt'])
		return str_out

	def plot_self(self):
		""" call the particular plt functions for the line"""

		#NOTE line section
		kwargs = deepcopy(self.line_keys)
		if kwargs.pop("is_used"):
			x = kwargs.pop('xdata')
			y = kwargs.pop('ydata')
			f = kwargs.pop('fmt')
			#NOTE hide label if show_label prevents it
			# print(kwargs["show_label"]) #DEBUG
			if kwargs.pop("show_label") is False:
				kwargs["label"] = None
			# plt.plot(x,y,f,**kwargs)
			# print("line: ", kwargs) #DEBUG
			plt.errorbar(x,y,**kwargs)