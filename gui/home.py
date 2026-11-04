import tkinter as tk
from tkinter import ttk, messagebox

from database.videos import (
    create_video, get_all_videos, get_video, update_video, delete_video, search_video
)
from database.customers import (
    create_customer, get_all_customers, get_customer, update_customer,
    delete_customer, search_customers
)
from database.rentals import get_active_rentals, return_rental


from gui.customer_history import CustomerHistoryFrame
from gui.rental import RentalFrame


def inv_page():
    refresh_inventory()
    inventory_page.tkraise()

def cust_page():
    refresh_customers()
    customer_page.tkraise()

def show_return_page():
    refresh_returns()
    return_page.tkraise()

def show_customer_hist():
    selected_id = int(cust_table.selection()[0]) if cust_table.selection() else None
    customer_hist.refresh_data(selected_id)
    customer_hist.tkraise()

def show_rental_page():
    rental_page.refresh_data()
    rental_page.tkraise()

root = tk.Tk()
root.title("Video Store Inventory")
root.geometry("900x600")

contain = tk.Frame(root)
contain.pack(fill='both', expand=True)

#Pages
inventory_page = tk.Frame(contain)
customer_page = tk.Frame(contain)
return_page = tk.Frame(contain)
customer_hist = CustomerHistoryFrame(contain,on_home=inv_page, on_rent=show_rental_page,on_history=show_customer_hist,on_return=show_return_page,)
rental_page = RentalFrame(contain,on_home=inv_page,on_rent=show_rental_page,on_history=show_customer_hist,on_return=show_return_page,)

#Inventory Page
#Header Frame
header = tk.Frame(inventory_page, height=50, bd=2, relief='solid')
header.pack(fill='x')
header.propagate(False)

#Name top left
name = tk.Label(header, text="Video Store")
name.pack(side='left', padx=10)

#Return button top right
menu = tk.Button(header, text='Return Movie', command=show_return_page)
menu.pack(side='right', padx=(1,10))

#Customer History Button
customer_hist_but = tk.Button(header, text='Customer History', command=show_customer_hist)
customer_hist_but.pack(side='right', padx=1)

#Rental Button
Rent = tk.Button(header, text='Rent', command=show_rental_page)
Rent.pack(side='right', padx=1)

#Main search
main_search = tk.Entry(header, width=30,)
main_search.place(relx=.51, rely=.25)




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

# Add, edit and delete act on the selected database ID
editing_video_id = None

def show_add():
    global editing_video_id
    editing_video_id = None
    clear_video_fields()
    add_submit.config(text='Save')
    entry_row.pack(fill='x', padx=5, pady=5)

def show_edit():
    global editing_video_id
    selection = table.selection()
    if not selection:
        messagebox.showwarning('Select a video', 'Select a video to edit first')
        return
    video_id = int(selection[0])
    try:
        video = get_video(video_id)
    except Exception as exc:
        messagebox.showerror('Database error', f'Could not load video:\n{exc}')
        return
    if video is None:
        messagebox.showwarning('Missing video', 'This video no longer exists')
        refresh_inventory()
        return
    editing_video_id = video_id
    for field, key in zip(video_fields, video_field_keys):
        field.delete(0, tk.END)
        value = video.get(key)
        field.insert(0, '' if value is None else str(value))
    add_submit.config(text='Update')
    entry_row.pack(fill='x', padx=5, pady=5)

def remove_video():
    selection = table.selection()
    if not selection:
        messagebox.showwarning('Select a video', 'Select a video to delete first')
        return
    video_id = int(selection[0])
    title = table.item(selection[0], 'values')[0]
    if not messagebox.askyesno('Delete video', f'Delete "{title}"? This cannot be undone'):
        return
    try:
        deleted = delete_video(video_id)
    except Exception as exc:
        messagebox.showerror('Delete failed',
                             f'Could not delete video\nIt may have rental history\n\n{exc}')
        return
    if not deleted:
        messagebox.showwarning('Missing video', 'Video was not found')
    cancel_video_edit()
    refresh_inventory()

add_but = tk.Button(table_section_but, text='Add', height=1, width=6, command=show_add)
add_but.pack(side='left', padx=4, pady=4)
edit_but = tk.Button(table_section_but, text='Edit', height=1, width=6, command=show_edit)
edit_but.pack(side='right', padx=4, pady=4)
delete_but = tk.Button(table_section_but, text='Delete', height=1, width=7, command=remove_video)
delete_but.pack(side='right', padx=4, pady=4)

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


def refresh_inventory():
    """Load videos from Supabase into the inventory table"""
    try:
        term = main_search.get().strip()
        videos = search_video(term) if term else get_all_videos()
    except Exception as exc:
        messagebox.showerror("Database error", f"Could not load inventory:\n{exc}")
        return

    table.delete(*table.get_children())
    for video in videos:
        table.insert(
            "", "end", iid=str(video["video_id"]),
            values=(
                video.get("title") or "",
                video.get("year") if video.get("year") is not None else "",
                video.get("director") or "",
                video.get("rating") if video.get("rating") is not None else "",
                video.get("genre") or "",
                video.get("total_quantity", 0)
            )
        )


#Add Insert
entry_row = tk.Frame(table_frame)
entry_row.pack_forget()

# Labeled inventory inputs

def inventory_field(label, width=12):
    field_frame = tk.Frame(entry_row)
    field_frame.pack(side='left', padx=2, fill='x', expand=True)
    tk.Label(field_frame, text=label, anchor='w').pack(fill='x')
    entry = tk.Entry(field_frame, bd=2, width=width)
    entry.pack(fill='x')
    return entry


title_entry = inventory_field("Title")
year_entry = inventory_field("Year", 6)
director_entry = inventory_field("Director")
rating_entry = inventory_field("Rating", 6)
genre_entry = inventory_field("Genre")
quantity_entry = inventory_field("Quantity", 6)
video_fields = (title_entry, year_entry, director_entry, rating_entry, genre_entry, quantity_entry)
video_field_keys = ('title', 'year', 'director', 'rating', 'genre', 'total_quantity')

def clear_video_fields():
    for field in video_fields:
        field.delete(0, tk.END)
    quantity_entry.insert(0, '0')

def cancel_video_edit():
    global editing_video_id
    editing_video_id = None
    entry_row.pack_forget()
    clear_video_fields()
    add_submit.config(text='Save')

quantity_entry.insert(0, "0")


def add_save():
    """Save a new or edited video and refresh inventory"""
    payload = {
        'title': title_entry.get(),
        'year': year_entry.get().strip(),
        'director': director_entry.get().strip(),
        'rating': rating_entry.get().strip(),
        'genre': genre_entry.get().strip(),
        'total_quantity': quantity_entry.get().strip()
    }
    try:
        if editing_video_id is None:
            saved = create_video(**payload)
        else:
            saved = update_video(editing_video_id, payload)
    except ValueError as exc:
        messagebox.showerror('Invalid video', str(exc))
        return
    except Exception as exc:
        messagebox.showerror('Database error', f'Could not save video:\n{exc}')
        return

    if saved is None:
        messagebox.showwarning('Missing video', 'This video no longer exists')
        return
    was_editing = editing_video_id is not None
    cancel_video_edit()
    refresh_inventory()
    messagebox.showinfo('Video updated' if was_editing else 'Video added',
                        f'Saved {saved["title"]}')


add_submit = tk.Button(entry_row, bd=4, text='Save', command=add_save)
add_submit.pack(side='left', padx=2, fill='x', expand=True)
tk.Button(entry_row, text='Cancel', command=cancel_video_edit).pack(side='left', padx=2, pady=(18, 0))

# Avoid querying the database on every keystroke
inventory_search_job = None

def schedule_inventory_search(_event=None):
    global inventory_search_job
    if inventory_search_job is not None:
        root.after_cancel(inventory_search_job)
    inventory_search_job = root.after(300, refresh_inventory)

main_search.bind('<KeyRelease>', schedule_inventory_search)







#Customer Page
cust_header = tk.Frame(customer_page, height=50, bd=2, relief='solid')
cust_header.pack(fill='x')
cust_header.propagate(False)

#Name top left
cust_name = tk.Label(cust_header, text="Video Store")
cust_name.pack(side='left', padx=10)

#Return button top right
cust_menu = tk.Button(cust_header, text='Return Movie', command=show_return_page)
cust_menu.pack(side='right', padx=(1,10))

#Customer History Button
customer_hist_but = tk.Button(cust_header, text='Customer History', command=show_customer_hist)
customer_hist_but.pack(side='right', padx=1)

#Rental Button
Rent = tk.Button(cust_header, text='Rent', command=show_rental_page)
Rent.pack(side='right', padx=1)

#Main search
cust_main_search = tk.Entry(cust_header, width=30)
cust_main_search.place(relx=.51, rely=.25)




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

# Add, edit and delete customers by their database IDs
editing_customer_id = None

def cust_show_add():
    global editing_customer_id
    editing_customer_id = None
    clear_customer_fields()
    cust_add_submit.config(text='Save')
    cust_entry_row.pack(fill='x', padx=5, pady=5)

def cust_show_edit():
    global editing_customer_id
    selection = cust_table.selection()
    if not selection:
        messagebox.showwarning('Select a customer', 'Select a customer to edit first')
        return
    customer_id = int(selection[0])
    try:
        customer = get_customer(customer_id)
    except Exception as exc:
        messagebox.showerror('Database error', f'Could not load customer:\n{exc}')
        return
    if customer is None:
        messagebox.showwarning('Missing customer', 'This customer no longer exists')
        refresh_customers()
        return
    editing_customer_id = customer_id
    for field, key in zip(customer_fields, customer_field_keys):
        field.delete(0, tk.END)
        field.insert(0, customer.get(key) or '')
    cust_add_submit.config(text='Update')
    cust_entry_row.pack(fill='x', padx=5, pady=5)

def remove_customer():
    selection = cust_table.selection()
    if not selection:
        messagebox.showwarning('Select a customer', 'Select a customer to delete first')
        return
    customer_id = int(selection[0])
    values = cust_table.item(selection[0], 'values')
    name = f'{values[0]} {values[1]}'.strip()
    if not messagebox.askyesno('Delete customer', f'Delete {name}? This cannot be undone'):
        return
    try:
        deleted = delete_customer(customer_id)
    except Exception as exc:
        messagebox.showerror('Delete failed',
                             f'Could not delete customer\nThey may have rental history\n\n{exc}')
        return
    if not deleted:
        messagebox.showwarning('Missing customer', 'Customer was not found')
    cancel_customer_edit()
    refresh_customers()

cust_add_but = tk.Button(cust_table_section_but, text='Add', height=1, width=6, command=cust_show_add)
cust_add_but.pack(side='left', padx=4, pady=4)
cust_edit_but = tk.Button(cust_table_section_but, text='Edit', height=1, width=6, command=cust_show_edit)
cust_edit_but.pack(side='right', padx=4, pady=4)
cust_delete_but = tk.Button(cust_table_section_but, text='Delete', height=1, width=7, command=remove_customer)
cust_delete_but.pack(side='right', padx=4, pady=4)

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

#Add Insert
cust_entry_row = tk.Frame(cust_table_frame)
cust_entry_row.pack_forget()

# Customer table uses real database IDs so later edit/delete can target records
def refresh_customers():
    """Load customers from Supabase into the customer table"""
    try:
        term = cust_main_search.get().strip()
        customers = search_customers(term) if term else get_all_customers()
    except Exception as exc:
        messagebox.showerror("Database error", f"Could not load customers:\n{exc}")
        return

    cust_table.delete(*cust_table.get_children())
    for customer in customers:
        cust_table.insert(
            "", "end", iid=str(customer["customer_id"]),
            values=(
                customer.get("first_name") or "",
                customer.get("last_name") or "",
                customer.get("address") or "",
                customer.get("phone") or "",
                customer.get("email") or ""
            )
        )


# Labeled customer inputs
def customer_field(label):
    field_frame = tk.Frame(cust_entry_row)
    field_frame.pack(side='left', padx=2, fill='x', expand=True)
    tk.Label(field_frame, text=label, anchor='w').pack(fill='x')
    entry = tk.Entry(field_frame, bd=2, width=12)
    entry.pack(fill='x')
    return entry


first_entry = customer_field("First name")
last_entry = customer_field("Last name")
address_entry = customer_field("Address")
phone_entry = customer_field("Phone")
email_entry = customer_field("Email")
customer_fields = (first_entry, last_entry, address_entry, phone_entry, email_entry)
customer_field_keys = ('first_name', 'last_name', 'address', 'phone', 'email')

def clear_customer_fields():
    for field in customer_fields:
        field.delete(0, tk.END)

def cancel_customer_edit():
    global editing_customer_id
    editing_customer_id = None
    clear_customer_fields()
    cust_entry_row.pack_forget()
    cust_add_submit.config(text='Save')


def cust_add_save():
    """Save a new or edited customer and refresh the table"""
    payload = {
        'first_name': first_entry.get(),
        'last_name': last_entry.get(),
        'address': address_entry.get(),
        'phone': phone_entry.get(),
        'email': email_entry.get()
    }
    try:
        if editing_customer_id is None:
            saved = create_customer(**payload)
        else:
            saved = update_customer(editing_customer_id, payload)
    except ValueError as exc:
        messagebox.showerror('Invalid customer', str(exc))
        return
    except Exception as exc:
        messagebox.showerror('Database error', f'Could not save customer:\n{exc}')
        return

    if saved is None:
        messagebox.showwarning('Missing customer', 'This customer no longer exists')
        return
    was_editing = editing_customer_id is not None
    cancel_customer_edit()
    refresh_customers()
    messagebox.showinfo('Customer updated' if was_editing else 'Customer added',
                        f'Saved {saved["first_name"]} {saved.get("last_name") or ""}')


cust_add_submit = tk.Button(cust_entry_row, bd=4, text='Save', command=cust_add_save)
cust_add_submit.pack(side='left', padx=2, pady=(18, 0))
tk.Button(cust_entry_row, text='Cancel', command=cancel_customer_edit).pack(side='left', padx=2, pady=(18, 0))

customer_search_job = None

def schedule_customer_search(_event=None):
    global customer_search_job
    if customer_search_job is not None:
        root.after_cancel(customer_search_job)
    customer_search_job = root.after(300, refresh_customers)

cust_main_search.bind('<KeyRelease>', schedule_customer_search)


inventory_page.tkraise()







#Return Page
return_page_main = tk.Frame(return_page, bg='grey')
return_page_main.pack(fill='both', expand=True)
return_page_main.propagate(False)

#Return top frame
return_top = tk.Frame(return_page_main, height=50, bg='grey')
return_top.pack(fill='x')
return_page_main.propagate(False)

home_button = tk.Button(return_top, text = 'Home', command=inv_page)
home_button.pack(fill='x', side='left', padx=5, pady=5)



# Return active rentals using their rental ID
return_controls = tk.Frame(return_page_main, bg='grey')
return_controls.pack(fill='x', padx=10, pady=8)
tk.Label(return_controls, text='Active rentals', bg='grey', font=('Arial', 14, 'bold')).pack(side='left')

return_columns = ('Rental ID', 'Customer', 'Movie', 'Rented At')
return_table = ttk.Treeview(return_page_main, columns=return_columns, show='headings', selectmode='browse')
for column in return_columns:
    return_table.heading(column, text=column)
return_table.pack(fill='both', expand=True, padx=10, pady=5)


def refresh_returns():
    """Load active rentals with customer and movie names"""
    try:
        rentals = get_active_rentals()
        customers = {c['customer_id']: c for c in get_all_customers()}
        videos = {v['video_id']: v for v in get_all_videos()}
    except Exception as exc:
        messagebox.showerror('Database error', f'Could not load rentals:\n{exc}')
        return
    return_table.delete(*return_table.get_children())
    for rental in rentals:
        customer = customers.get(rental['customer_id'], {})
        movie = videos.get(rental['video_id'], {})
        customer_name = f"{customer.get('first_name', 'Unknown')} {customer.get('last_name') or ''}".strip()
        return_table.insert('', 'end', iid=str(rental['rental_id']), values=(
            rental['rental_id'], customer_name, movie.get('title', 'Unknown'),
            str(rental.get('rented_at') or '')[:19]
        ))


def return_selected():
    """Return the selected rental and refresh inventory"""
    selection = return_table.selection()
    if not selection:
        messagebox.showwarning('Select a rental', 'Choose a rental from the table first')
        return
    rental_id = int(selection[0])
    try:
        result = return_rental(rental_id)
    except Exception as exc:
        messagebox.showerror('Database error', f'Could not return rental:\n{exc}')
        return
    if result is None:
        messagebox.showwarning('Already returned', 'This rental is no longer active')
    else:
        messagebox.showinfo('Returned', f'Rental #{rental_id} was returned')
    refresh_returns()
    refresh_inventory()


tk.Button(return_controls, text='Return selected rental', command=return_selected).pack(side='right', padx=5)
tk.Button(return_controls, text='Refresh', command=refresh_returns).pack(side='right', padx=5)


#Place all the pages
inventory_page.place(x=0, y=0, relwidth=1, relheight=1)
customer_page.place(x=0, y=0, relwidth=1, relheight=1)
return_page.place(x=0, y=0, relwidth=1, relheight=1)
customer_hist.place(x=0, y=0, relwidth=1, relheight=1)
rental_page.place(x=0, y=0, relwidth=1, relheight=1)


refresh_inventory()
refresh_customers()
inv_page()


def run():
    """Start the application window"""
    root.mainloop()


if __name__ == "__main__":
    run()