############################
##       Calvin Yong      ##
##    MTH 691 Program 5   ##
############################

from __future__ import print_function
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import pathlib
from time import time
import projfuncs as pf
import sys

def program5b(fileloc, filetype, ticker):
    init_tm = time()

    # Make dir
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    dirpath = "output/program5b_out/" + filetype + "/" + date + "/"
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

    print("Getting data...")
    data = pf.get_tickerData(fileloc, filetype, ticker, "T")
    print("Got data. Generating plot...")

    #################
    # Plotting time #
    #################

    if(data.empty):
        print("At date " + date + ", ticker" + ticker + " had no trade data\n")
        return

    # Make a trace for each venue
    traces = []
    for venue in data["Contributor Id"].unique():
        trace = go.Scatter(x = data.Time[data["Contributor Id"] == venue], 
                           y = data["Trade Price"][data["Contributor Id"] == venue],
                           name = venue)
        traces.append(trace)

    title_date = data.Time[len(data) - 1].strftime('%b %-d, %Y')
    layout = go.Layout(xaxis={'title': 'Time (UTC)', 'type': 'date',
                                'tickformat': '%I:%M:%S %p'},
                       yaxis={'title': 'Trade Price'},
                    title=ticker + " | " + "Trades | " + title_date)
    
    fig = go.Figure(data = traces, layout = layout)

    # Output the plot
    imgname = ticker + "_" + "tradesV2_" + filetype + "_" + date
    py.plot(fig, 
            filename=dirpath + imgname + ".html", 
            image="png",
            image_filename=imgname,
            image_width=1024,
            image_height=768,
            auto_open=False, 
            show_link=False)
    
    print("Ticker", ticker, "at date", date, "finished in", 
          time() - init_tm, "seconds")

###################
## Main Function ##
###################

if __name__ == "__main__":
    try:
        filetype = sys.argv[1]
        date = sys.argv[2]
        ticker = sys.argv[3]
    except IndexError:
        print("Program 5b: Plot Trade Prices by Venue")
        print("Type 'list' to get a list of valid inputs")

        filetype = pf.get_validInput("Type A or B files: ", 4)
        date = pf.get_validInput("Enter Date in yyyymmdd: ", 0,
                                 filetype=filetype)
        ticker = pf.get_validInput("Enter One Ticker: ", 1)
        ticker = ticker[0]

    if (filetype == "A"):
        fileloc = "/space/crypto/PLUSTICK_1619_" + date + ".txt"
    else:
        fileloc = "/space/crypto/PLUSTICK_FI_1356_" + date + ".txt"

    program5b(fileloc, filetype, ticker)