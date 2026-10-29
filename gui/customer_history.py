import tkinter as tk
from tkinter import ttk


class CustomerHistoryFrame(tk.Frame):
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

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        self.customer_id = tk.StringVar(
            master=self,
            value="Customer ID: —",
        )
        self.customer_name = tk.StringVar(
            master=self,
            value="Name: —",
        )

        self.configure_styles()

        if show_header:
            self.create_header()

        # Page title
        tk.Label(
            self,
            text="Customer History and Rentals",
            bg=self.BACKGROUND,
            font=("Arial", 20, "bold"),
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 15),
        )

        # Customer information
        customer_panel = tk.Frame(
            self,
            bg=self.PANEL,
        )
        customer_panel.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15),
        )

        tk.Label(
            customer_panel,
            textvariable=self.customer_id,
            bg=self.PANEL,
            font=("Arial", 12),
        ).pack(
            side="left",
            padx=15,
            pady=12,
        )

        tk.Label(
            customer_panel,
            textvariable=self.customer_name,
            bg=self.PANEL,
            font=("Arial", 12),
        ).pack(
            side="left",
            padx=25,
            pady=12,
        )

        # Current rentals panel
        current_panel = tk.LabelFrame(
            self,
            text="Current Rentals",
            bg=self.PANEL,
            font=("Arial", 14, "bold"),
            padx=12,
            pady=12,
        )
        current_panel.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 15),
        )

        movie_columns = (
            ("title", "Name", 180),
            ("year", "Year", 65),
            ("director", "Director", 140),
            ("rating", "Rating", 70),
            ("genre", "Genre", 100),
            ("video_id", "Movie ID", 85),
        )

        self.current_table = self.create_table(
            current_panel,
            movie_columns,
        )

        # Rental history panel
        history_panel = tk.LabelFrame(
            self,
            text="Rental History",
            bg=self.PANEL,
            font=("Arial", 14, "bold"),
            padx=12,
            pady=12,
        )
        history_panel.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 15),
        )

        history_columns = movie_columns + (
            ("date_rented", "Date Rented", 110),
            ("date_returned", "Date Returned", 110),
        )

        self.history_table = self.create_table(
            history_panel,
            history_columns,
        )

        self.status = tk.StringVar(
            master=self,
            value="",
        )

        tk.Label(
            self,
            textvariable=self.status,
            bg=self.BACKGROUND,
            fg="#444444",
            font=("Arial", 10),
            wraplength=700,
            justify="left",
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 15),
        )

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
            "History.Treeview",
            background=self.TABLE,
            fieldbackground=self.TABLE,
            foreground="black",
            rowheight=30,
            font=("Arial", 11),
        )

        style.configure(
            "History.Treeview.Heading",
            background="#666666",
            foreground="white",
            font=("Arial", 11, "bold"),
        )

        style.map(
            "History.Treeview",
            background=[("selected", "#555555")],
            foreground=[("selected", "white")],
        )

    def create_table(self, parent, columns):
        table = ttk.Treeview(
            parent,
            columns=[column[0] for column in columns],
            show="headings",
            selectmode="browse",
            style="History.Treeview",
            height=5,
        )

        for column_id, heading, width in columns:
            table.heading(
                column_id,
                text=heading,
            )
            table.column(
                column_id,
                width=width,
                minwidth=55,
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
    root.title("Video Store Inventory — Customer History")
    root.geometry("900x600")
    root.minsize(850, 550)

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    screen = CustomerHistoryFrame(root)
    screen.pack(
        fill="both",
        expand=True,
    )

    root.mainloop()