from tkinter import *

import matplotlib.pyplot as plt
import mplcursors as cc
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap


def put(fname, reso, col, size):
    # Generates the map, plots the coords and stores and retrieves data of each point
    if not size:
        size = 40
    size = int(size)
    try:
        df = pd.read_excel(fname)
        final = [list(map(float, df["Long"])), list(map(float, df["Lat"]))]
        # id_ = list(map(str, df['ID']))
        id_To = list(map(str, df["Station1"]))
        id_From = list(map(str, df["Station2"]))
        dates = list(map(str, df["Date"]))
        times = list(map(str, df["Time"]))
        colours = ["r", "g", "b", "c", "m", "y", "coral"]
        if col and col not in colours:
            colours.append(col)
        m = Basemap(
            projection="mill",
            # llcrnrlat=4,
            # urcrnrlat=37,
            # llcrnrlon=65,
            # urcrnrlon=100,
            #  Uncomment the above values to specify a particular part of the world map (above values are for the India-Pacific region)
            resolution=reso,
        )
        # NOTE: Higher resolution takes longer to load and will be heavier to store and render
        m.drawcountries()
        m.drawstates()
        m.drawcoastlines()
        m.drawparallels(np.arange(-90, 90, 10), labels=[True, True, False, False])
        m.drawmeridians(np.arange(-180, 180, 30), labels=[False, False, False, True])
        m.drawmapboundary(fill_color="aqua")
        m.fillcontinents(color="w", lake_color="aqua")
        p = len(colours)
        for x in range(len(final[0])):
            m.scatter(
                final[0][x],
                final[1][x],
                c=colours[x % p],
                s=size,
                latlon=True,
                label=f"({str(final[0][x])}, {str(final[1][x])})\nStation To: {id_To[x]}\nStation From: {id_From[x]}\nDate: {dates[x]}\nTime: {times[x]}",
            )
        plt.title("Coordinates Mapped")
        cc.cursor().connect(
            "add", lambda sel: sel.annotation.set_text(sel.artist.get_label())
        )
        plt.show()

    except Exception as e:
        w2 = Tk()
        w2.title("Error")
        w2.geometry(
            "+%d+%d"
            % ((w2.winfo_screenwidth() / 2) - 200, (w2.winfo_screenheight() / 2) - 125)
        )
        Label(w2, text=f"{type(e).__name__}: {e}").pack()


def plotter():
    # Displays menu
    w = Tk()
    w.title("Offline Geolocator")
    w.geometry(
        "+%d+%d"
        % ((w.winfo_screenwidth() / 2) - 200, (w.winfo_screenheight() / 2) - 125)
    )
    Label(w, text="Enter the path and name of the excel file:").grid()
    file = Entry(w)
    file.grid(row=0, column=1, columnspan=2)
    Label(
        w,
        text="Set the resolution of the map:",
    ).grid()
    reso = StringVar()
    reso.set("Choose")
    OptionMenu(w, reso, "f", "h", "i", "l", "c").grid(row=1, column=1)
    Label(w, text="(From slowest and clearest to fastest and roughest)").grid(
        row=2, column=0
    )
    Label(
        w, text="(Optional) Enter the desired size of the points (default = 40):"
    ).grid(row=3, column=0)
    Label(w, text="(Optional) Enter the desired colour option for the points:").grid(
        row=4, column=0
    )
    size = Entry(w)
    size.grid(row=3, column=1, columnspan=2)
    colour = Entry(w)
    colour.grid(row=4, column=1, columnspan=2)
    Button(
        w,
        text="Enter",
        command=lambda: put(file.get(), reso.get(), colour.get(), size.get()),
    ).grid(row=5, column=1, columnspan=2)
    mainloop()


if __name__ == "__main__":
    plotter()
