# encoding: utf-8

r"""Plotting constants"""

import matplotlib.pyplot as plt


# Color and linestyles
rgb_converter = lambda triple: [float(rgb) / 255.0 for rgb in triple]
top_color = rgb_converter((67,183,219))
bottom_color = rgb_converter((37,56,159))
bathy_linestyle = '-'
internal_linestyle = '--'
surface_linestyle = '-'


def add_legend(axes,label,location=0,color='r',linestyle='-'):
    r""""""
    
    # Create new line for legend
    line = plt.Line2D((0,0),(0,1),color=color,linestyle=linestyle)
    
    # Append extra legend entry to list of handles and labels
    handles,labels = axes.get_legend_handles_labels()
    handles.append(line)
    labels.append(label)
    
    # Add legend to axes
    axes.legend(handles,labels,loc=location)
