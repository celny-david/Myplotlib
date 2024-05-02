# Info
My Plot Lib conceptualizes the plot into structure that can be saved to JSON file. Finally you are able to save and load your figures from the project without the need for costly recalculation. The module wraps around the original matplotlib functionality allowing for simple switch from `matplotlib` to `Myplotlib` simply within `import` statement.

This allows to backup the plotting enable ex-post re-visualization of ploted data. This module resolves the issue of adjusting plot later in the project when the original implementation is no longer supporting creating the plots from the past.

This is intended as personal hobby project for purposes of supporting my research. If you want to extend its capabilities or find some issues with it, you can contact me [here](mailto:celny.david@gmail.com).

# Capabilities
 - save matplotlib figure into JSON file format with extension `.mpl` while preserving the original matplotlib commands
 - supports use of follwoing functions:
 	- wrapped matplotlib functionality
 		- `def figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=True, clear=False, make_current=True, **kwargs):`
 		- `def gca():`
 		- `def make_axes_locatable(axes):`
 		- `def plot(*args, scalex=True, scaley=True, data=None, show_label=True, fig_data=None, **kwargs):`
 		- `def errorbar(x, y, yerr=None, xerr=None, fmt='', ecolor=None, elinewidth=None, capsize=None, barsabove=False,  		- lolims=False, uplims=False, xlolims=False, xuplims=False, errorevery=1, capthick=None, data=None,  		- show_label=True, fig_data=None, **kwargs):`
 		- `def xlim(*args, fig_data=None, **kwargs):`
 		- `def ylim(*args, fig_data=None, **kwargs):`
 		- `def xticks(ticks=None, labels=None, minor=False, fig_data=None, **kwargs):`
 		- `def yticks(ticks=None, labels=None, minor=False, fig_data=None, **kwargs):`
 		- `def xlabel(xlabel, fontdict=None, labelpad=None, loc=None, fig_data=None, **kwargs):`
 		- `def ylabel(ylabel, fontdict=None, labelpad=None, loc=None, fig_data=None, **kwargs):`
 		- `def legend(*args, fig_data=None, **kwargs):`
 		- `def title(label, fontdict=None, loc=None, pad=None, y=None, fig_data=None, **kwargs):`
 		- `def suptitle(t, fig_data=None, **kwargs):`
 		- `def tight_layout(fig_data=None):`
 		- `def show():`
	- added features:
		- `def save(filename, figure=None):`
			- save the current figure data into `<filename>.mpl`, if figure is given then it is saved instead
		- `def clear(filename):`
			- remove the existing file `<filename>.mpl`
		- `def get_fig_name(filename):`
			- verify if the name exist and then return it if it does
		- `def load(filename, alternative_figname = None, load_as_current=True, plot_self=True, is_silent=False):`
			- loading of the `*.mpl` file. Does not display
		- `def load_and_show(files):`
			- performs the loading and display the result using `show()`
 - to test the basic functionality run the test.py program
 	- you can run it with `./test.py <test_option>`
 		- `-1` load and show all `*.mpl` files in the folder with `test.py`
 		- `0` create figure plot two lines in it, save it as `test_mpl.mpl` and show
 		- `1` change the name from the `0` test to second_figure and save it as `test_mpl1.mpl`
 		- `2` plot another line with additional information into case `1` and show
 		- `3` simply load figure from case `0`  and add aditional line and info same as `2` and save it as `test_mpl3.mpl`
 		- `4` load two different figures simultaneously and show the second one
 		- `5` continuously append new lines to same figure in for loop and save it at the end as `test_mpl5.mpl`

# Concluding remarks
 This project was used throughout the work on dissertation and was originally designed with matplotlib 3.3 in mind.
  Be aware that this project is sensitive to changes in matplotlib interface and issues oof backwards compatibility may apper in the future.