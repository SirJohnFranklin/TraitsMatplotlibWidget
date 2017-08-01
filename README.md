# TraitsMatplotlibWidget
Matplotlib widget for Traits (http://code.enthought.com/projects/traits/)

This widget allows you to integrate matplotlib in your traits program in an efficent way. 
See the examples, how to use the plot, errorbar, imshow, blitting, plotting with multiple axes and integrating matplotlib patches.

## Features:
- fast plotting, imshow, errorbar automatic updating of data in traits GUI for python 2.7 & python 3.6
- copy data shown in plot to clipboard in linux & windows
- automatic masking of data before matplotlib freezes (can be turned off)
- set title, label etc.
- multiple axis support
- blitting support for plot & errorbar

Update 2017-08-01 (port to python 3.6 & python 2.7 support maintained):
- Added interpolation for line cut through image
- Data of line cuts are now stored and updated automatically in WidgetFigure.line_data
- Data of rectangle patches are now stored and updated automatically in WidgetFigure.patch_data
