# -*- coding: utf-8 -*-
"""
Provide wrappers of matplotlib functions to facilitate transfer and saving of the fig_data
"""

# Futures
# from __future__ import print_function

# Built-in/Generic Imports
from sigtools import specifiers
# Libs
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.axes_divider as mplt
# own
from line import Line
from errline import ErrLine
import utilities as util
from fig_data import Fig_data, curr_axes, curr_figure

#=== matplotlib functions vrappers ===

@specifiers.forwards_to_function(plt.figure)
def figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=True, clear=False, make_current=True, **kwargs):
	""" """
	# print(type(kwargs)) #DEBUG
	# print(kwargs) #DEBUG
	fig = plt.figure(num=num, figsize=figsize, dpi=dpi,\
			  facecolor=facecolor, edgecolor=edgecolor, frameon=frameon,\
			  clear=clear, **kwargs)

	figure = util.setup_curr_figure(make_current)
	# print("figure wrapper: ",figure)#DEBUG

	#NOTE save the important atributes
	util.set_val_to_figure_dict(figure.figure_keys, kwargs)
	util.set_val_to_figure_dict(figure.figure_keys, {'num':num, 'figsize':figsize, 'dpi':dpi, 'facecolor':facecolor, 'edgecolor':edgecolor, 'frameon':frameon, 'clear':clear,})
	
	return fig 

@specifiers.forwards_to_function(plt.gca)
def gca():
	""" """
	global curr_axes
	ax = plt.gca()

	if curr_axes is None:
		axis = ax
	else:
		axis = curr_axes

	return ax

@specifiers.forwards_to_function(mplt.make_axes_locatable)
def make_axes_locatable(axes):
	""" """
	divider = make_axes_locatable(axes)
	
	return divider

@specifiers.forwards_to_function(plt.plot)
def plot(*args, scalex=True, scaley=True, data=None, show_label=True, fig_data=None, **kwargs):
	""" """
	# print(args) #DEBUG
	figure = util.get_curr_figure_ifnone(fig_data)
	#NOTE handle the not show lable
	if show_label is False:
		# print('removing label') #DEBUG
		try:
			kwargs.pop('label')
		except:
			pass

	plt_line = plt.plot(*args, scalex=scalex, scaley=scaley, data=data, **kwargs)
	if type(plt_line) is list:
		plt_line = plt_line[0]

	kyes_of_intererst = ('xdata','ydata',\
						 'color','linestyle','linewidth',\
						 'marker','markersize')
	new_line = Line()	
	util.set_val_to_figure_dict(new_line.line_keys, kwargs)
	util.set_val_to_figure_dict(new_line.line_keys, {'scalex':scalex,'scaley':scaley,'data':data})
	util.set_val_from_plt_line(plt_line, new_line.line_keys, keys_to_set=kyes_of_intererst)
	figure.lines.append(new_line)

@specifiers.forwards_to_function(plt.errorbar)
def errorbar(x, y, yerr=None, xerr=None, fmt='', ecolor=None, elinewidth=None, capsize=None, barsabove=False, lolims=False, uplims=False, xlolims=False, xuplims=False, errorevery=1, capthick=None, data=None, show_label=True, fig_data=None, **kwargs):
	""" """
	# print(args) #DEBUG
	figure = util.get_curr_figure_ifnone(fig_data)
	#NOTE handle the not show lable
	if show_label is False:
		# print('removing label') #DEBUG
		try:
			kwargs.pop('label')
		except:
			pass

	plt_errline = plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt=fmt,\
							ecolor=ecolor, elinewidth=elinewidth, capsize=capsize, barsabove=barsabove,\
							lolims=lolims, uplims=uplims, xlolims=xlolims, xuplims=xuplims, errorevery=errorevery,\
							capthick=capthick, data=data, **kwargs)
	if type(plt_errline) is list:
		plt_errline = plt_errline[0]

	line2d_kyes_of_intererst = ('xdata','ydata',\
						 'color','linestyle','linewidth',\
						 'marker','markersize')
	new_errline = ErrLine()	
	util.set_val_to_figure_dict(new_errline.line_keys, kwargs)
	util.set_val_to_figure_dict(new_errline.line_keys, {'data':data, 'xerr':xerr, 'yerr':yerr, 'ecolor':ecolor, 'elinewidth':elinewidth, 'capsize':capsize, 'barsabove':barsabove} )
	line2d = plt_errline.get_children()[0]
	util.set_val_from_plt_line(line2d, new_errline.line_keys, keys_to_set=line2d_kyes_of_intererst)
	figure.err_lines.append(new_errline)

	
@specifiers.forwards_to_function(plt.xlim)
def xlim(*args, fig_data=None, **kwargs):
	""" """
	plt.xlim(*args, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	left,right = plt.xlim()
	util.set_val_to_figure_dict(figure.xlim_keys, kwargs)
	util.set_val_to_figure_dict(figure.xlim_keys, {'left':float(left),'right':float(right)})
	util.enable_figure_feature(figure.xlim_keys)

@specifiers.forwards_to_function(plt.ylim)
def ylim(*args, fig_data=None, **kwargs):
	""" """
	plt.ylim(*args, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	bottom,top = plt.ylim()
	util.set_val_to_figure_dict(figure.ylim_keys, kwargs)
	util.set_val_to_figure_dict(figure.ylim_keys, {'top':float(top),'bottom':float(bottom)})
	util.enable_figure_feature(figure.ylim_keys)

@specifiers.forwards_to_function(plt.xticks)
def xticks(ticks=None, labels=None, minor=False, fig_data=None, **kwargs):
	""" """
	plt.xticks(ticks=ticks, labels=labels, minor=minor, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	# ticks,labels = plt.xticks() #BUG not working - return Text structure and np.ndarray which it does not accept
	util.set_val_to_figure_dict(figure.xticks_keys, kwargs)
	util.set_val_to_figure_dict(figure.xticks_keys, {'ticks':ticks,'labels':labels, 'minor':bool(minor)})
	util.enable_figure_feature(figure.xticks_keys)

@specifiers.forwards_to_function(plt.yticks)
def yticks(ticks=None, labels=None, minor=False, fig_data=None, **kwargs):
	""" """
	plt.yticks(ticks=ticks, labels=labels, minor=minor, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	# ticks,labels = plt.yticks() #BUG not working - return Text structure and np.ndarray which it does not accept
	util.set_val_to_figure_dict(figure.yticks_keys, kwargs)
	util.set_val_to_figure_dict(figure.yticks_keys, {'ticks':ticks,'labels':labels, 'minor':bool(minor)})
	util.enable_figure_feature(figure.yticks_keys)

@specifiers.forwards_to_function(plt.xlabel)
def xlabel(xlabel, fontdict=None, labelpad=None, loc=None, fig_data=None, **kwargs):
	""" """
	xlabel = fr"{xlabel}"
	plt.xlabel(xlabel, fontdict=fontdict, labelpad=labelpad, loc=loc, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	util.set_val_to_figure_dict(figure.xlabel_keys, kwargs)
	util.set_val_to_figure_dict(figure.xlabel_keys, {'xlabel':xlabel, 'fontdict':fontdict, 'labelpad':labelpad, 'loc':loc, })
	util.enable_figure_feature(figure.xlabel_keys)

@specifiers.forwards_to_function(plt.ylabel)
def ylabel(ylabel, fontdict=None, labelpad=None, loc=None, fig_data=None, **kwargs):
	""" """
	ylabel = fr"{ylabel}"
	plt.ylabel(ylabel, fontdict=fontdict, labelpad=labelpad, loc=loc, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	util.set_val_to_figure_dict(figure.ylabel_keys, kwargs)
	util.set_val_to_figure_dict(figure.ylabel_keys, {'ylabel':ylabel, 'fontdict':fontdict, 'labelpad':labelpad, 'loc':loc, })
	util.enable_figure_feature(figure.ylabel_keys)

@specifiers.forwards_to_function(plt.legend)
def legend(*args, fig_data=None, **kwargs):
	""" """
	plt.legend(*args, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	util.set_val_to_figure_dict(figure.legend_keys, kwargs)
	util.enable_figure_feature(figure.legend_keys)

@specifiers.forwards_to_function(plt.suptitle)
def title(label, fontdict=None, loc=None, pad=None, y=None, fig_data=None, **kwargs):
	""" """
	label = fr"{label}"
	plt.title(label, fontdict=fontdict, loc=loc, pad=pad, y=y, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	util.set_val_to_figure_dict(figure.title_keys, kwargs)
	util.set_val_to_figure_dict(figure.title_keys, {'label':label, 'fontdict':fontdict, 'loc':loc, 'pad':pad, 'y':y })
	util.enable_figure_feature(figure.title_keys)


@specifiers.forwards_to_function(plt.suptitle)
def suptitle(t, fig_data=None, **kwargs):
	""" """
	t = fr"{t}"
	plt.suptitle(t, **kwargs)
	#NOTE own processing
	figure = util.get_curr_figure_ifnone(fig_data)
	util.set_val_to_figure_dict(figure.suptitle_keys, kwargs)
	util.set_val_to_figure_dict(figure.suptitle_keys, {'label':t})
	util.enable_figure_feature(figure.suptitle_keys)

def tight_layout(fig_data=None):
	""" provide tight layout for externally placed legends"""
	plt.tight_layout()
	
	figure = util.get_curr_figure_ifnone(fig_data)
	util.set_val_to_figure_dict(figure.other_keys, {'is_tight_layout':True})
	util.enable_figure_feature(figure.other_keys)

def show():
	""" show the figures"""
	plt.show()
