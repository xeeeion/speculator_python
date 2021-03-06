# --------FOR START THAT CODE PRINT "bokeh serve --show wwdata.py" IN TERMINAL-----------
# Also to start code u need print stock name in str 95 "symbol = ''  "

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Dropdown
from bokeh.io import curdoc
from bokeh.layouts import column

from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter

import pyautogui


W_Sreen, H_Screen = pyautogui.size()

# Define constants
W_PLOT = W_Sreen // 2
H_PLOT = H_Screen // 3
TOOLS = 'pan,wheel_zoom,hover,reset'

VBAR_WIDTH = 0.2
RED = Category20[7][6]
GREEN = Category20[5][4]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]


def get_symbol_df (symbol=None):
    df = pd.DataFrame (pd.read_csv ( symbol + '.csv'))[-50:]
    df.reset_index (inplace=True)
    df["Date"] = pd.to_datetime (df["Date"])
    return df


def plot_stock_price (stock):
    p = figure (plot_width=W_PLOT, plot_height=H_PLOT, tools=TOOLS,
                title="Stock price", toolbar_location='above')

    inc = stock.data['Close'] > stock.data['Open']
    dec = stock.data['Open'] > stock.data['Close']
    view_inc = CDSView (source=stock, filters=[BooleanFilter (inc)])
    view_dec = CDSView (source=stock, filters=[BooleanFilter (dec)])

    # map dataframe indices to date strings and use as label overrides
    p.xaxis.major_label_overrides = {
        i + int (stock.data['index'][0]): date.strftime ('%b %d') for i, date in
        enumerate (pd.to_datetime (stock.data["Date"]))
    }
    p.xaxis.bounds = (stock.data['index'][0], stock.data['index'][-1])

    p.segment (x0='index', x1='index', y0='Low', y1='High', color=RED, source=stock, view=view_inc)
    p.segment (x0='index', x1='index', y0='Low', y1='High', color=GREEN, source=stock, view=view_dec)

    p.vbar (x='index', width=VBAR_WIDTH, top='Open', bottom='Close', fill_color=BLUE, line_color=BLUE,
            source=stock, view=view_inc, name="price")
    p.vbar (x='index', width=VBAR_WIDTH, top='Open', bottom='Close', fill_color=RED, line_color=RED,
            source=stock, view=view_dec, name="price")

    p.legend.location = "top_left"
    p.legend.border_line_alpha = 0
    p.legend.background_fill_alpha = 0
    p.legend.click_policy = "mute"

    p.yaxis.formatter = NumeralTickFormatter (format='$ 0,0[.]000')
    p.x_range.range_padding = 0.05
    p.xaxis.ticker.desired_num_ticks = 40
    p.xaxis.major_label_orientation = 3.14 / 4

    # Select specific tool for the plot
    price_hover = p.select (dict (type=HoverTool))

    # Choose, which glyphs are active by glyph name
    price_hover.names = ["price"]
    # Creating tooltips
    price_hover.tooltips = [("Datetime", "@Date{%Y-%m-%d}"),
                            ("Open", "@Open{$0,0.00}"),
                            ("Close", "@Close{$0,0.00}"),
                            ("Volume", "@Volume{($ 0.00 a)}")]
    price_hover.formatters = { "Date": 'datetime' }

    return p


stock = ColumnDataSource (
    data=dict (Date=[], Open=[], Close=[], High=[], Low=[], index=[]))
symbol = 'aflt'     #<-------stock name here
df = get_symbol_df (symbol)
stock.data = stock.from_df (df)
elements = list ()

# update_plot()
p_stock = plot_stock_price (stock)

elements.append (p_stock)

curdoc ().add_root (column (elements))
curdoc ().title = 'Bokeh stocks historical prices'