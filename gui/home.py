import tkinter as tk
from tkinter import ttk

def inv_page():
    inventory_page.tkraise()

def cust_page():
    customer_page.tkraise()

root = tk.Tk()
root.title("Video Store Inventory")
root.geometry("900x600")

#Inventory Page
inventory_page = tk.Frame(root)

#Header Frame
header = tk.Frame(inventory_page, height=50, bd=2, relief='solid')
header.pack(fill='x')
header.propagate(False)

#Name top left
name = tk.Label(header, text="Video Store")
name.pack(side='left', padx=10)

#Menu button top right
menu = tk.Button(header, text='Placeholder')
menu.pack(side='right', padx=10)

#Main search
main_search = tk.Entry(header, width=70,)
main_search.pack(expand=True)




#Tabs Bar (Sort, Filter, Inventory, Customer)
tabs = tk.Frame(inventory_page, height=50, bd=2, relief='solid')
tabs.pack(fill='x')
tabs.propagate(False)

#Sort button
def inv_show_sort():
    flt.pack_forget()
    sort.pack(side='left', before=table_section, padx=0, fill='y')
    sort_but.config(bg='blue')
    flt_but.config(bg='white')
sort_but = tk.Button(tabs, text='Sort', width=14, bg='blue', command=inv_show_sort)
sort_but.pack(side='left', padx=0, fill='both')

#Filter button
def inv_show_flt():
    sort.pack_forget()
    flt.pack(side='left', before=table_section, padx=0, fill='y')
    flt_but.config(bg='blue')
    sort_but.config(bg='white')
flt_but = tk.Button(tabs, text='Filter', width=14, command=inv_show_flt)
flt_but.pack(side='left', padx=0, fill='both')

#Invintory Button
inv_but = tk.Button(tabs, text='Inventory', bg='blue', command=inv_page)
inv_but.pack(side='left', padx=0, fill='both',expand=True)

#Customer button
cust_but = tk.Button(tabs, text='Customer', command=cust_page)
cust_but.pack(side='left', padx=0, fill='both', expand=True)




#Main content
main_box = tk.Frame(inventory_page, bd=2, relief='solid')
main_box.pack(fill='both', expand=True)
main_box.propagate(False)

#Sidebar (left)
#Sort Section
sort = tk.Frame(main_box, bd=2, relief='solid', width=215, bg='lightblue')
sort.pack(side='left', padx=0, fill='y')
sort.propagate(False)
sort.propagate(False)
#Filter Section
flt = tk.Frame(main_box, bd=2, relief='solid', width=215, bg='lightblue')
flt.propagate(False)

#Sort Box (left)
name = tk.BooleanVar()
year = tk.BooleanVar()
director = tk.BooleanVar()
rating = tk.BooleanVar()
genre = tk.BooleanVar()
rental_status = tk.BooleanVar()
tk.Checkbutton(sort, text='Name', variable=name, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(sort, text='Year', variable=year, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(sort, text='Director', variable=director, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(sort, text='Rating', variable=rating, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(sort, text='Genre', variable=genre, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(sort, text='Rental Status', variable=rental_status, bg='lightblue').pack(anchor='w', padx=10, pady=10)

#Filter Box (left)
#Rental Status (Inside of Filter Box)
tk.Label(flt, text='Rental Status', bg='lightblue').pack(anchor='w', padx=10, pady=(10, 0))
rent_stat_box = tk.StringVar(value='year')
tk.Radiobutton(flt, text='Available', variable=rent_stat_box, value='rent_stat_box', bg='lightblue').pack(anchor='w', padx=10)

#Year Box (Inside of Filter Box)
tk.Label(flt, text='Year:', bg='lightblue').pack(anchor='w', padx=10, pady=(10, 0))
year_box = tk.Frame(flt, bg='lightblue', bd=2, relief='solid')
year_box.pack(padx=2, side='top', fill='x')
year = tk.StringVar(value='year')
#Year Boc Radio Buttons
tk.Radiobutton(year_box, text='2020+', variable=year, value='2020+', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='2010-2020', variable=year, value='2010s', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='2000-2010', variable=year, value='2000s', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='1990-2000', variable=year, value='1990s', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='1980-1990', variable=year, value='1980s', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='1970-1980', variable=year, value='1970s', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='1960-1970', variable=year, value='1960s', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(year_box, text='Up tp 1960', variable=year, value='1900s=', bg='lightblue').pack(anchor='w', padx=10)

#Rating Box (Inside of Filter)
tk.Label(flt, text='Rating:', bg='lightblue').pack(anchor='w', padx=10, pady=(10,0))
rating_box = tk.Frame(flt, bg='lightblue', bd=2, relief='solid')
rating_box.pack(padx=2, side='top', fill='x')
rating = tk.StringVar(value='rating')
#Genre Radio Buttons
tk.Radiobutton(rating_box, text='G', variable=rating, value='G', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(rating_box, text='PG', variable=rating, value='PG', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(rating_box, text='PG-13', variable=rating, value='PG-13', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(rating_box, text='R', variable=rating, value='R', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(rating_box, text='NC-17', variable=rating, value='NC-17', bg='lightblue').pack(anchor='w', padx=10)

#Genre Box (Inside of Filter)
tk.Label(flt, text='Genre:', bg='lightblue').pack(anchor='w', padx=10, pady=(10,0))
genre_box = tk.Frame(flt, bg='lightblue', bd=2, relief='solid')
genre_box.pack(padx=2, side='top', fill='x')
genre = tk.StringVar(value='genre')
#Genre Radio Buttons (placeholder)
tk.Label(genre_box, text='Placeholder', bg='lightblue').pack(anchor='w', padx=10)



#Table Display Section
table_section = tk.Frame(main_box, bd=2, relief='solid', bg='grey')
table_section.pack(side='left', padx=0, fill='both', expand=True)

#Button Row (Inside the table display)
table_section_but = tk.Frame(table_section, bg='grey')
table_section_but.pack(side='top', fill='x')

#Edit Button
edit_but = tk.Button(table_section_but, text='Edit', height= 1, width=4)
edit_but.pack(side='right' , padx=4, pady=4)

#Add button
add_but = tk.Button(table_section_but, text='Add', height= 1, width=4)
add_but.pack(side='left' , padx=4, pady=4)

#Customer table
#Frame of table
table_frame = tk.Frame(table_section, bd=2, relief='solid')
table_frame.pack(fill='both', expand=True, padx=5, pady=5)
col=("Title", 'Year', 'Director', 'Rating', 'Genre', 'Total Quantity')
#Table (Inventory)
table = ttk.Treeview(table_frame, columns=col, show='headings')
for col in col:
    table.heading(col, text=col)
table.pack(fill="both", expand=True)








#Customer Page
customer_page = tk.Frame(root)

cust_header = tk.Frame(customer_page, height=50, bd=2, relief='solid')
cust_header.pack(fill='x')
cust_header.propagate(False)

#Name top left
cust_name = tk.Label(cust_header, text="Changed")
cust_name.pack(side='left', padx=10)

#Menu button top right
cust_menu = tk.Button(cust_header, text='Placeholder')
cust_menu.pack(side='right', padx=10)

#Main search
cust_main_search = tk.Entry(cust_header, width=70,)
cust_main_search.pack(expand=True)




#Tabs Bar (Sort, Filter, Inventory, Customer)
cust_tabs = tk.Frame(customer_page, height=50, bd=2, relief='solid')
cust_tabs.pack(fill='x')
cust_tabs.propagate(False)

#Sort button

def cust_show_sort():
    cust_flt.pack_forget()
    cust_sort.pack(side='left', before=cust_table_section, padx=0, fill='y')
    cust_sort_but.config(bg='blue')
    cust_flt_but.config(bg='white')
cust_sort_but = tk.Button(cust_tabs, text='Sort', width=14, bg='blue', command=cust_show_sort)
cust_sort_but.pack(side='left', padx=0, fill='both')

#Filter button
def cust_show_flt():
    cust_sort.pack_forget()
    cust_flt.pack(side='left', before=cust_table_section, padx=0, fill='y')
    cust_flt_but.config(bg='blue')
    cust_sort_but.config(bg='white')
cust_flt_but = tk.Button(cust_tabs, text='Filter', width=14, command=cust_show_flt)
cust_flt_but.pack(side='left', padx=0, fill='both')

#Invintory Button
inv_but = tk.Button(cust_tabs, text='Inventory', command=inv_page)
inv_but.pack(side='left', padx=0, fill='both',expand=True)

#Customer button
cust_but = tk.Button(cust_tabs, text='Customer', bg='blue', command=cust_page)
cust_but.pack(side='left', padx=0, fill='both', expand=True)




#Main content
cust_main_box = tk.Frame(customer_page, bd=2, relief='solid')
cust_main_box.pack(fill='both', expand=True)
cust_main_box.propagate(False)

#Sidebar (left)
#Sort Section
cust_sort = tk.Frame(cust_main_box, bd=2, relief='solid', width=215, bg='lightblue')
cust_sort.pack(side='left', padx=0, fill='y')
cust_sort.propagate(False)
cust_sort.propagate(False)
#Filter Section
cust_flt = tk.Frame(cust_main_box, bd=2, relief='solid', width=215, bg='lightblue')
cust_flt.propagate(False)

#Sort Box (left)
f_name = tk.BooleanVar()
l_name = tk.BooleanVar()
address = tk.BooleanVar()
phone = tk.BooleanVar()
email = tk.BooleanVar()
tk.Checkbutton(cust_sort, text='First', variable=f_name, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(cust_sort, text='Last', variable=l_name, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(cust_sort, text='Address', variable=address, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(cust_sort, text='Phone', variable=phone, bg='lightblue').pack(anchor='w', padx=10, pady=10)
tk.Checkbutton(cust_sort, text='Email', variable=email, bg='lightblue').pack(anchor='w', padx=10, pady=10)

#Filter Box (left)
#Has A Rental (Inside of Filter Box)
tk.Label(cust_flt, text='Rental:', bg='lightblue').pack(anchor='w', padx=10, pady=(10, 0))
renting_box = tk.StringVar(value='rent_check')
tk.Radiobutton(cust_flt, text='Currently Renting', variable=renting_box, value='renting_box', bg='lightblue').pack(anchor='w', padx=10)

#Email Box (Inside of Filter Box)
tk.Label(cust_flt, text='Email:', bg='lightblue').pack(anchor='w', padx=10, pady=(10, 0))
cust_email_box = tk.Frame(cust_flt, bg='lightblue', bd=2, relief='solid')
cust_email_box.pack(padx=2, side='top', fill='x')
cust_year = tk.StringVar(value='year')
#Year Boc Radio Buttons
tk.Radiobutton(cust_email_box, text='Gmail', variable=cust_year, value='Gmail', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(cust_email_box, text='Icloud', variable=cust_year, value='Icloud', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(cust_email_box, text='Yahoo', variable=cust_year, value='Yahoo', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(cust_email_box, text='Outlook', variable=cust_year, value='Outlook', bg='lightblue').pack(anchor='w', padx=10)
tk.Radiobutton(cust_email_box, text='Other', variable=cust_year, value='Other', bg='lightblue').pack(anchor='w', padx=10)



#Table Display Section
cust_table_section = tk.Frame(cust_main_box, bd=2, relief='solid', bg='grey')
cust_table_section.pack(side='left', padx=0, fill='both', expand=True)

#Button Row (Inside the table display)
cust_table_section_but = tk.Frame(cust_table_section, bg='grey')
cust_table_section_but.pack(side='top', fill='x')

#Edit Button
cust_edit_but = tk.Button(cust_table_section_but, text='Edit', height= 1, width=4)
cust_edit_but.pack(side='right' , padx=4, pady=4)

#Add button
cust_add_but = tk.Button(cust_table_section_but, text='Add', height= 1, width=4)
cust_add_but.pack(side='left' , padx=4, pady=4)

#Customer table
#Frame of table
cust_table_frame = tk.Frame(cust_table_section, bd=2, relief='solid')
cust_table_frame.pack(fill='both', expand=True, padx=5, pady=5)
col=("First", 'Last', 'Address', 'Phone', 'Email')
#Table (Inventory)
cust_table = ttk.Treeview(cust_table_frame, columns=col, show='headings')
for col in col:
    cust_table.heading(col, text=col)
cust_table.pack(fill="both", expand=True)

inventory_page.place(x=0, y=0, relwidth=1, relheight=1)
customer_page.place(x=0, y=0, relwidth=1, relheight=1)

inventory_page.tkraise()






#Return Page


root.mainloop()