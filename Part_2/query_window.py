import tkinter as tk
import matplotlib.pyplot as plt
import datetime
from tkinter import messagebox
from matplotlib.widgets import Slider  # import the Slider widget
import numpy as np

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

def show_region_graph(region, date_from, date_to):
    a_min = 0    # the minimial value of the paramater a
    a_max = 10   # the maximal value of the paramater a
    a_init = 1   # the value of the parameter a to be used initially, when the graph is created

    pass

    # query_window = tk.Tk(className="Region")
    # query_window.geometry("600x500")



    # for i in range(len(table)):
    #     for j in range(len(table[0])):
    #         l = tk.Label(query_window, text=table[i][j])
    #         l.grid(row=i, column=j, sticky="wens")
    

    # for x in range(len(table)):
    #     tk.Grid.rowconfigure(query_window, x, weight=20)

    # for x in range(len(table[0])):
    #     tk.Grid.columnconfigure(query_window, x, weight=1)

    # query_window.mainloop()

def show_country_graph(date_from, date_to):
    a_min = 0    # the minimial value of the paramater a
    a_max = 10   # the maximal value of the paramater a
    a_init = 1   # the value of the parameter a to be used initially, when the graph is created

    x = [0,1,2,3,4,5,6]
    y = [5,7,5,10,5,7,2]

    fig = plt.figure(figsize=(8,3))

    # first we create the general layount of the figure
    # with two axes objects: one for the plot of the function
    # and the other for the slider
    sin_ax = plt.axes([0.1, 0.2, 0.8, 0.65])
    slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])


    # in plot_ax we plot the function with the initial value of the parameter a
    plt.axes(sin_ax) # select sin_ax
    plt.title('y = sin(ax)')
    plt.bar(x,y)
    plt.xlim(0, 10)
    plt.ylim(0, 15)

    # here we create the slider
    a_slider = Slider(slider_ax,      # the axes object containing the slider
                    'a',            # the name of the slider parameter
                    a_min,          # minimal value of the parameter
                    a_max,          # maximal value of the parameter
                    valinit=a_init  # initial value of the parameter
                    )

    # Next we define a function that will be executed each time the value
    # indicated by the slider changes. The variable of this function will
    # be assigned the value of the slider.
    def update(a):
        plt.cla()
        plt.axes(sin_ax) # select sin_ax
        plt.title('y = sin(ax)')
        plt.xlim(0, 10)
        plt.ylim(0, 15)
        y[5] = a
        plt.bar(x,y)


    a_slider.on_changed(update)

    plt.show()
