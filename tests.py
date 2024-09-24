import unittest
import os
import json
from note import Note  # Adjust the path as needed
from data_manager import save_to_file  # Adjust the path as needed

class TestDataManager(unittest.TestCase):

    def setUp(self):
        """Set up for each test case."""
        self.test_note = Note(content="Test note", label="Test label", character="Test character", date=None)
        self.test_filename = "data/test_notes.json"

    def tearDown(self):
        """Clean up after each test case."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_save_note_creates_file(self):
        """Test that saving a note creates a file."""
        save_to_file(self.test_note, self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))

    def test_save_note_content(self):
        """Test that the saved note content is correct."""
        save_to_file(self.test_note, self.test_filename)
        with open(self.test_filename, 'r') as file:
            notes = json.load(file)
        
        self.assertEqual(len(notes), 1)  # Check one note saved
        self.assertEqual(notes[0]['content'], self.test_note.content)  # Check content matches

    def test_multiple_saves(self):
        """Test that multiple notes can be saved."""
        second_note = Note(content="Another note", label="Label 2", character="Character 2", date=None)
        save_to_file(self.test_note, self.test_filename)
        save_to_file(second_note, self.test_filename)

        with open(self.test_filename, 'r') as file:
            notes = json.load(file)
        
        self.assertEqual(len(notes), 2)  # Check two notes saved

if __name__ == "__main__":
    unittest.main()
