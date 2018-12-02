"""
projfuncs - the functions required for the crypto programs
=====================================================================

Put description here

Function List:
    in_fileList()
    get_fileList()
    get_tickerList()
    get_validInput()
    go_to_ticker()
    make_output()
    unix2time()

Issues:
    In go_to_ticker(), Tickers like X:SDAHEUR can be in the
    ticker list given in the project spec doc, but it may not
    be in a file like 20180202. Can make the ticker list using
    some code.
    
    In get_validInput(), if input is ALL and another input, something
    bad will probably happen (Fixed, needs testing)

Improvements that can be made:
    In go_to_ticker, write try-except block rather than
    raise SystemExit

    Can use os rather than glob for a more versatile
    list of files (but not needed)
"""

import pandas as pd
import gc
import getpass
import multiprocessing as mp
import pathlib
from datetime import datetime
from itertools import repeat
from glob import glob
from time import time
import projLists

###############
## Functions ##
###############

def in_fileList(a):
    """
    Returns True if there is at least one string in strlist
    where a is a substring of that string. Helper function
    to get_validInput().
    
    Args:
        a (string):
        strlist (list):
        
    Returns:
        bool: True if in list.
    """
    return any([a in i for i in projLists.file_list])

def get_fileList(filetype):
    """
    Gets the file list for a given file type

    Args:
        filetype (string): A or B
        
    Returns:
        projLists.file_list

    Improvements:
        Remove projList.file_list. Would have to
        modify programs to adopt this change.
    """
    if (filetype == "A"):
        projLists.file_list = sorted(glob("/space/crypto/PLUSTICK_1619_*"))
    else:
        projLists.file_list = sorted(glob("/space/crypto/PLUSTICK_FI_1356_*"))

    return projLists.file_list

def get_tickerList(date, filetype):
    """
    Gets all tickers from a file. List is written
    in projLists.ticker_list

    Args:
        date (string): the date to get tickers
    
    Returns:
        None
    """
    print("Getting ticker list...")
    if (filetype == "A"):
        fileloc = "/space/crypto/PLUSTICK_1619_" + date + ".txt"
    else:
        fileloc = "/space/crypto/PLUSTICK_FI_1356_" + date + ".txt"
    
    mylist = []
    init_tm = time()
    with open(fileloc, 'r') as finput:
        for line in finput:
            if (line.startswith("H")):
                mylist.append(line.split('|')[2])
        projLists.ticker_list = mylist
    print("Got ticker list in", time() - init_tm, "seconds")

def get_validInput(prompt, option, filetype=""):
    """
    Takes in user input, and returns that same input.
    The function will keep asking the user for valid
    input until the user inputs a string that's in its
    corresponding list
    
    Args:
        prompt (string): Ask the user what to input
        option (int): a number indicating the type of input
            to check against
            0: file
            1: ticker
            2: venue
            3: region
            4: filetype
    
    Returns:
        ui (string): the valid user input for the date if option is 0
        mylist: the valid user list for all other cases
    """

    inputerror = "Please enter an input"
    inputerror0 = "File does not exist."
    inputerror1 = "Ticker(s) not in data"
    inputerror2 = "Venue not in list"
    inputerror3 = "Region not in list"
    inputerror4 = "Please type 'A' or 'B'"
    
    while True:
        # Compatibility for python 2 and 3
        try:
            ui = raw_input(prompt)
        except NameError:
            ui = input(prompt)
        mylist = [x.strip() for x in ui.split(',')]
        # Removes duplicates, destroys order
        mylist = list(set(mylist))
        #if ("ALL" in mylist):
        #    mylist = ["ALL"]
        
        # Check if user input nothing or spaces
        if (mylist == ['']):
            print(inputerror)
        elif (option == 0):
            if (in_fileList(ui) and len(ui) == 8):
                get_tickerList(ui, filetype)
                return ui
            elif (ui == "list"):
                print("\n".join(projLists.file_list))
            else:
                print(inputerror0)
        elif (option == 1):
            # Checks if mylist is subset of ticker_list
            if (all(x in projLists.ticker_list for x in mylist)):
                break
            elif (ui == "list"):
                print("\n".join(projLists.ticker_list))
            else:
                print(inputerror1)
        elif (option == 2):
            if (all(x in projLists.venue_list for x in mylist)):
                break
            elif (ui == "list"):
                print("\n".join(projLists.venue_list))
            else:
                print(inputerror2)
        elif (option == 3):
            if (all(x in projLists.region_list for x in mylist)):
                break
            elif (ui == "list"):
                print("\n".join(projLists.region_list))
            else:
                print(inputerror3)
        else:
            if (ui in ["A", "B"]):
                get_fileList(ui)
                return ui
            else:
                print(inputerror4)
            
    return mylist

def go_to_ticker(finput, ticker):
    """
    Goes to the line where the ticker data is,
    and writes the ticker header to the file.
    
    Args:
        finput (file): the data file to search
        ticker (string): the ticker to go to
    
    Returns:
        None
    
    Raises:
        SystemExit: if ticker not found
    """
    flag = True

    # Keep reading until we find the ticker
    for line in finput:
        if (line.startswith('H')):
            if (line.split("|")[2] == ticker):
                flag = False
                break
        else:
            continue
    
    # If we went through entire file and did not break, print.
    if flag:
        print("Ticker", ticker, 
              "was in ticker list, but it is not in this file. Quitting.")
        raise SystemExit

def get_tickerData(fileloc, filetype, ticker, option, basic=True):
    """
    Gets the ticker data in a df format from one file

    Args:
        fileloc (string): the data file to get data
        filetype (string): A or B
        ticker (string):
        option (string): Q (quotes) or T (trades)
        basic (Bool): Set relevant subset of df if True

    Returns:
        df (pd.DataFrame): dataframe for ticker
    """

    with open(fileloc, 'r') as finput:
        datals = []

        # Go to ticker in file
        go_to_ticker(finput, ticker)

        for line in finput:
            if (line.startswith(option)):
                datals.append(line.strip('\n').split('|'))
            elif (line.startswith("H")):
                break
        
        if (filetype == "A"):
            if (option == "Q"):
                df = pd.DataFrame(datals, columns=projLists.typeA_Qcols)
                if (basic):
                    df = df.drop(columns=projLists.typeA_Qcols_rm)
            else:
                df = pd.DataFrame(datals, columns=projLists.typeA_Tcols)
                if (basic):
                    df = df.drop(columns=projLists.typeA_Tcols_rm)
        else:
            if (option == "Q"):
                df = pd.DataFrame(datals, columns=projLists.typeB_Qcols)
                if (basic):
                    df = df.drop(columns=projLists.typeB_Qcols_rm)
            else:
                df = pd.DataFrame(datals, columns=projLists.typeB_Tcols)
                if (basic):
                    df = df.drop(columns=projLists.typeB_Tcols_rm)
        
        # Cast to int if possible
        df = df.apply(pd.to_numeric, errors='ignore')

        # Deal with timestamp
        df.rename(columns={"Activity Datetime": "Time"}, inplace=True)
        df.Time = pd.to_datetime(df.Time, unit='s')
        # Convert to EST
        #df.Time = df.Time.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
        # Use the bottom since plotly doesn't support timezones
        # df.Time = df.Time + pd.Timedelta('-04:00:00')

    # Manually run garbage collection (may not be needed)
    gc.collect()

    return df

############################
# Functions for Daily Data #
############################

def get_closingPrice(fileloc, filetype, ticker, venue):
    """
    Helper function to get_tickerDailyData()

    Args:
        fileloc (str): 
        filetype (str):
        ticker (str):
        venue (str)
    
    Returns:
        formatted_date: date in yyyy-mm-dd format
        price: Last trade price before close_time (4:00pm)
    """
    # Indices
    time_i = 2
    price_i = 3
    if (filetype == "A"):
        venue_i = 6
    else:
        venue_i = 8

    # Get the date
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    formatted_date = '-'.join([date[:4], date[4:6], date[6:]])
    
    # 4:00 PM in unixtimestamp
    close_time = "16:00"
    pivot = time2unix(date, close_time)
    
    with open(fileloc, 'r') as finput:
        # Check if ticker is in file
        try:
            go_to_ticker(finput, ticker)
        except SystemExit:
            print("Ticker Does not exist")
            return [formatted_date, None]
        
        price = -1

        for line in finput:
            if (line.startswith("H")):
                if (price == -1):
                    print("No trades found, alg did not past 4pm", 
                          "and reached end of data")
                    break
                else:
                    # Return the most recent price if we reach end of
                    # data before 4pm
                    return [formatted_date, price]
            elif (line.startswith("T")):
                sline = line.split('|')
                if (float(sline[time_i]) > pivot):
                    # If we reach 4pm, but there were no trades,
                    # print message and return None
                    if (price == -1):
                        print("Reached 4pm, but no trades occured")
                        break
                    return [formatted_date, price]
                # If we are before 4pm, if we have empty venue string,
                # record price (doesn't matter what the current venue is)
                # If we have a nonempty string, then if current venue is
                # equal to venue, record price
                elif (not venue or sline[venue_i] == venue):
                    price = sline[price_i]
                # venue is not empty and venue does not match trade
                # row venue, continue
                else:
                    continue
            # If quote line
            else:
                continue

        if (price == -1):
            return [formatted_date, None]
        # else:
        #     with open("dailydata_helperlog.txt", "a+") as f:
        #         f.write("You messed up on ticker " + ticker + "\n")

def get_tickerDailyData(ticker, filetype, venue="", write_csv=True):
    """
    Get closing price by 4pm EST
    
    Args:
        ticker (str):
        filetype (str): A or B
        venue (str): Default "", meaning don't filter
            by venue
        write_csv (Bool): export df as csv if True

    Returns:
        df (pd.DataFrame): the daily ticker data
    """
    myls = []
    
    # Get file list and make list of closing prices
    get_fileList(filetype)
    for fileloc in projLists.file_list:
        myls.append(get_closingPrice(fileloc, filetype, ticker, venue))
    
    df = pd.DataFrame(myls, columns=["Date", ticker])
    df.set_index("Date", inplace=True)

    if (df[ticker].isnull().all()):
        print("There is no Close data for", ticker)
        return None
    else:
        if(write_csv):
            if not venue:
                dirpath = "daily_closing_prices/" + filetype + "/ALL" + "/"
            else:
                dirpath = "daily_closing_prices/" + filetype + "/" + venue + "/"
            pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
            filename = ticker + "_" + filetype + "_" + venue + ".csv"
            df.to_csv(dirpath + filename)

        return df

########
# OHLC #
########

def get_ohlcOneDay(fileloc, filetype, ticker):
    """
    Helper function to get_ohlc(). Gets ohlc for
    one day

    Args:
        fileloc (string): file location
        filetype (string): A or B
        ticker (string): ticker

    Returns:
        data, ohlc
    """
    # Get formatted date
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    formatted_date = '-'.join([date[:4], date[4:6], date[6:]])

    df = get_tickerData(fileloc, filetype, ticker, "T")
    
    if (df.empty):
        return None

    o = df["Trade Price"][0]
    h = df["Trade Price"].max()
    l = df["Trade Price"].min()
    c = df["Trade Price"][df.shape[0] - 1]

    return [formatted_date, o, h, l, c]

def get_olhc(ticker, filetype, write_csv=True):
    """
    Get open-high-low-close of ticker given a filetype

    Args:
        ticker (string): ticker
        filetype (string): A or B

    Returns:
        data (pd.DataFrame): ohlc for ticker
    """
    filelist = get_fileList(filetype)

    # Get ohlc for all days with parallel processing
    with mp.Pool(mp.cpu_count()) as p:
        results = p.starmap(get_ohlcOneDay, 
                            zip(filelist, repeat(filetype), repeat(ticker)))

    data = pd.DataFrame(results, 
                        columns=["Date", "Open", "High", "Low", "Close"])
    data.set_index("Date", inplace=True)

    if (data.dropna().empty):
        print("There is no ohlc for ticker", ticker)
        return None

    if (write_csv):
        # Make dir and export csv
        dirpath = "ohlc/"
        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
        data.to_csv(dirpath + ticker + "_" + filetype + "_ohlc.csv", 
                  index=False)

    return data

########
# VWAP #
########

def VWAP_helper(fileloc, filetype, ticker):
    """
    Helper function to get_VWAP(). Gets VWAP for
    one day
    """
    # Get the date
    fsplit = fileloc.split('_')
    date = fsplit[len(fsplit) - 1][:-4]
    formatted_date = '-'.join([date[:4], date[4:6], date[6:]])

    try:
        data = get_tickerData(fileloc, filetype, ticker, "T")
    except SystemExit:
        return [formatted_date, None]

    if (data.empty):
        return [formatted_date, None]

    VWAP = data["Trade Price"].dot(data["Trade Size Dec"]) / data["Trade Size Dec"].sum()
    return [formatted_date, VWAP]

def get_VWAP(ticker, filetype="B", write_csv=True):
    """
    Get daily volume weighted average price
    for a ticker and filetype

    Args:
        ticker (string):
        filetype (string): Default is B since A has
            no volume data
        write_csv (Bool): export df as csv if True

    Returns:
        df (pd.DataFrame): the daily VWAP for given ticker
    """
    filelist = get_fileList(filetype)
    with mp.Pool(mp.cpu_count()) as p:
        results = p.starmap(VWAP_helper,
                            zip(filelist, repeat(filetype), repeat(ticker)))
        
    df = pd.DataFrame(results, columns=["Date", ticker + "_VWAP"])
    df.set_index("Date", inplace=True)

    if (df.dropna().empty):
        print("There is no VWAP data for ticker", ticker)
        return None

    if (write_csv):
        dirpath = "vwap/"
        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
        df.to_csv(dirpath + ticker + "_vwap.csv", index=False)

    return df

######################
# Auxilary Functions #
######################

def fileHead(fileloc, n=10):
    with open(fileloc, 'r') as f:
        for i in range(n):
            print(next(f), end = '')

def tickerHead(fileloc, ticker, n=10):
    with open(fileloc, 'r') as f:
        go_to_ticker(f, ticker)
        for i in range(n):
            print(next(f), end='')

def unix2time(unix_ts, include_date=False, hour24=False, dt_obj=False):
    """
    Given a unix timestamp, return a human readable time.
    
    Args:
        unix_ts (float): a unix timestamp
        include_date (Bool): include the date if True
        hour24 (Bool): format as 24 hour if True
    
    Returns:
        tm (string): the human readable time
    """
    tm = datetime.fromtimestamp(unix_ts)

    # Returns the datetime object
    if (dt_obj):
        return tm
    
    #returns a string
    if (include_date):
        if (hour24):
            tm = tm.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            tm = tm.strftime('%Y-%m-%d %I:%M:%S.%f %p')
    else:
        if (hour24):
            tm = tm.strftime('%H:%M:%S.%f')
        else:
            tm = tm.strftime('%I:%M:%S.%f %p')
    
    return tm

def time2unix(date, tm):
    """
    Convert from readable time to unix timestamp.
    Could use pytz for better solution.
    
    Args:
        date (string): the date
        tm (string): the time (assumed EST)
    
    Returns:
        timestamp (int): unix timestamp (UTC)
    """
    #epoch = datetime(1970,1,1) 
    epoch = datetime.utcfromtimestamp(0) # Start of the Unix Epoch
    offset = 60*60*4 # Adjust for time zone
    
    dt = date + tm
    # Get datetime object
    if (any(i in tm for i in ["AM", "PM"])):
        dt = datetime.strptime(dt, '%Y%m%d%I:%M %p')
    else:
        dt = datetime.strptime(dt, '%Y%m%d%H:%M')
    
    dt = dt - epoch
    timestamp = int(dt.total_seconds() + offset)
    return timestamp