import sqlite3
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk

class SQLiteBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Browser")
        self.root.geometry("1000x600")

        # Create a frame for the left panel
        self.left_frame = Frame(root)
        self.left_frame.pack(side=LEFT, fill=Y, padx=10, pady=10, expand=False)

        # Create a frame for the right panel
        self.right_frame = Frame(root)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Setup menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Database", command=self.open_database)

        # Left panel: Listbox for tables
        self.table_listbox = Listbox(self.left_frame, width=40)
        self.table_listbox.pack(side=LEFT, fill=Y, expand=False)

        # Add a scrollbar to the listbox
        self.scrollbar = Scrollbar(self.left_frame, orient=VERTICAL, command=self.table_listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.table_listbox.config(yscrollcommand=self.scrollbar.set)

        # Bind selection event to update table view
        self.table_listbox.bind('<<ListboxSelect>>', self.on_table_select)

        # Right panel: Query entry and results
        self.query_entry = Entry(self.right_frame, width=80)
        self.query_entry.pack(pady=5, fill=X)

        run_button = Button(self.right_frame, text="Run Query", command=self.run_query)
        run_button.pack(pady=5)

        self.results_tree = ttk.Treeview(self.right_frame, style="Custom.Treeview")
        self.results_tree.pack(pady=20, fill=BOTH, expand=True)

        # Style configuration for Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 10))

        self.db_connection = None

    def open_database(self):
        # Open file dialog to select SQLite database
        db_path = filedialog.askopenfilename(
            title="Open SQLite Database",
            filetypes=[("SQLite Database Files", "*.sqlite *.db *.sqlite3")]
        )

        if db_path:
            try:
                self.db_connection = sqlite3.connect(db_path)
                self.db_label = Label(self.right_frame, text=f"Loaded: {db_path}")
                self.db_label.pack(pady=10)
                self.populate_table_list()
                print(f"Database loaded: {db_path}")  # Debug: Confirm database load
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to open database: {e}")
                print(f"Failed to open database: {e}")  # Debug: Print error

    def populate_table_list(self):
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.table_listbox.delete(0, END)  # Clear current list
            for table in tables:
                self.table_listbox.insert(END, table[0])

    def on_table_select(self, event):
        selected_table = self.table_listbox.get(ACTIVE)
        if selected_table:
            self.query_entry.delete(0, END)
            self.query_entry.insert(0, f"SELECT * FROM {selected_table}")
            self.run_query()

    def run_query(self):
        query = self.query_entry.get()
        if self.db_connection and query:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                self.results_tree.delete(*self.results_tree.get_children())

                if columns:
                    self.results_tree["columns"] = columns
                    for col in columns:
                        self.results_tree.heading(col, text=col)
                        self.results_tree.column(col, width=150, anchor='w')  # Adjust width and alignment
                    for row in results:
                        self.results_tree.insert("", "end", values=row)
                else:
                    messagebox.showinfo("Info", "Query executed successfully but returned no results.")
                    print("Query executed successfully but returned no results.")  # Debug: Query executed but no results

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Query failed: {e}")
                print(f"Query failed: {e}")  # Debug: Print query error
        else:
            messagebox.showerror("Error", "No database loaded or query is empty")
            print("No database loaded or query is empty")  # Debug: No database or query is empty

if __name__ == "__main__":
    root = Tk()
    app = SQLiteBrowser(root)
    root.mainloop()

