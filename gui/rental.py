import tkinter as tk
from tkinter import ttk, messagebox

from database.customers import get_all_customers
from database.videos import get_all_videos, available_quantity
from database.rentals import create_rental


class RentalFrame(tk.Frame):
    HEADER = "#ebebeb"
    BACKGROUND = "#dddddd"
    PANEL = "#bfbfbf"
    TABLE = "#eeeeee"

    def __init__(
        self,
        parent,
        show_header=True,
        on_home=None,
        on_rent=None,
        on_history=None,
        on_return=None,
    ):
        super().__init__(parent, bg=self.BACKGROUND)

        self.on_home = on_home
        self.on_rent = on_rent
        self.on_history = on_history
        self.on_return = on_return

        self.columnconfigure(0, weight=1, uniform="panels")
        self.columnconfigure(1, weight=1, uniform="panels")
        self.rowconfigure(2, weight=1)

        self.configure_styles()

        if show_header:
            self.create_header()

        # Page title
        tk.Label(
            self,
            text="Rent Movies",
            bg=self.BACKGROUND,
            font=("Arial", 20, "bold"),
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(20, 15),
        )

        # Customers panel
        customer_panel = tk.LabelFrame(
            self,
            text="",
            bg=self.PANEL,
            padx=12,
            pady=12,
        )
        customer_panel.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=(0, 15),
        )

        tk.Label(
            customer_panel,
            text="Search customers",
            bg=self.PANEL,
            font=("Arial", 11),
        ).pack(anchor="w")

        self.customer_search = tk.StringVar(master=self)

        self.customer_search_entry = tk.Entry(
            customer_panel,
            textvariable=self.customer_search,
            bg="white",
            fg="black",
            insertbackground="black",
            font=("Arial", 12),
        )
        self.customer_search_entry.pack(
            fill="x",
            pady=(5, 12),
        )

        self.customer_table = self.create_table(
            customer_panel,
            columns=(
                ("name", "Customer", 220),
                ("customer_id", "Customer ID", 100),
            ),
            selectmode="browse",
        )

        # Movies panel
        movie_panel = tk.LabelFrame(
            self,
            text="",
            bg=self.PANEL,
            padx=12,
            pady=12,
        )
        movie_panel.grid(
            row=2,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=(0, 15),
        )

        tk.Label(
            movie_panel,
            text="Search movies",
            bg=self.PANEL,
            font=("Arial", 11),
        ).pack(anchor="w")

        self.movie_search = tk.StringVar(master=self)

        self.movie_search_entry = tk.Entry(
            movie_panel,
            textvariable=self.movie_search,
            bg="white",
            fg="black",
            insertbackground="black",
            font=("Arial", 12),
        )
        self.movie_search_entry.pack(
            fill="x",
            pady=(5, 12),
        )

        self.movie_table = self.create_table(
            movie_panel,
            columns=(
                ("title", "Movie", 220),
                ("video_id", "Movie ID", 100),
            ),
            selectmode="browse",
        )

        # Bottom section
        bottom = tk.Frame(
            self,
            bg=self.BACKGROUND,
        )
        bottom.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(0, 20),
        )
        bottom.columnconfigure(0, weight=1)

        self.status = tk.StringVar(
            master=self,
            value="",
        )

        tk.Label(
            bottom,
            textvariable=self.status,
            bg=self.BACKGROUND,
            fg="#444444",
            font=("Arial", 10),
            wraplength=500,
            justify="left",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.rent_button = ttk.Button(
            bottom,
            text="Rent",
            command=self.rent_selected,
            state="disabled",
        )
        self.rent_button.grid(
            row=0,
            column=1,
            padx=(15, 0),
        )
        self.customer_table.bind("<<TreeviewSelect>>", self.update_selection)
        self.movie_table.bind("<<TreeviewSelect>>", self.update_selection)
        self.customer_search.trace_add("write", lambda *_: self.filter_tables())
        self.movie_search.trace_add("write", lambda *_: self.filter_tables())
        self.customers = []
        self.movies = []

    def refresh_data(self):
        """Load customers and videos for the rental screen"""
        try:
            self.customers = get_all_customers()
            self.movies = get_all_videos()
            self.filter_tables()
            self.status.set("Choose a customer and an available movie")
        except Exception as exc:
            self.status.set("Could not load rental information")
            messagebox.showerror("Database error", str(exc), parent=self)

    def filter_tables(self):
        """Filter customer and movie lists locally"""
        customer_query = self.customer_search.get().strip().lower()
        movie_query = self.movie_search.get().strip().lower()
        self.customer_table.delete(*self.customer_table.get_children())
        self.movie_table.delete(*self.movie_table.get_children())
        for person in self.customers:
            name = f"{person.get('first_name') or ''} {person.get('last_name') or ''}".strip()
            if customer_query in f"{name} {person['customer_id']}".lower():
                self.customer_table.insert("", "end", iid=str(person["customer_id"]), values=(name, person["customer_id"]))
        for movie in self.movies:
            title = movie.get("title") or ""
            if movie_query in f"{title} {movie['video_id']}".lower():
                self.movie_table.insert("", "end", iid=str(movie["video_id"]), values=(title, movie["video_id"]))
        self.update_selection()

    def update_selection(self, event=None):
        """Enable Rent after selecting a customer and movie"""
        ready = bool(self.customer_table.selection() and self.movie_table.selection())
        self.rent_button.configure(state="normal" if ready else "disabled")

    def rent_selected(self):
        """Create a rental for the selected customer and movie"""
        if not self.customer_table.selection() or not self.movie_table.selection():
            return
        customer_id = int(self.customer_table.selection()[0])
        video_id = int(self.movie_table.selection()[0])
        try:
            available = available_quantity(video_id)
            if available <= 0:
                raise ValueError("No copies available for rental")
            rental = create_rental(customer_id, video_id)
        except ValueError as exc:
            messagebox.showerror("Cannot rent movie", str(exc), parent=self)
            return
        except Exception as exc:
            messagebox.showerror("Database error", str(exc), parent=self)
            return
        self.status.set(f"Rental #{rental['rental_id']} created successfully")
        messagebox.showinfo("Rental created", f"Rental ID: {rental['rental_id']}", parent=self)
        self.refresh_data()

    def create_header(self):
        header = tk.Frame(
            self,
            height=50,
            bg=self.HEADER,
            bd=2,
            relief="solid",
        )
        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
        )
        header.pack_propagate(False)

        # Click the store name to return home.
        name = tk.Label(
            header,
            text="Video Store",
            bg=self.HEADER,
            fg="black",
            cursor="hand2",
        )
        name.pack(side="left", padx=10)

        if self.on_home is not None:
            name.bind(
                "<Button-1>",
                lambda event: self.on_home(),
            )

        # Navigation buttons on the right.
        navigation = tk.Frame(
            header,
            bg=self.HEADER,
        )
        navigation.pack(side="right", padx=10)

        for text, callback in (
            ("Rent", self.on_rent),
            ("Customer History", self.on_history),
            ("Return", self.on_return),
        ):
            tk.Button(
                navigation,
                text=text,
                command=callback,
                state=(
                    "normal"
                    if callback is not None
                    else "disabled"
                ),
            ).pack(
                side="left",
                padx=1,
            )

        # Search bar between the title and navigation.
        self.header_search = tk.StringVar(master=self)

        self.main_search = tk.Entry(
            header,
            textvariable=self.header_search,
            bg="white",
            fg="black",
            insertbackground="black",
        )
        self.main_search.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
        )

    def configure_styles(self):
        style = ttk.Style(self)

        style.configure(
            "Rental.Treeview",
            background=self.TABLE,
            fieldbackground=self.TABLE,
            foreground="black",
            rowheight=30,
            font=("Arial", 11),
        )

        style.configure(
            "Rental.Treeview.Heading",
            background="#666666",
            foreground="white",
            font=("Arial", 11, "bold"),
        )

        style.map(
            "Rental.Treeview",
            background=[("selected", "#555555")],
            foreground=[("selected", "white")],
        )

    def create_table(self, parent, columns, selectmode):
        table = ttk.Treeview(
            parent,
            columns=[column[0] for column in columns],
            show="headings",
            selectmode=selectmode,
            style="Rental.Treeview",
            height=10,
        )

        for column_id, heading, width in columns:
            table.heading(
                column_id,
                text=heading,
            )
            table.column(
                column_id,
                width=width,
                minwidth=60,
                stretch=True,
                anchor="w",
            )

        table.pack(
            fill="both",
            expand=True,
        )

        table.tag_configure(
            "even",
            background="#eeeeee",
        )
        table.tag_configure(
            "odd",
            background="#d5d5d5",
        )

        return table


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Store Inventory — Rentals")
    root.geometry("900x600")
    root.minsize(850, 550)

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    screen = RentalFrame(root)
    screen.pack(
        fill="both",
        expand=True,
    )

    root.mainloop()