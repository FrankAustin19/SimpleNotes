import tkinter as tk
from tkinter import ttk
from note import Note
from data_manager import *
from datetime import datetime
import json
import os


class NoteApp:
    SETTINGS_FILE = 'data/settings.json'
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notes")
        self.root.geometry("900x100")
        self.labels = load_labels()
        self.characters = ['PP', 'Kevin', 'Mitch', 'Alex', 'Steven R', 'Steven A', 'Party', 'DM'] #write function to set these
        self.current_order = 0

        self.load_settings()

        # Setup the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="View All Notes", command=self.open_note_display)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.setup_ui()

    def load_settings(self):
        #Load settings file to get current_order
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)

            
            self.current_order = settings.get('current_order', 0)  
        else:
            self.current_order = 0  

    def open_note_display(self):
        # Open Note Display Window
        notes = load_notes()  
        display_window = tk.Toplevel(self.root)
        display_window.title("All Notes")
        NoteDisplay(display_window, notes)  


    def setup_ui(self):
        """Method to set up the initial UI elements."""
        # Frame
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Content text box
        self.note_label = ttk.Label(self.frame, text="Note:")
        self.note_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))        
        self.note_text = tk.Text(self.frame, height=1, width=90)
        self.note_text.grid(row=0, column=1, columnspan=6, sticky=tk.W, padx=(0, 10))  

        # "Label" label
        self.label_label = ttk.Label(self.frame, text="Label:")
        self.label_label.grid(row=1, column=0, sticky=tk.W)

        # Combobox for labels
        self.label_combobox = ttk.Combobox(self.frame, values=self.labels, state='normal', width=20)
        self.label_combobox.grid(row=1, column=1, sticky=tk.W, padx=(0, 5)) 
        self.label_combobox.set("")
        self.label_combobox.bind("<Return>", self.save_label)

        # Checkboxes
        self.character_vars = {}
        self.character_frame = ttk.Frame(self.frame)
        self.character_frame.grid(row=1, column=2, sticky=tk.W, padx=(0, 10), columnspan=5)  
        for i, character in enumerate(self.characters):
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.character_frame, text=character, variable=var)
            checkbox.grid(row=0, column=i, sticky=tk.W, padx=5)  
            self.character_vars[character] = var

        # Save button
        self.save_button = ttk.Button(self.frame, text="Save", command=self.save_note)  
        self.save_button.grid(row=1, column=8, sticky=tk.W)  

    # Function for saving notes
    def save_note(self):
        # Define dictionary variables
        content = self.note_text.get("1.0", tk.END).strip()
        label =self.label_combobox.get()
        characters = [character for character, var in self.character_vars.items() if var.get()]
        date = datetime.today().date()

        #Load existing notes file and increment note order
        notes = load_notes()
        self.current_order += 1

        # Create new note
        note = Note(content=content, label=label, character = characters, date=date, order=self.current_order)

        #Save new note, new label, and current order
        save_to_file(note)
        self.save_label()
        self.save_current_order()

        # Clear fields
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
    
    def save_current_order(self):                 #Function for keeping track of note serial numbers
        with open(self.SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
            settings['current_order'] = self.current_order
        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file, indent=4)


class NoteDisplay:
    SETTINGS_FILE = 'data/settings.json'

    def __init__(self, root, notes):
        self.root = root
        self.notes = notes 
        self.load_settings()
        self.setup_ui()
        self.sort_reverse = {col: False for col in self.tree["columns"]}
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_note_display(self):
        # Method to open Note Display
        notes = load_notes() 
        display_window = tk.Toplevel(self.root)
        display_window.title("All Notes")
        NoteDisplay(display_window, notes)

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
        # Insert notes into table
        notes = load_notes()  
        for note in notes:
            self.tree.insert('', tk.END, values=(
                note.get('content'),
                note.get('label'),
                ', '.join(note.get('character', [])),  
                note.get('date'),
                note.get('order')
            ))
        for col in self.tree["columns"]:
            self.tree.heading(col, command=lambda _col=col: self.sort_notes(_col))
            


    def on_close(self):
        # Get window geometry (size and position)
        window_geometry = self.root.geometry() 

        # Get column widths
        column_widths = {col: self.tree.column(col, width=None) for col in self.tree["columns"]}

        # Save the settings
        settings = {
            'geometry': window_geometry,
            'column_widths': column_widths,
            'current_order': self.current_order
        }

        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)

        # Close the window
        self.root.destroy()

    def load_settings(self):
        # Load geometry and order settings
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)

            # Apply window geometry (size and position)
            self.root.geometry(settings.get('geometry', '800x600'))

            self.current_order = settings.get('current_order', 0) 
        
        else:
            self.current_order = 0

    def load_column_widths(self):
        # Load column widths for display window preferences
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)

            column_widths = settings.get('column_widths', {})
            for col, width in column_widths.items():
                if width:
                    self.tree.column(col, width=width)
    
    def save_current_order(self):
        # Save the note serial number
        with open(self.SETTINGS_FILE, 'r') as file:
            settings = json.load(file)

            # Update the current order in the settings
            settings['current_order'] = self.current_order

        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file, indent=4)

    def sort_notes(self, col):
        # Determine the current sort order
        reverse = self.sort_reverse[col]
        notes = load_notes()
        # Sort notes based on the selected column
        notes.sort(key=lambda x: x[col], reverse=reverse)

        # Clear the current items in the tree
        self.tree.delete(*self.tree.get_children())

        # Reinsert sorted notes
        for note in notes:
            self.tree.insert('', tk.END, values=(
                note.get('content'),
                note.get('label'),
                ', '.join(note.get('character', [])),  # Join list for display
                note.get('date'),
                note.get('order')
            ))

        # Toggle the sort direction for the next click
        self.sort_reverse[col] = not self.sort_reverse[col]


if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
