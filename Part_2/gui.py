#!/usr/bin/env python3

import tkinter as tk
import query
import query_window
import datetime



# create database class
db = query.MySQLDb()

# main window
window = tk.Tk(className="Corona")
window.geometry("600x450")


# init objects to show ######

# pick date from-to
date_from_label = tk.Label(window, text="Dátum od:")
date_from_label.grid(row=3, column=0, columnspan=3)
date_from_label.config(font=(44))
date_from = tk.Entry(window)
date_from.insert(0, "2020-03-01")
date_from.grid(row=4, column=0, columnspan=3, sticky="we")

date_to_label = tk.Label(window, text="Dátum do:")
date_to_label.grid(row=3, column=3, columnspan=3)
date_to_label.config(font=(44))
date_to = tk.Entry(window)
date_to.insert(0, "2020-11-30")
date_to.grid(row=4, column=3, columnspan=3, sticky="we")


# value of chosen queryA option
queryA_option_choice = tk.IntVar()
queryA_option_choice.set(0)

queryA_options = []

# queryA option radiobutton
for val, text in enumerate(["Graf abs. prírastku", "Graf perc. prírastku", "Kĺzavý priemer"]):
    tmp = tk.Radiobutton(window, 
        text= text,
        width = 18,
        indicatoron = 0,
        variable=queryA_option_choice, 
        value=val)
    tmp.grid(row=8, column=val*2, columnspan=2, sticky="wens")
    queryA_options.append(tmp)

# queryA parameters
# gender:
queryA_param_gender = tk.IntVar()
queryA_param_gender.set(2)
for val, text in enumerate(["Muži", "Ženy", "Nezáleží"]):
    tmp = tk.Radiobutton(window, 
        text= text,
        width = 18,
        variable=queryA_param_gender, 
        value=val)
    tmp.grid(row=val+5, column=0, columnspan=2, sticky="wens")
    queryA_options.append(tmp)

# imported
queryA_param_imported = tk.IntVar()

queryA_param_imported_chbox = tk.Checkbutton(window, text="Len importované", variable=queryA_param_imported)
queryA_param_imported_chbox.grid(row=5, column=2, columnspan=4, sticky="wens")

# age
age_from_label = tk.Label(window, text="Vek od:")
age_from_label.grid(row=6, column=2, sticky="wens")
age_from = tk.Entry(window)
age_from.insert(0, "0")
age_from.grid(row=6, column=3, columnspan=3, sticky="wens")

age_to_label = tk.Label(window, text="Vek do:")
age_to_label.grid(row=7, column=2, sticky="wens")
age_to = tk.Entry(window)
age_to.insert(0, "100")
age_to.grid(row=7, column=3, columnspan=3, sticky="wens")


#########
# query B

# value of chosen queryB option
# queryB_order_choice = tk.IntVar()
# queryB_order_choice.set(0)

# queryB_orders = []

# # queryB option radiobutton
# for val, text in enumerate(["zoradenie 1", "zoradenie 2", "zoradenie 3"]):
#     tmp = tk.Radiobutton(window, 
#         text= text,
#         width = 18,
#         indicatoron = 0,
#         variable=queryB_order_choice, 
#         value=val)
#     tmp.grid(row=8, column=val*2, columnspan=2, sticky="wens")
#     queryB_orders.append(tmp)

# DISTRICT listbox
# district_listbox = tk.Listbox(window)
# district_listbox.grid(row=6, column=3, rowspan=2, columnspan=2, sticky="wens")

# district_scrollbar = tk.Scrollbar(window)
# district_scrollbar.grid(row=6, rowspan=2, column=5, sticky="wns")



# district_listbox.config(yscrollcommand = district_scrollbar.set)
# district_scrollbar.config(command = district_listbox.yview)

queryB_option = []


def regionSelect():
    prepare_query()
    if queryB_choice.get() == 1:        
        regions = db.get_regions()

        for region in regions:
            region_listbox.insert(tk.END, region)


# REGION listbox
region_listbox = tk.Listbox(window)
region_listbox.grid(row=6, column=0, rowspan=2, columnspan=2, sticky="wens")

region_scrollbar = tk.Scrollbar(window)
region_scrollbar.grid(row=6, rowspan=2, column=2, sticky="wns")



region_listbox.config(yscrollcommand = region_scrollbar.set)
region_scrollbar.config(command = region_listbox.yview)

# region_listbox.bind("<<ListboxSelect>>", regionselect)





# show and hide objects due to choosen query
def prepare_query():
    actual_query = query_choice.get()
    
    if actual_query == 0:
        date_from_label.grid()
        date_from.grid()
        date_to_label.grid()
        date_to.grid()
        queryA_param_imported_chbox.grid()
        age_from_label.grid()
        age_from.grid()
        age_to_label.grid()
        age_to.grid()
        for i in queryA_options:
            i.grid()

        region_listbox.grid_remove()
        region_scrollbar.grid_remove()
        # district_listbox.grid_remove()
        # district_scrollbar.grid_remove()
        for i in queryB_option:
            i.grid_remove()
        # for i in queryB_orders:
        #     i.grid_remove()

        
    elif actual_query == 1:
        date_from_label.grid()
        date_from.grid()
        date_to_label.grid()
        date_to.grid()
        queryA_param_imported_chbox.grid_remove()
        age_from_label.grid_remove()
        age_from.grid_remove()
        age_to_label.grid_remove()
        age_to.grid_remove()
        for i in queryA_options:
            i.grid_remove()

        actual_queryB_option = queryB_choice.get()

        # region_listbox.grid()
        # region_scrollbar.grid()
    
        if actual_queryB_option == 1:
            region_listbox.grid()
            region_scrollbar.grid()
            region_listbox.delete(0,tk.END)
        else:
            region_listbox.grid_remove()
            region_scrollbar.grid_remove()

        for i in queryB_option:
            i.grid()
        # for i in queryB_orders:
        #     i.grid()

    elif actual_query == 2 :
        date_from_label.grid_remove()
        date_from.grid_remove()
        date_to_label.grid_remove()
        date_to.grid_remove()
        queryA_param_imported_chbox.grid_remove()
        age_from_label.grid_remove()
        age_from.grid_remove()
        age_to_label.grid_remove()
        age_to.grid_remove()
        for i in queryA_options:
            i.grid_remove()

        region_listbox.grid_remove()
        region_scrollbar.grid_remove()
        # district_listbox.grid_remove()
        # district_scrollbar.grid_remove()
        for i in queryB_option:
            i.grid_remove()
        # for i in queryB_orders:
        #     i.grid_remove()






# value of chosen query in radiobutton
query_choice = tk.IntVar()
query_choice.set(0)

queryB_choice = tk.IntVar()
queryB_choice.set(0)



# queryB option radiobutton


for val, text in enumerate(["Všetky kraje", "Výber krajov"]):
    tmp = tk.Radiobutton(window, 
        text= text,
        width = 18,
        variable=queryB_choice, 
        command=regionSelect,
        value=val)
    tmp.grid(row=5, column=val*3, columnspan=3, sticky="wens")
    queryB_option.append(tmp)

prepare_query()

# constructor for radiobutton for Queries
query_text = ["Dotaz A", "Dotaz B", "Dotaz C"]

for val, text in enumerate(query_text):
    rButton = tk.Radiobutton(window, 
        text= text,
        indicatoron = 0,
        variable=query_choice, 
        command=prepare_query,
        width=100,
        height=2,
        value=val)
    rButton.grid(row=val, column=0, columnspan=6, sticky="wens")




def HandleQuery():
    choosen_query = query_choice.get()
    
    # QUERY A
    if choosen_query == 0:
        # get options for queryA
        choosen_option = queryA_option_choice.get()
        
        # get table with illness increase for all A options
        table = db.get_ill_increase_in_time(date_from.get(), date_to.get(), age_from.get(), age_to.get(), queryA_param_gender.get(), queryA_param_imported.get())

        # show graph of absolute illness increase
        if choosen_option == 0:
            query_window.show_grapfh_abs_illness(table)

        # show graph of percentual illness increase
        elif choosen_option == 1:
            pop = db.get_country_population("CZ")
            query_window.show_grapfh_perc_illness(table, pop)

        elif choosen_option == 2:
            query_window.show_moving_average(table)

    # QUERY B
    elif choosen_query == 1:
        
        # whole country - show by regions
        if queryB_choice.get() == 0:
            table = []
            
            start_date = date_from.get()
            start_date = datetime.date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
            end_date = date_to.get()
            end_date = datetime.date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
            delta = datetime.timedelta(days=1)

            while start_date <= end_date:
                table.append(db.get_data_per_day_groupby_region(start_date))
                start_date += delta

            
            # table.append(db.get_data_per_day_groupby_region(date_i))

            query_window.show_country_graph(table, date_from.get())

        # choice by region - show by districts
        else:
            index = region_listbox.curselection()
            if index != ():
                
                region = region_listbox.get(index)

                table = db.get_data_per_day_groupby_district_in_region(table, region)
                query_window.show_region_graph(region, date_from.get(), date_to.get())
    
        
            
        

    elif choosen_query == 2:
        print("ahoj dotaz C")


    
    


B1 = tk.Button(window, text="Spracuj dotaz", width=10, command=HandleQuery)

B1.grid(row=9, column=0, columnspan=6)


# set size of rows and cols
for x in range(3, 8):
    tk.Grid.rowconfigure(window, x, weight=3, minsize=8)

for x in range(8,10):
    tk.Grid.rowconfigure(window, x, weight=20)

for x in range(6):
    tk.Grid.columnconfigure(window, x, weight=1)

window.mainloop()