import pandas as pd
import multiprocessing as mp
import plotly.offline as py
import plotly.graph_objs as go
from glob import glob

def get_boxTrace(fileloc):
    ticker = fileloc.split('/')[5][:9]
    print("Getting", ticker)
    df = pd.read_csv(fileloc)
    volume = df["Trade Size Dec"][df["Trade Size Dec"] <= df["Trade Size Dec"].quantile(0.25)]
    trace = go.Box(y = volume, name = ticker)
    print("Done with", ticker)

    return trace

if __name__ == "__main__":

    filelist = glob("/space/mth693/common/volumedata/*")
    filelist = [x for x in filelist if "USDa" in x]

    with mp.Pool(mp.cpu_count()) as pool:
        traces = pool.map(get_boxTrace, filelist)
    
    layout = go.Layout(title = "Volume Boxplots for lower 25% (USD)")

    fig = go.Figure(data = traces, layout = layout)

    # Output plot

    py.plot(fig, filename="volumeBoxplots_USD.html", image = "png", 
            image_width=1600, image_height=900, image_filename="USD Boxplots")
