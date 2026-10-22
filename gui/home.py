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
sort_but = tk.Button(tabs, text='Sort')
sort_but.pack(side='left', padx=0, fill='both')

#Filter button
flt_but = tk.Button(tabs, text='Filter')
flt_but.pack(side='left', padx=0, fill='both')

#Invintory Button
inv_but = tk.Button(tabs, text='Inventory')
inv_but.pack(side='left', padx=0, fill='both')

#Customer button
cust_but = tk.Button(tabs, text='Customer')
cust_but.pack(side='left', padx=0, fill='both')

root.mainloop()