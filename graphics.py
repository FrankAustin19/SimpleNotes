import tkinter as tk
from tkinter import ttk
from note import Note
from data_manager import *
from datetime import datetime

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notes")
        self.root.geometry("900x100")  # Adjusted size for two rows only
        self.labels = load_labels()
        self.characters = ['PP', 'Kevin', 'Mitch', 'Alex', 'Steven R', 'Steven A', 'Party', 'DM']
        
        # Call method to set up the GUI elements
        self.setup_ui()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
