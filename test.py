#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import MyPlotLib as mpl

# print(sys.argv) #DEBUG

argv = sys.argv
argc = len(argv)
if argc > 1:
	test_case = int(argv[1])
else:
	test_case = 0

if test_case in (-1,):
	#NOTE test case of loading all figure files in folder
	#NOTE remove the command call and test_case argument
	argv = argv[2:]
	argc = len(argv)
	if argc == 0: 
		print("Not enough arguments supplied for loading *.mpl file")
		exit(-1)
	mpl.load_and_show(argv)

if test_case in (0,1,2,):
	#NOTE test case of plotting multiple lines in figure and setting all properties
	mpl.figure('first figure')
	mpl.plot([1,2,3],[2,3,4],'-go')
	# print("\n",mpl.curr_figure.lines) #DEBUG
	mpl.plot([3,4,5],'-rx',label='red line')
	# print("\n",mpl.curr_figure.lines) #DEBUG
	mpl.xlim(-1,5)
	mpl.ylim(2,7)
	mpl.xlabel('this is X label')
	mpl.ylabel('this is Y label')
	mpl.legend()
	mpl.title('this is a title')
	mpl.save('test_mpl')
	# mpl.curr_figure.figure_keys['num'] = 'first figure'
	# print(mpl.curr_figure) #DEBUG

if test_case in (1,2,):
	#NOTE test case of loading new figure
	#NOTE change the first figure name to not conflict
	#     this is valid only for the testing
	mpl.get_curr_figure().figure_keys['num'] = 'second figure'
	mpl.save('test_mpl1')
	#NOTE load the figure as in normal scenario
	mpl.load('test_mpl1')
	# print(mpl.curr_figure)

if test_case in (2,3):
	if test_case in (3,):
		#NOTE test case of only loading
		#     enables changing the test_mpl.mpl file
		mpl.load('test_mpl')
	#NOTE add new data in previously loaded figure
	mpl.plot([2,3,4],'-ms',label='magenta line')
	mpl.xlim(-2,4)
	mpl.ylim(1,6)
	mpl.xlabel('this is SECOND X label')
	mpl.ylabel('this is SECOND Y label')
	mpl.legend()

	if test_case in (3,):
		#NOTE save the new figure
		mpl.save('test_mpl3')

if test_case in (4,):
	#NOTE test case of loading two different figures
	myfig1 = mpl.load('test_mpl')
	myfig2 = mpl.load('test_mpl3')

if test_case in (5,):
	#NOTE test appending into the figure
	filename = 'appended'
	mpl.clear(filename)
	for i in range(4):
		mpl.figure('test_append')
		mpl.load(filename, plot_self=False)

		mpl.plot([i*1,i*2,i*3], label=f"line {i}")
		mpl.xlim(0,3)
		mpl.ylim(-1,i*3)
		mpl.legend()
		mpl.save(filename)

mpl.show()

