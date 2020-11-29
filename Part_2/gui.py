#!/usr/bin/env python3

import tkinter as tk
import query
import matplotlib



# create database class
db = query.MySQLDb()

# main window
window = tk.Tk(className="Corona")
window.geometry("600x200")


# init objects to show
date_from_label = tk.Label(window, text="Od:")
date_from = tk.Entry(window)
date_to_label = tk.Label(window, text="Do:")
date_to = tk.Entry(window)


# value of chosen queryA option
queryA_option_choice = tk.IntVar()
queryA_option_choice.set(0)

queryA_options_text = ["Graf abs. prírastku", "Graf perc. prírastku", "Kĺzavý priemer"]
queryA_options = []

# queryA option radiobutton
for val, text in enumerate(queryA_options_text):
    tmp = tk.Radiobutton(window, 
        text= text,
        width = 18,
        variable=queryA_option_choice, 
        value=val)
    tmp.place(relx=0.3*val, rely=0.65)
    queryA_options.append(tmp)


# show and hide objects due to choosen query
def prepare_query():
    actual_query = query_choice.get()
    
    if actual_query == 0:
        date_from_label.place(relx=0, rely=0.35)
        date_from.place(relx=0, rely=0.45) 
        date_to_label.place(relx=0.5, rely=0.35)
        date_to.place(relx=0.5, rely=0.45) 
        for i in range(3):
            queryA_options[i].place(relx=0.3*i, rely=0.65)

        
    elif actual_query == 1:
        date_from_label.place_forget()
        date_from.place_forget()
        date_to_label.place_forget()
        date_to.place_forget()
        for i in queryA_options:
            i.place_forget()

    elif actual_query == 2 :
        date_from_label.place_forget()
        date_from.place_forget()
        date_to_label.place_forget()
        date_to.place_forget()
        for i in queryA_options:
            i.place_forget()




# value of chosen query in radiobutton
query_choice = tk.IntVar()
query_choice.set(0)

prepare_query()

# constructor for radiobutton for Queries
query_text = ["Dotaz A", "Dotaz B", "Dotaz C"]

for val, text in enumerate(query_text):
    tk.Radiobutton(window, 
        text= text,
        indicatoron = 0,
        width = 100,
        variable=query_choice, 
        command=prepare_query,
        value=val).pack(anchor=tk.W)





def HandleQuery():
    choosen_query = query_choice.get()
    
    if choosen_query == 0:
        choosen_option = queryA_option_choice.get()

        if choosen_option == 0:
            print("ahoj dotaz A opt 1")

        elif choosen_option == 1:
            print("ahoj dotaz A opt 2")

        elif choosen_option == 2:
            print("ahoj dotaz A opt 3")

    elif choosen_query == 1:
        print("ahoj dotaz B")

    elif choosen_query == 2:
        print("ahoj dotaz C")


    queryWindow = tk.Tk(className="Dotaz")
    queryWindow.mainloop()


B1 = tk.Button(window, text="Spracuj dotaz", width=10, command=HandleQuery)


B1.place(x=200, rely=0.8)






window.mainloop()