# Not needed for main functions. Used for aux funcs
ticker_list = ["X:SXBTXRP", "X:SXBTUST", "X:SXBTCAD", "X:SXBTCNY", "X:SXBTEUR", 
               "X:SXBTJPY", "X:SXBTMXN", "X:SXBTGBP", "X:SXBTRUB", "X:SXBTSGD", 
               "X:SXBTUSD", "X:SETHXBT", "X:SETHUST", "X:SETHCAD", "X:SETHCNY", 
               "X:SETHEUR", "X:SETHGBP", "X:SETHJPY", "X:SETHMXN", "X:SETHUSD", 
               "X:SLTCXBT", "X:SLTCUST", "X:SLTCCNY", "X:SLTCEUR", "X:SLTCGBP", 
               "X:SLTCJPY", "X:SLTCMXN", "X:SLTCUSD", "X:SXRPXBT", "X:SXRPEUR", 
               "X:SXRPJPY", "X:SXRPMXN", "X:SXRPUSD", "X:SDAHXBT", "X:SDAHEUR", 
               "X:SDAHGBP", "X:SDAHUSD", "X:SBCHXBT", "X:SBCHETH", "X:SBCHUST", 
               "X:SBCHEUR", "X:SBCHJPY", "X:SBCHGBP", "X:SBCHUSD", "X:SXCOEUR",
               "X:SXCOUSD", "X:SXCOXBT"]

file_list = []

# Could consider writing a get_venueList function
venue_list = ["BBK", "BFX", "BMX", "BSO", "BST", "BTC", "BCC", "BDC", "CEX", 
              "CNK", "CFL", "CNO", "EXM", "GPX", "ITB", "OKC", "OKX", "TRK", 
              "UNC", "VLT", "ZAF", "CNB", "CTC", "IGML", "KKN"]

region_list = ["ASI", "EUR", "NAM"]

#################################
# Column names for Type A files #
#################################

typeA_Qcols = ['#D=Q', 'Tas Seq', 'Activity Datetime', 'Bid Price', 'Bid Size',
               'Ask Price', 'Ask Size', 'Quote Cond_1', 'Contributor Id',
               'Region Code', 'City Code', 'Quote Datetime',
               'Exch Message Timestamp']

typeA_Tcols = ['#D=T', 'Tas Seq', 'Activity Datetime', 'Trade Price',
               'Trade Size', 'Trade Cond_1', 'Contributor Id', 'Region Code',
               'City Code', 'Trade Datetime', 'Exch Message Timestamp',
               'Trade Cond_2', 'Trade Cond_3', 'Trade Official Time', 
               'Trade Cond_4', 'Trade Cond_5', 'Extended Trade Cond',
               'Trade Official Date', 'Retransmission Flag']

# Column names to remove from A

typeA_Qcols_rm = ['#D=Q', 'Tas Seq', 'Quote Cond_1', 'Quote Datetime', 
                  'Exch Message Timestamp']

typeA_Tcols_rm = ['#D=T', 'Tas Seq',  'Trade Cond_1', 'Trade Datetime', 
                  'Exch Message Timestamp', 'Trade Cond_2', 'Trade Cond_3',
                  'Trade Official Time', 'Trade Cond_4', 'Trade Cond_5', 
                  'Extended Trade Cond', 'Trade Official Date', 
                  'Retransmission Flag']

#################################
# Column names for Type B files #
#################################

typeB_Qcols = ['#D=Q', 'Tas Seq', 'Activity Datetime', 'Ask Price', 
               'Bid Price', 'Quote Datetime', 'Quote Official Time',
               'Exch Message Timestamp', 'Bid Size Dec', 'Ask Size Dec', 
               'Contributor Id', 'Quote Official Date', 'Region Code', 
               'City Code', 'Quote Cond_4']

typeB_Tcols = ['#D=T', 'Tas Seq', 'Activity Datetime', 'Trade Price', 
               'Trade Datetime', 'Exch Message Timestamp', 'Trade Size Dec',
               'Trade Vol Dec', 'Contributor Id', 'Trade Official Date',
               'Trade Official Time', 'Region Code', 'City Code', 
               'Retransmission Flag']

# Column names to remove from B

typeB_Qcols_rm = ['#D=Q', 'Tas Seq', 'Quote Datetime', 'Quote Official Time',
               'Exch Message Timestamp', 'Quote Official Date', 'Quote Cond_4']

typeB_Tcols_rm = ['#D=T', 'Tas Seq', 'Trade Datetime', 'Exch Message Timestamp', 
                  'Trade Official Date', 'Trade Official Time', 
                  'Retransmission Flag']