import tkinter as tk
import matplotlib.pyplot as plt
import datetime
from tkinter import messagebox

def show_grapfh_abs_illness(table):
    
    dates = [x[0] for x in table]
    values = [x[1] for x in table]

    fig, ax = plt.subplots()
    ax.plot_date(dates, values, marker='', linestyle='solid')
    fig.autofmt_xdate()
    ax.set_xlim([dates[0], dates[-1]])
    plt.ylabel("Prírastok nakazených")
    plt.xlabel("Dátum")
    plt.show()


def show_grapfh_perc_illness(table, pop):
    
    dates = [x[0] for x in table]
    values = [x[1]*100/pop for x in table]

    fig, ax = plt.subplots()
    ax.plot_date(dates, values, marker='', linestyle='solid')
    fig.autofmt_xdate()
    ax.set_xlim([dates[0], dates[-1]])
    plt.ylabel("Prírastok nakazených [%]")
    plt.xlabel("Dátum")
    plt.show()


def show_moving_average(table):
    values = [x[1] for x in table]

    x = 2/(len(values) + 1)

    ema = 0

    for i in values:
        ema += x * (i - ema)

    messagebox.showinfo("Kĺzavý priemer", "Kĺzavý priemer za obdobie\n"+str(table[0][0])+" - "+str(table[-1][0])+"\nje\n"+str(ema))

