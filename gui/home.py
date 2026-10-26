import tkinter as tk

root = tk.Tk()
root.title("Video Store Inventory")
root.geometry("900x600")

#Header Frame
header = tk.Frame(root, height=50, bd=2, relief='solid')
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
tabs = tk.Frame(root, height=50, bd=2, relief='solid')
tabs.pack(fill='x')
tabs.propagate(False)

#Sort button
sort_but = tk.Button(tabs, text='Sort', width=14)
sort_but.pack(side='left', padx=0, fill='both')

#Filter button
flt_but = tk.Button(tabs, text='Filter', width=14)
flt_but.pack(side='left', padx=0, fill='both')

#Invintory Button
inv_but = tk.Button(tabs, text='Inventory')
inv_but.pack(side='left', padx=0, fill='both',expand=True)

#Customer button
cust_but = tk.Button(tabs, text='Customer')
cust_but.pack(side='left', padx=0, fill='both', expand=True)




#Main content
main_box = tk.Frame(root, bd=2, relief='solid')
main_box.pack(fill='both', expand=True)
main_box.propagate(False)

#Sidebar (left)
#Sort Section
# sort = tk.Frame(main_box, bd=2, relief='solid', width=215, bg='lightblue')
# sort.pack(side='left', padx=0, fill='y')
# sort.propagate(False)
# sort.propagate(False)
#Filter Section
flt = tk.Frame(main_box, bd=2, relief='solid', width=215, bg='lightblue')
flt.pack(side='left', padx=0, fill='y')
flt.propagate(False)

#Sort Box (left)
# name = tk.BooleanVar()
# year = tk.BooleanVar()
# director = tk.BooleanVar()
# rating = tk.BooleanVar()
# genre = tk.BooleanVar()
# rental_status = tk.BooleanVar()
# tk.Checkbutton(sort, text='Name', variable=name, bg='lightblue').pack(anchor='w', padx=10, pady=10)
# tk.Checkbutton(sort, text='Year', variable=year, bg='lightblue').pack(anchor='w', padx=10, pady=10)
# tk.Checkbutton(sort, text='Director', variable=director, bg='lightblue').pack(anchor='w', padx=10, pady=10)
# tk.Checkbutton(sort, text='Rating', variable=rating, bg='lightblue').pack(anchor='w', padx=10, pady=10)
# tk.Checkbutton(sort, text='Genre', variable=genre, bg='lightblue').pack(anchor='w', padx=10, pady=10)
# tk.Checkbutton(sort, text='Rental Status', variable=rental_status, bg='lightblue').pack(anchor='w', padx=10, pady=10)

#Filter Box (left)
#Rental Status (Inside of Filter Box
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

root.mainloop()