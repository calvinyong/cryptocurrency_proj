import pandas as pd
import multiprocessing as mp
from itertools import repeat
from time import time
import projfuncs as pf
import projLists

def get_ohlc(fileloc, filetype, ticker):
    """
    Get open-high-low-close of ticker for one day

    Args:

    Returns:
    """
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    formatted_date = '-'.join([date[:4], date[4:6], date[6:]])

    print("Getting", ticker, "data from date", date)
    with open(fileloc, 'r') as finput:
        df = pf.get_tickerData(finput, filetype, ticker, "T")
    
    o = df["Trade Price"][0]
    h = df["Trade Price"].max()
    l = df["Trade Price"].min()
    c = df["Trade Price"][df.shape[0] - 1]

    print("Got ohlc at date", date)

    return [formatted_date, o, h, l, c]
    
###################
## Main Function ##
###################

if __name__ == "__main__":
    ticker = "X:SXBTUSD"
    filetype = pf.get_validInput("Type A or B files: ", 4)

    program_start_tm = time()
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.starmap(get_ohlc, 
                               zip(projLists.file_list, 
                                   repeat(filetype), 
                                   repeat(ticker)))

    data = pd.DataFrame(results, 
                        columns=["Date", "Open", "High", "Low", "Close"])

    print("Got ohlc data in", time() - program_start_tm, "seconds")
    data.to_csv(ticker + "_ohlc.csv", index=False)
