import json
from note import Note
import os

# Function for saving note as JSON
def save_to_file(note, filename="data/notes.json"):
    note_dict = note.to_dict()

    try:
        
        with open(filename, 'r') as file:
            # Check if the file is empty
            if file.readable() and file.read().strip() == "":
                notes = []
            else:
                file.seek(0)  # Move the cursor back to the beginning of the file
                notes = json.load(file)
        
    except FileNotFoundError:
        notes = []  # If the file doesn't exist, start with an empty list
    except json.JSONDecodeError:
        notes = []  # If there's a JSON error, start with an empty list

    notes.append(note_dict)

    with open(filename, 'w') as file:
        json.dump(notes, file, indent=4)


#Function handling saving new labels
def save_labels(labels, filename="data/labels.json"):
    """Save the labels to a JSON file."""
    with open(filename, 'w') as file:  # Open in write mode
        json.dump(labels, file, indent=4)

    
#Function handling loading label list

def load_labels(filename="data/labels.json"):
    """Load labels from a JSON file."""
    try:
        with open(filename, 'r') as file:
            content = file.read().strip()
            if content:  # Check if the content is not empty
                return json.loads(content)
            return []  # Return an empty list if the file is empty
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        print("Error: Labels file is not valid JSON. Returning empty labels list.")
        return []  # Return an empty list if the JSON is invalid
    
def load_notes():
    file_path = 'data/notes.json'  # Update with your actual file path
    if not os.path.exists(file_path):
        return []  # Return an empty list if the file doesn't exist

    with open(file_path, 'r') as file:
        content = file.read().strip()  # Read and strip whitespace
        if not content:  # Check if content is empty
            return []  # Return an empty list if the file is empty
        return json.loads(content)  # Load the JSON data

