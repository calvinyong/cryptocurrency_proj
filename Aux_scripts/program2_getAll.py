############################
##       Calvin Yong      ##
##    MTH 691 Program 2   ##
############################

import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import multiprocessing as mp
from itertools import repeat
import pathlib
import os
from time import time
import projfuncs as pf
import projLists

def program2(fileloc, filetype):
    init_tm = time()

    # Make dir
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    dirpath = "program2_out/" + filetype + "/" + date + "/"
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

    # Get List of tickers
    pf.get_tickerList(date, filetype)

    for ticker in projLists.ticker_list:
        data_starttm = time()
        data = pf.get_tickerData(fileloc, filetype, ticker, "T")
        print("Got", ticker, "data DF in", time() - data_starttm, "Seconds")

        #################
        # Plotting time #
        #################

        if(data.empty):
            message = "At date " + date + ", ticker" + ticker + " had no trade data\n"
            print(message)
            with open("program2_" + filetype + "_log.txt", 'a+') as f:
                f.write(message)
            continue

        trace = go.Scatter(x = data.Time, y = data["Trade Price"])

        title_date = data.Time[len(data) - 1].strftime('%b %-d, %Y')
        layout = go.Layout(xaxis={'title': 'Time (UTC)', 'type': 'date',
                                'tickformat': '%I:%M:%S %p'},
                           yaxis={'title': 'Trade Price'},
                        title=ticker + " | " + "Trades | " + title_date)
        
        fig = go.Figure(data = [trace], layout = layout)

        # Output the plot
        imgname = ticker + "_" + "trades_" + filetype + "_" + date
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
        pool.starmap(program2, 
                     zip(projLists.file_list, repeat(filetype)))
    
    print("Program finished in", (time() - program_start_tm)/60, "minutes")
    print("Type", filetype, "files done :D")