############################
##       Calvin Yong      ##
##    MTH 691 Program 5   ##
############################

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import multiprocessing as mp
from itertools import repeat
import pathlib
from time import time
import projfuncs as pf
import projLists
import os

def yeda3(fileloc, filetype):
    init_tm = time()

    # Make dir
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    dirpath = "program3_mpl_out/" + filetype + "/" + date + "/"
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

    # Get List of tickers
    pf.get_tickerList(date, filetype)

    for ticker in projLists.ticker_list:
        data_starttm = time()
        data = pf.get_tickerData(fileloc, filetype, ticker, "Q")
        print("Got", ticker, "data data in", time() - data_starttm, "Seconds")

        #################
        # Plotting time #
        #################

        if(data.empty):
            message = "At date " + date + ", ticker" + ticker + " had no trade data\n"
            print(message)
            with open("program3_mpl_" + filetype + "_log.txt", 'a+') as f:
                f.write(message)
            continue

        fig, ax = plt.subplots(figsize=(20,8))
        ax.plot(data.Time, data['Ask Price'],color = "blue", linewidth = 1.0, 
                linestyle = '-', label = 'Ask Price')
        ax.plot(data.Time, data['Bid Price'],color = "red", linewidth = 1.0, 
                linestyle = '-', label = 'Bid Price')
        ax.set_xlabel('Time (UTC)')
        ax.set_ylabel('Price')
        title_date = data.Time[len(data) - 1].strftime('%b %-d, %Y')
        ax.set_title(ticker + " | " + "quotes | " + title_date)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        #setting major locator
        alldays =  mdates.HourLocator(interval = 1) # 3H interval
        ax.xaxis.set_major_locator(alldays)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I %p'))

        #setting minor locator
        hoursLoc = mdates.HourLocator(interval=30)
        ax.xaxis.set_minor_locator(hoursLoc)
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%M'))
        ax.legend()
        imgname = ticker + "_" + "quotes_" + filetype + "_" + date + ".png"
        fig.savefig(dirpath + imgname)
        plt.close()
        
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
        pool.starmap(yeda3, 
                     zip(projLists.file_list, repeat(filetype)))
    
    print("Program 3 mpl finished in", (time() - program_start_tm)/60, "minutes")
    print("Type", filetype, "files done :D")