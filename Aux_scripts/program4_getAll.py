############################
##       Calvin Yong      ##
##    MTH 691 Program 4   ##
############################
'''
DF made in 78.3248 on server output file
(using .loc, don't use this lol)
'''
import pandas as pd
import multiprocessing as mp
from itertools import repeat
from time import time
import pathlib
import projfuncs as pf
import projLists

def get_program4Output(filetype, dirpath, collist, fileloc):

    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]

    if (filetype == "A"):
        venue_q = 8
        venue_t = 6
        region_q = 9
        region_t = 7
        volume = 4
    else:
        venue_q = 10
        venue_t = 8
        region_q = 12
        region_t = 11
        volume = 6

    pf.get_tickerList(date, filetype)
    projLists.ticker_list.remove("ALL")
    df = pd.DataFrame(data=0.0, index=projLists.ticker_list, columns=collist)
    
    init_tm = time()
    with open(fileloc, 'r') as finput:
        for i in range(6):
            next(finput)
        for line in finput:
            split_line = line.split('|')
            if (split_line[0] == "H"):
                curr_ticker = split_line[2]
            elif (split_line[0] == "Q"):
                # Update Q's for the venue and region
                df.at[curr_ticker, "Q-ALL"] += 1
                df.at[curr_ticker, "Q-" + split_line[venue_q]] += 1
                df.at[curr_ticker, "Q-" + split_line[region_q]] += 1
            else:
                # Update T's
                df.at[curr_ticker, "T-ALL"] += 1
                df.at[curr_ticker, "T-" + split_line[venue_t]] += 1
                df.loc[curr_ticker, "T-" + split_line[region_t]] += 1
                # Update V's. First line is not optimal
                # If we get empty string, do nothing
                try:
                    df.at[curr_ticker, "V-ALL"] += float(split_line[volume])
                    df.at[curr_ticker, "V-" + split_line[venue_t]] += float(split_line[volume])
                    df.at[curr_ticker, "V-" + split_line[region_t]] += float(split_line[volume])
                except ValueError:
                    pass
                     
    print("DF for " + date + " made in ", time() - init_tm, "seconds")
    #print(df)
    df.to_csv(dirpath + "program4_out_" + filetype + "_" + date + ".csv")


if __name__ == "__main__":
    filetype = pf.get_validInput("Type A or B files: ", 4)

    # Make dir for output if it doesn't exist
    dirpath = "output/program4_out/" + filetype + "/"
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

    # Column List
    collist = []
    projLists.ticker_list.remove("ALL")
    # To prevent duplicates when making collist
    projLists.region_list.remove("ALL")

    for x in projLists.venue_list:
        collist = collist + ["Q-" + x, "T-" + x, "V-" + x]
    for x in projLists.region_list:
        collist = collist + ["Q-" + x, "T-" + x, "V-" + x]

    # The magic
    with mp.Pool(16) as pool:
        pool.starmap(get_program4Output, 
                     zip(repeat(filetype), repeat(dirpath), repeat(collist), projLists.file_list))
    
    print("Type", filetype, "files done :D")