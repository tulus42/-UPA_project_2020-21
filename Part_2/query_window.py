import tkinter as tk
import matplotlib.pyplot as plt
import datetime

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
