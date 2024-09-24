from datetime import datetime

class Note:
    def __init__(self, content, label=None, character=None, date=None, order=None):
        """Initialize a new Note object."""
        self.content = content
        self.label = label
        self.character = character
        self.date = date if date else datetime.today().date()
        self.order = order  

    def to_dict(self):
        """Convert the note object to a dictionary for easy storage."""
        return {
            'content': self.content,
            'label': self.label,
            'character': self.character,
            'date': self.date.isoformat(),
            'order': self.order  
        }

    @classmethod
    def from_dict(cls, note_dict):
        """Create a Note object from a dictionary."""
        date_str = note_dict.get('date')
        date = datetime.fromisoformat(date_str).date() if date_str else datetime.today().date()
        return cls(
            content=note_dict['content'],
            label=note_dict.get('label'),
            character=note_dict.get('character'),
            date=date,
            order=note_dict.get('order')
        )

    def __str__(self):
        return f"Note: {self.content} Label: {self.label} Character: {self.character} Date: {self.date}"

