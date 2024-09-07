import sqlite3
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import pyperclip

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
        file_menu.add_command(label="Export to Excel", command=self.export_to_excel)

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

        self.results_tree = ttk.Treeview(self.right_frame, style="Custom.Treeview", columns=[])
        self.results_tree.pack(pady=20, fill=BOTH, expand=True)

        # Style configuration for Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 10))

        # Bind right-click menu
        self.results_tree.bind("<Button-3>", self.show_popup_menu)

        # Popup menu
        self.popup_menu = Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Copy", command=self.copy_selection)

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

    def show_popup_menu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def copy_selection(self):
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No rows selected")
            return

        rows = []
        for item in selected_items:
            row_values = self.results_tree.item(item, "values")
            rows.append("\t".join(map(str, row_values)))

        text = "\n".join(rows)
        pyperclip.copy(text)  # Copy the text to the clipboard
        messagebox.showinfo("Info", "Copied to clipboard")

    def export_to_excel(self):
        if self.results_tree["columns"]:
            # Prepare data for export
            columns = self.results_tree["columns"]
            rows = [self.results_tree.item(item, "values") for item in self.results_tree.get_children()]

            # Create a DataFrame and export to Excel
            df = pd.DataFrame(rows, columns=columns)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                title="Save Excel File"
            )
            
            if file_path:
                try:
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Success", f"Data exported to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export data: {e}")
                    print(f"Failed to export data: {e}")  # Debug: Print export error
        else:
            messagebox.showinfo("Info", "No data available to export")

if __name__ == "__main__":
    root = Tk()
    app = SQLiteBrowser(root)
    root.mainloop()

