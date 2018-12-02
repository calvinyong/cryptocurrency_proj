############################
##       Calvin Yong      ##
##    MTH 691 Program 3   ##
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

def program3(fileloc, filetype):
    init_tm = time()

    # Make dir
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    dirpath = "program3_out/" + filetype + "/" + date + "/"
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
            message = "At date " + date + ", ticker" + ticker + " had no quote data\n"
            print(message)
            with open("program3_" + filetype + "_log.txt", 'a+') as f:
                f.write(message)
            continue

        trace1 = go.Scatter(x = data.Time, y = data["Bid Price"],
                            line = {'color': 'red'}, name = "Bid Price")
        trace2 = go.Scatter(x = data.Time, y = data["Ask Price"],
                            line = {'color': 'blue'}, name = "Ask Price")
        
        title_date = data.Time[len(data) - 1].strftime('%b %-d, %Y')
        layout = go.Layout(xaxis={'title': 'Time (UTC)', 'type': 'date',
                                'tickformat': '%I:%M:%S %p'},
                           yaxis={'title': 'Price'},
                        title=ticker + " | Quotes | " + title_date)
        
        fig = go.Figure(data = [trace1, trace2], layout = layout)

        # Output the plot
        imgname = ticker + "_" + "quotes_" + filetype + "_" + date
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

    os.chdir("/space/mth693/common/phase1_alloutput/")

    program_start_tm = time()
    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(program3, 
                     zip(projLists.file_list, repeat(filetype)))
    
    print("Program 3 finished in", (time() - program_start_tm)/60, "minutes")
    print("Type", filetype, "files done :D")