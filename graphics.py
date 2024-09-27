import tkinter as tk
from tkinter import ttk
from note import Note
from data_manager import *
from datetime import datetime
import json
import os



class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notes")
        self.root.geometry("900x100")
        self.labels = load_labels()
        self.characters = ['PP', 'Kevin', 'Mitch', 'Alex', 'Steven R', 'Steven A', 'Party', 'DM']

        # Setup the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="View All Notes", command=self.open_note_display)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.setup_ui()

    def open_note_display(self):
        """Method to open a new window displaying all notes."""
        notes = load_notes()  
        display_window = tk.Toplevel(self.root)
        display_window.title("All Notes")
        NoteDisplay(display_window, notes)  # Pass the notes to the display class


    def setup_ui(self):
        """Method to set up the initial UI elements."""
        # Creating a frame for layout
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add a text box for entering notes
        self.note_label = ttk.Label(self.frame, text="Note:")
        self.note_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.note_text = tk.Text(self.frame, height=1, width=90)
        self.note_text.grid(row=0, column=1, columnspan=6, sticky=tk.W, padx=(0, 10))  

        # Add a label dropdown menu
        self.label_label = ttk.Label(self.frame, text="Label:")
        self.label_label.grid(row=1, column=0, sticky=tk.W)

        self.label_combobox = ttk.Combobox(self.frame, values=self.labels, state='normal', width=20)
        self.label_combobox.grid(row=1, column=1, sticky=tk.W, padx=(0, 5)) 
        self.label_combobox.set("")
        self.label_combobox.bind("<Return>", self.save_label)

        # Add checkboxes for characters
        self.character_vars = {}
        self.character_frame = ttk.Frame(self.frame)
        self.character_frame.grid(row=1, column=2, sticky=tk.W, padx=(0, 10), columnspan=5)  

        for i, character in enumerate(self.characters):
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.character_frame, text=character, variable=var)
            checkbox.grid(row=0, column=i, sticky=tk.W, padx=5)  
            self.character_vars[character] = var

        # Add a button to save the note
        self.save_button = ttk.Button(self.frame, text="Save", command=self.save_note)  
        self.save_button.grid(row=1, column=8, sticky=tk.W)  

    # Function for saving notes
    def save_note(self):
        content = self.note_text.get("1.0", tk.END).strip()
        label =self.label_combobox.get()
        characters = [character for character, var in self.character_vars.items() if var.get()]
        date = datetime.today().date()

        note = Note(content=content, label=label, character = characters, date=date)

        save_to_file(note)
        self.save_label()

        self.note_text.delete("1.0", tk.END)
        self.label_combobox.set("")
        for var in self.character_vars.values():
            var.set(False)

        

    # Function for saving labels
    def save_label(self):
        new_label = self.label_combobox.get().strip()

        if new_label and new_label not in self.labels:
            self.labels.append(new_label)
            self.label_combobox['values'] = self.labels
            self.label_combobox.set("")
            save_labels(self.labels)

        elif new_label in self.labels:
            pass

class NoteDisplay:
    SETTINGS_FILE = 'data/settings.json'

    def __init__(self, root, notes):
        self.root = root
        self.notes = notes 
        self.load_settings()
        self.setup_ui()

        # Bind the close event to save settings before exiting
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_note_display(self):
        """Method to open a new window displaying all notes."""
        notes = load_notes() 
        display_window = tk.Toplevel(self.root)
        display_window.title("All Notes")
        NoteDisplay(display_window, notes)  # Pass the notes to the display class

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
        notes = load_notes()  # Load notes before populating
        for note in notes:
            self.tree.insert('', tk.END, values=(
                note.get('content'),
                note.get('label'),
                ', '.join(note.get('character', [])),  # Join list for display
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
    app = NoteApp(root)
    root.mainloop()
