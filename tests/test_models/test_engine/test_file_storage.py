import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from io import StringIO
from models.engine.file_storage import FileStorage


# Mock object for testing
class MockObject:
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {'__class__': 'MockObject', 'id': self.id}

class TestFileStorage(unittest.TestCase):
    
    def setUp(self):
        self.storage = FileStorage()
        self.mock_obj = MockObject(id='1234')

    def test_all(self):
        # Verify that all() returns the internal dictionary
        FileStorage._FileStorage__objects = {}
        self.assertEqual(self.storage.all(), {})

    def test_new(self):
        # Verify that new() adds an object to the internal dictionary
        FileStorage._FileStorage__objects = {}
        self.storage.new(self.mock_obj)
        expected_key = 'MockObject.1234'
        self.assertIn(expected_key, self.storage.all())
        self.assertEqual(self.storage.all()[expected_key], self.mock_obj.to_dict())


    @patch('builtins.open', new_callable=mock_open)
    def test_save(self, mock_open):
        # Verify that save() writes the internal dictionary to a file
        FileStorage._FileStorage__objects = {'MockObject.1234': self.mock_obj.to_dict()}
        self.storage.save()
        mock_open.assert_called_once_with(FileStorage._FileStorage__file_path, 'w')
        handle = mock_open()
        handle.write.assert_called()
        # Combine all write calls into a single string to compare the final content
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        expected_content = json.dumps({'MockObject.1234': self.mock_obj.to_dict()})
        self.assertEqual(written_content, expected_content)

    @patch('builtins.open', new_callable=mock_open, read_data='{"MockObject.1234": {"__class__": "MockObject", "id": "1234"}}')
    def test_reload(self, mock_open):
        # Verify that reload() reads the file and updates the internal dictionary
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        mock_open.assert_called_once_with(FileStorage._FileStorage__file_path, 'r')
        self.assertIn('MockObject.1234', self.storage.all())
        self.assertEqual(self.storage.all()['MockObject.1234'], {"__class__": "MockObject", "id": "1234"})

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_reload_file_not_found(self, mock_open):
        # Verify that reload() handles the file not found scenario gracefully
        FileStorage._FileStorage__objects = {'MockObject.1234': self.mock_obj.to_dict()}
        self.storage.reload()
        mock_open.assert_called_once_with(FileStorage._FileStorage__file_path, 'r')
        self.assertEqual(self.storage.all(), {'MockObject.1234': self.mock_obj.to_dict()})

if __name__ == '__main__':
    unittest.main()

