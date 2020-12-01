from matplotlib.widgets import Slider  # import the Slider widget

import numpy as np
import matplotlib.pyplot as plt
from math import pi





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