import tkinter as tk
from tkinter import ttk
import json
import os

class NoteDisplay:
    SETTINGS_FILE = 'settings.json'

    def __init__(self, root, notes):
        self.root = root
        self.notes = notes  # Notes should be passed as a list of dictionaries

        # Load previous settings if available
        self.load_settings()

        # Set up the UI
        self.setup_ui()

        # Bind the close event to save settings before exiting
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # Create a frame for the Treeview
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid to allow stretching
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create the Treeview widget
        self.tree = ttk.Treeview(self.frame, columns=('content', 'label', 'character', 'date', 'order'), show='headings')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Define headings for the table
        self.tree.heading('content', text='Content')
        self.tree.heading('label', text='Label')
        self.tree.heading('character', text='Character')
        self.tree.heading('date', text='Date')
        self.tree.heading('order', text='Order')

        # Set the column to expand and stretch to fill available space
        self.tree.column('content', width=200, stretch=tk.YES)
        self.tree.column('label', width=100, stretch=tk.YES)
        self.tree.column('character', width=100, stretch=tk.YES)
        self.tree.column('date', width=100, stretch=tk.YES)
        self.tree.column('order', width=100, stretch=tk.YES)

        # Load saved column widths, if available
        self.load_column_widths()

        # Insert notes into the Treeview table
        self.populate_table()

        # Add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def populate_table(self):
        """Insert the notes into the table"""
        for note in self.notes:
            self.tree.insert('', tk.END, values=(
                note.get('content'),
                note.get('label'),
                note.get('character'),
                note.get('date'),
                note.get('order')
            ))

    def on_close(self):
        """Save window and column settings when the window is closed."""
        # Get window geometry (size and position)
        window_geometry = self.root.geometry()  # Format is "widthxheight+x+y"

        # Get column widths
        column_widths = {col: self.tree.column(col, width=None) for col in self.tree["columns"]}

        # Save the settings
        settings = {
            'geometry': window_geometry,
            'column_widths': column_widths
        }

        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)

        # Close the window
        self.root.destroy()

    def load_settings(self):
        """Load window geometry and column widths from a file."""
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)

            # Apply window geometry (size and position)
            self.root.geometry(settings.get('geometry', '800x600'))

    def load_column_widths(self):
        """Load column widths from the saved settings."""
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)

            column_widths = settings.get('column_widths', {})
            for col, width in column_widths.items():
                if width:
                    self.tree.column(col, width=width)


if __name__ == "__main__":
    root = tk.Tk()

    # Example notes (replace this with your actual notes data)
    notes = [
        {'content': 'First note', 'label': 'Important', 'character': 'Alex', 'date': '2024-09-25', 'order': 1},
        {'content': 'Second note', 'label': 'Casual', 'character': 'Kevin', 'date': '2024-09-26', 'order': 2},
        {'content': 'Third note', 'label': 'Work', 'character': 'PP', 'date': '2024-09-27', 'order': 3},
    ]

    app = NoteDisplay(root, notes)
    root.mainloop()
