import tkinter as tk
import matplotlib.pyplot as plt
import datetime
from tkinter import messagebox
from matplotlib.widgets import Slider  # import the Slider widget
import numpy as np
from math import sqrt
from matplotlib.ticker import ScalarFormatter

def show_grapfh_abs_illness(table):
    
    dates = [x[0] for x in table]
    values = [x[1] for x in table]

    fig, ax = plt.subplots()
    ax.plot_date(dates, values, marker='', linestyle='solid')
    fig.autofmt_xdate()
    ax.set_xlim([dates[0], dates[-1]])
    plt.ylabel("Prírastok nakazených")
    plt.xlabel("Dátum")
    plt.title("Nové prípady")
    plt.show()


def show_grapfh_perc_illness(table, pop):
    
    dates = [x[0] for x in table]
    values = [x[1] for x in table]
    perc_values = [values[i+1]*100/values[i] for i in range(len(values)-1)]

    fig, ax = plt.subplots()
    ax.plot_date(dates[1:], perc_values, marker='', linestyle='solid')
    fig.autofmt_xdate()
    ax.set_xlim([dates[0], dates[-1]])
    plt.ylabel("Percentuálny nárast [ % ]")
    plt.xlabel("Dátum")
    plt.title("Percetuálny prírastok vzhľadom na predchádzajúci deň")
    plt.show()


def show_moving_average(table):
    dates = [x[0] for x in table]
    values = [int(x[1]) for x in table]

    
    week_values = [values[i:i+6] for i in range(len(values)-6)]
    week_sorted_values = [sorted(i) for i in week_values]
    week_median = [i[3] for i in week_sorted_values]

    fig, ax = plt.subplots()
    ax.plot_date(dates[6:], week_median, marker='', linestyle='solid')
    fig.autofmt_xdate()
    ax.set_xlim([dates[0], dates[-1]])
    plt.title("Kĺzavý medián")
    plt.ylabel("Medián nových prípadov")
    plt.xlabel("Dátum")
    plt.show()

    plt.show()  



def moving_graph(table, date_from, region):
    a_min = 0    # the minimial value of the paramater a
    a_max = len(table)-10   # the maximal value of the paramater a
    a_init = len(table)-10   # the value of the parameter a to be used initially, when the graph is created

    actual_date = datetime.date(int(date_from[0:4]), int(date_from[5:7]), int(date_from[8:10]))
    delta = datetime.timedelta(days=a_max)
    actual_date += delta

    x = [x[0] for x in table[0]]
    y = [int(y[1]) for y in table[-10]]
    lines = [line for line in table]
    values = []
    for line in lines:
        for value in line:
            values.append(int(value[1]))
    max_y = max(values)
    max_x = len(x)

    fig = plt.figure(figsize=(12,7))

    # # first we create the general layount of the figure
    # # with two axes objects: one for the plot of the function
    # # and the other for the slider
    y_ax = plt.axes([0.1, 0.3, 0.8, 0.55])
    slider_ax = plt.axes([0.1, 0.02, 0.8, 0.05])
    slider_ax.set_xticks([0,1,2,3])

    # # in plot_ax we plot the function with the initial value of the parameter a
    plt.axes(y_ax) # select sin_ax
    plt.title(region + ' - ' + str(actual_date))
    plt.bar(x,y)
    plt.tick_params(rotation=60)
    plt.xlim(-0.5, max_x-0.5)
    plt.ylim(0, max_y)

    # # here we create the slider
    a_slider = Slider(slider_ax,      # the axes object containing the slider
                    'a',            # the name of the slider parameter
                    a_min,          # minimal value of the parameter
                    a_max,          # maximal value of the parameter
                    valinit=a_init  # initial value of the parameter
                    )

    # # Next we define a function that will be executed each time the value
    # # indicated by the slider changes. The variable of this function will
    # # be assigned the value of the slider.
    def update(a):
        actual_date = datetime.date(int(date_from[0:4]), int(date_from[5:7]), int(date_from[8:10]))
        delta = datetime.timedelta(days=a)
        actual_date += delta

        plt.cla()
        plt.axes(y_ax)
        plt.title(region + ' - ' + str(actual_date))
        plt.tick_params(rotation=60)
        plt.xlim(-0.5, max_x-0.5)
        plt.ylim(0, max_y)
        y = [int(y[1]) for y in table[int(a)]]
        try:
            plt.bar(x,y)
        except Exception:
            pass
            


    a_slider.on_changed(update)

    plt.show()

def show_country_graph(table, country):
    lines = [x for x in table]
    dates = [x[0] for x in lines]
    new_cases = [x[1] for x in lines]
    tests_done = [x[2] for x in lines]

    y_ax = plt.axes([0.1, 0.2, 0.8, 0.7])
    

    plt.axes(y_ax)
    plt.xlim(min(dates), max(dates))
    plt.plot( dates, new_cases, marker='', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label="Nové prípady")
    plt.plot( dates, tests_done, marker='', color='olive', linewidth=2, label="Vykonané testy")
    plt.legend()
    plt.yscale(value="log")
    
    plt.title(country)
    plt.tick_params(axis='x', rotation=60)
    y_ax.yaxis.set_major_formatter(ScalarFormatter())
 
    plt.show()  

def show_country_perc_graph(table, country):
    lines = [x for x in table]
    dates = [x[0] for x in lines]
    values = [x[1] for x in lines]

    plt.axes([0.1, 0.2, 0.8, 0.65])
    plt.plot( dates, values, marker='', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    plt.ylabel("[%]")
    plt.yscale(value="linear")
    plt.title(country + " - percentuálny nárast nových prípadov\nvzhľadom na vykonané testy")
    plt.tick_params(rotation=60)

    plt.show()  

def evaluate_corelation(date_from, date_to, country, table):
    lines = [x for x in table]
    x = [int(x[1]) for x in lines]   # new cases
    y = [int(x[2]) for x in lines]   # tests done


    n = len(table)
    xy = [x[i]*y[i] for i in range(n)]
    x2 = [i**2 for i in x]
    y2 = [i**2 for i in y]
    sumX = sum(x)
    sumY = sum(y)
    sumXY = sum(xy)
    sumX2 = sum(x2)
    sumY2 = sum(y2)
    sum2X = sumX**2
    sum2Y = sumY**2
  
    corelation = (n * sumXY - sumX * sumY)/(sqrt(n * sumX2 - sum2X) * sqrt(n * sumY2 - sum2Y))

    messagebox.showinfo("Korelačný koeficient", "Korelačný koeficient pre " + country + " za obdobie\n"+str(date_from)+" - "+str(date_to)+"\nje\n"+str(corelation))
