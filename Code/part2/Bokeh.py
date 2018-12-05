# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 18:50:30 2018

@author: lifen
"""

import pandas as pd
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.palettes import Set2
from bokeh.palettes import GnBu3, OrRd3
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.glyphs import Line
import math

#%%
output_file("bar_stacked.html")

df0 = pd.read_csv('CrimeCatbyOffender_Age.csv')

#df0.sum(axis = 1) # check values, group categories less than 500 and 'other crimes'
df0.iloc[4] = df0.iloc[4:10].sum()
df0 = df0.set_value(4, 'Category', 'Other Category')
df0 = pd.concat([df0[0:5], df0[10:]], ignore_index = True)

#df0.sum(axis = 0) # check values, group ages less than 1000

df0['Total'] = df0.sum(axis = 1)
df0 = df0.sort_values(['Total'], ascending = False)
del df0['Total']

cat = df0.iloc[:,0]
age = df0.columns[1:].tolist()
colors = Set2[4]

data = {'Category' : cat,
        '18-29'   : df0.iloc[:,1],
        '30-44' : df0.iloc[:,2],
        '45-60' : df0.iloc[:,3],
        "61+" : df0.iloc[:,4]}

p = figure(x_range=cat, plot_height=800, plot_width=700, title="Case Counts by Crime Citation Category, 2017",
           toolbar_location=None, tools="hover", tooltips="$name @Category: @$name")

p.vbar_stack(age, x='Category', width=0.9, color=colors, source=data,
             legend=[value(x) for x in age])

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.title.text_font_size = '20pt'
p.xaxis.major_label_orientation = math.pi/4
p.xaxis.major_label_text_font_size = '12pt'
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "horizontal"
p.legend.click_policy="hide"

show(p)

#%%
output_file("bar_stacked_1.html")

df1 = pd.read_csv('CrimeCatbyOffender_Race_male.csv')
df2 = pd.read_csv('CrimeCatbyOffender_Race_female.csv')

#group categories according to previous grouping
df1.iloc[4] = df1.iloc[4:10].sum()
df1 = df1.set_value(4, 'Category', 'Other Category')
df1 = pd.concat([df1[0:5], df1[10:]], ignore_index = True)

#group categories according to previous grouping
df2.iloc[4] = df2.iloc[4:10].sum()
df2 = df2.set_value(4, 'Category', 'Other Category')
df2 = pd.concat([df2[0:5], df2[10:]], ignore_index = True)

#df1.sum(axis = 0) # check values, group races less than 1000
df1['Other Race'] = df1['Asian'] + df1['Other'] 
del df1['Asian'], df1['Other']

#group categories according to previous grouping
df2['Other Race'] = df2['Asian'] + df2['Other'] 
del df2['Asian'], df2['Other']

df1['Total'] = df1.sum(axis = 1)
df1 = df1.sort_values(['Total'], ascending = False)
del df1['Total']

df2['Total'] = df2.sum(axis = 1)
df2 = df2.sort_values(['Total'], ascending = False)
del df2['Total']

race = df1.columns[1:].tolist()
race[2] = 'Other'

data1 = {'Category': cat,
        'Black': df1.iloc[:,1],
        'White': df1.iloc[:,2],
        'Other': df1.iloc[:,3]}

data2 = {'Category': cat,
        'Black': df2.iloc[:,1] * -1,
        'White': df2.iloc[:,2] * -1,
        'Other': df2.iloc[:,3] * -1}

p1 = figure(y_range=cat, plot_height=600, plot_width =1200, x_range=(-2500, 2800), title="Case Counts by Crime Citation Category, 2016",
           toolbar_location=None, tools="hover", tooltips="$name @Category: @$name")

p1.hbar_stack(race, y='Category', height=0.9, color=GnBu3, source=ColumnDataSource(data1),
             legend=['%s Male' % x for x in race])
p1.hbar_stack(race, y='Category', height=0.9, color=OrRd3, source=ColumnDataSource(data2),
             legend=['%s Female' % x for x in race])

p1.y_range.range_padding = 0.1
p1.ygrid.grid_line_color = None
p1.title.text_font_size = '20pt'
p1.axis.minor_tick_line_color = None
p1.yaxis.major_label_text_font_size = '12pt'
p1.outline_line_color = None
p1.legend.location = "top_right"
p1.legend.orientation = "vertical"
p1.legend.click_policy="hide"

show(p1)

#%%
output_file("line.html")

df3 = pd.read_csv('CriminalCitationsCount.csv')

year = df3['Year']
count = df3['Citations']
data3 = {'Year':year, 
         'Count': count}
plot = figure(title="Total Criminal Citations Issued in Maryland 2007-2017", plot_width=800, plot_height=600, #,
    h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None,
    tooltips="@Year: @Count")
glyph = Line(x="Year", y="Count", line_color="orange",line_width=6, line_alpha=0.6)
source=ColumnDataSource(data3)
plot.add_glyph(source, glyph)
plot.title.text_font_size = '20pt'
plot.yaxis.major_label_text_font_size = '12pt'
plot.xaxis.major_label_text_font_size = '12pt'
plot.y_range.start = 0
plot.xaxis.minor_tick_line_color = None

show(plot)
