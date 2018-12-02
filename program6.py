############################
##       Calvin Yong      ##
##    MTH 691 Program 6   ##
############################

from __future__ import print_function
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
from time import time
import projfuncs as pf

# NOT TESTED. SCRIPT MAY NOT WORK.
# Redundant since plotly can get 1 minute snapshots.

'''
Example input:

ticker = ['X:SBCHETH']
date = "20180401"
tm = "6:00 PM"
'''
###################
## Main Function ##
###################

if __name__ == "__main__":
    fileloc = "output/program1_out_A_20180404.txt"

    # Determine file type from file name
    fsplit = fileloc.split('_')
    if ("A" in fsplit):
        filetype = "A"
    else:
        filetype = "B"
    
    ticker = pf.get_validInput("Enter One Ticker: ", 1, ascii_art=True)
    ticker = ticker[0]

    # User should be careful. No error checking
    date = input("Enter Date: ")
    tm = input("Enter time")
    
    # Get unix timestamp from date and time
    unixtm = pf.time2unix(date, tm)

    # Get df from file
    with open(fileloc, 'r') as finput:
        pf.go_to_ticker(finput, ticker)
        print("Getting df from output...")
        init_tm = time()
        trades, quotes = pf.get_twoDFs(finput, filetype, unixtm=unixtm)
        print("Got data in", time() - init_tm, "seconds")
        
    # Plotting the data
    # Quote data plot
    if (quotes.empty):
        print("There are no quotes for this timeframe")
    else:
        trace1 = go.Scatter(x = quotes.Time, y = quotes["Bid Price"],
                            line = {'color': 'red'}, name = "Bid Price")
        trace2 = go.Scatter(x = quotes.Time, y = quotes["Ask Price"],
                            line = {'color': 'blue'}, name = "Ask Price")
        layout = go.Layout(xaxis = {'title': 'Time', 'type': 'date',
                                    'tickformat': '%I:%M:%S %p'},
                           yaxis = {'title': 'Price'},
                           title = ticker + " | " + quotes.Time[0].strftime('%b %-d, %Y'))
        fig = go.Figure(data = [trace1, trace2], layout = layout)
        py.plot(fig, filename='plots/plot6a.html', 
                auto_open=False, show_link=False,
                image="png", image_width=1600, image_height=900)
    
    # Trade data plot
    if (trades.empty):
        print("There are no trades for this timeframe")
    else:
        trace1 = go.Scatter(x = trades.Time, y = trades.Price,
                            name = "Price")
        layout = go.Layout(xaxis = {'title': 'Time', 'type': 'date',
                                    'tickformat': '%I:%M:%S %p'},
                           yaxis = {'title': 'Price'},
                           title = ticker + " | " + trades.Time[0].strftime('%b %-d, %Y'))
        fig = go.Figure(data = [trace1], layout = layout)
        py.plot(fig, filename='plots/plot6b.html',
                auto_open=False, show_link=False,
                image="png", image_width=1600, image_height=900)