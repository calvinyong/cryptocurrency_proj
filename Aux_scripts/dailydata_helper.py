import pandas as pd
import multiprocessing as mp
from itertools import repeat
import pathlib
import projfuncs as pf
import projLists
import sys

if __name__ == "__main__":
    #mytickers = ["X:SXBTUSD", "X:SETHUSD", "X:SLTCUSD", "X:SXRPUSD", 
    #             "X:SDAHUSD", "X:SBCHUSD"]

    try:
        filetype = sys.argv[1]
    except IndexError:
        print("Using Defaults")
        filetype = "A"

    mytickers = sorted(projLists.ticker_list)

    if (filetype == "A"):
        myvenues = ["CNB", "CTC", "IGML", "KKN", ""]
    else:
        myvenues = ["BBK", "BFX", "BMX", "BSO", "BST", "BTC", "BCC", "BDC", "CEX", 
                    "CNK", "CFL", "CNO", "EXM", "GPX", "ITB", "OKC", "OKX", "TRK", 
                    "UNC", "VLT", "ZAF", ""]
    
    dirpath = "daily_closing_prices/concat_data/" + filetype + "/"
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

    with mp.Pool(mp.cpu_count()) as p:
        for venue in myvenues:
            results = p.starmap(pf.get_tickerDailyData,
                                zip(mytickers, repeat(filetype), repeat(venue)))
            
            if (all(x is None for x in results)):
                print("No data for venue", venue)
                continue

            df = pd.concat(results, axis=1)
            df.to_csv(dirpath + "Alltickerdata_" + venue + ".csv")
            print("Daily data for type", filetype, "and venue", venue, "done")
 
    print("WOW. Incredible.")