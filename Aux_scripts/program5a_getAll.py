############################
##       Calvin Yong      ##
##    MTH 691 Program 5   ##
############################

import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import multiprocessing as mp
from itertools import repeat
import pathlib
from time import time
import projfuncs as pf
import projLists
import os

def program5a(fileloc, filetype, quotetype):
    init_tm = time()

    # Make dir
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    dirpath = "program5a_out/" + filetype + "/" + date + "/" + quotetype +"/"
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

    # Get List of tickers
    pf.get_tickerList(date, filetype)

    for ticker in projLists.ticker_list:
        data_starttm = time()
        data = pf.get_tickerData(fileloc, filetype, ticker, "Q")
        print("Got", ticker, "data DF in", time() - data_starttm, "Seconds")

        #################
        # Plotting time #
        #################

        if(data.empty):
            message = "There is no " + quotetype + " data for " + ticker + " at " + date + "\n"
            print(message)
            with open("program5a_" + filetype + "_log.txt", 'a+') as f:
                f.write(message)
            continue

        title_date = data.Time[len(data) - 1].strftime('%b %-d, %Y')
        layout = go.Layout(xaxis={'title': 'Time (UTC)', 'type': 'date',
                                'tickformat': '%I:%M:%S %p'},
                           yaxis={'title': 'Price'},
                           title=ticker + " | " + quotetype + " | " + title_date,
                           showlegend=True)
        
        # Make a trace for each venue
        traces = []
        for venue in data["Contributor Id"].unique():
            trace = go.Scatter(x = data.Time[data["Contributor Id"] == venue], 
                               y = data[quotetype + " Price"][data["Contributor Id"] == venue],
                               name = venue)
            traces.append(trace)
        
        # Output html file
        fig = go.Figure(data = traces, layout = layout)
        imgname = ticker + "_" + "quotes_" + quotetype + "_" + filetype \
                + "_" + date
        py.plot(fig, 
                filename=dirpath + imgname + ".html", 
                image="png",
                image_filename=imgname,
                image_width=1024,
                image_height=768,
                auto_open=False, 
                show_link=False)

        print("Ticker", ticker, "at date", date, "done")

    print(date, "plots finished in", time() - init_tm, "seconds")


###################
## Main Function ##
###################

if __name__ == "__main__":
    filetype = pf.get_validInput("Type A or B files: ", 4)
    while True:
        quotetype = input("Enter Bid or Ask: ")
        if (quotetype in ["Bid", "Ask"]):
            break
        print("Invalid Input")

    os.chdir("/space/mth693/common/phase1_alloutput/")

    program_start_tm = time()
    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(program5a, 
                     zip(projLists.file_list, repeat(filetype), repeat(quotetype)))
    
    print("Program finished in", (time() - program_start_tm)/60, "minutes")
    print("Type", filetype, "quotetype", quotetype, "files done :D")
 