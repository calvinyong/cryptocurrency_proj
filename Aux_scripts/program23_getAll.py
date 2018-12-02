############################
##       Calvin Yong      ##
##    Program 2 Get All   ##
############################

from __future__ import print_function
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
from time import time
from time import ctime
import pathlib
import projfuncs as pf
import projLists

if __name__ == "__main__":
    filetype = pf.get_validInput("Type A or B files: ", 4)
    
    print("Program started")
    program_start = time()

    log = open("program23_getAll_log.txt", "w+")

    for fileloc in projLists.file_list:
        # Make a directory for the date
        fsplit = fileloc.split('_')
        filedate = fsplit[len(fsplit) - 1][:-4]
        dirpath = 'plots/' + filetype + '/' + filedate + '/'
        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

        # Start timing file
        filetime_start = time()

        # Open the data file
        with open(fileloc, 'r') as finput:
            pf.get_tickerList(filedate, filetype)
            projLists.ticker_list.remove("ALL")

            # Get plots for each ticker
            for tick in projLists.ticker_list:
                ticker_start = time()
                print("----------------------------------------------")
                print("Program on date", filedate, "and ticker", tick)
                print("----------------------------------------------")
                print("Current time", ctime())

                pf.go_to_ticker(finput, tick, skip_header=True)
                print("Getting df from output...")
                init_tm = time()
                trades, quotes = pf.get_twoDFs(finput, filetype, one_min=False)
                print("Got data in", time() - init_tm, "seconds")

                #----------------------------
                # Plot the trade data
                #----------------------------

                if (trades.empty):
                    print("At date " + filedate + ", ticker" + tick + " had no trade data\n")
                    log.write("At date " + filedate + ", ticker" + tick + " had no trade data\n")
                else:
                    trace = go.Scatter(x = trades.Time, y = trades.Price)

                    layout = go.Layout(xaxis={'title': 'Time', 'type': 'date',
                                            'tickformat': '%I:%M:%S %p',
                                            'rangeslider': {}},
                                    yaxis={'title': 'Price'},
                                    title=tick + " | " + trades.Time[0].strftime('%b %-d, %Y'))
                    
                    fig = go.Figure(data = [trace], layout = layout)

                    # Output the plot
                    py.plot(fig, 
                    filename=dirpath + tick + "_trades_" + filedate + '.html', 
                    auto_open=False, show_link=False,
                    image="png", image_width=1600, image_height=900)

                #----------------------------
                # Plot the quote data
                #----------------------------

                if (quotes.empty):
                    print("At date " + filedate + ", ticker" + tick + " had no quote data\n")
                    log.write("At date " + filedate + ", ticker" + tick + " had no quote data\n")
                else:
                    trace1 = go.Scatter(x = quotes.Time, y = quotes["Bid Price"],
                                        line = {'color': 'red'}, name = "Bid Price")
                    trace2 = go.Scatter(x = quotes.Time, y = quotes["Ask Price"],
                                        line = {'color': 'blue'}, name = "Ask Price")
                    
                    layout = go.Layout(xaxis={'title': 'Time', 'type': 'date',
                                            'tickformat': '%I:%M:%S %p',
                                            'rangeslider': {}},
                                    yaxis={'title': 'Price'},
                                    title=tick + " | " + quotes.Time[0].strftime('%b %-d, %Y'))
                    
                    fig = go.Figure(data = [trace1, trace2], layout = layout)

                    # Output the plot
                    py.plot(fig, 
                            filename=dirpath + tick + "_quotes_" + filedate + '.html', 
                            auto_open=False, show_link=False,
                            image="png", image_width=1600, image_height=900)

                    print("Ticker", tick, "completed in", time() - ticker_start, "seconds")
                
                finput.seek(0)

            print("File", filedate, "completed in", (time() - filetime_start)/60, "minutes")

    print("Program finished in", (time() - program_start)/60, "minutes")
    log.close()