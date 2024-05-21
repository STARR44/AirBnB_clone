import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from models.base_model import BaseModel  # Adjust the import based on your project structure
import uuid


class TestBaseModel(unittest.TestCase):
    
    @patch('models.base_model.storage')
    def test_init_no_kwargs(self, mock_storage):
        """Test initialization without kwargs"""
        with patch('models.base_model.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)
            instance = BaseModel()
            
            self.assertIsInstance(instance.id, str)
            self.assertIsInstance(instance.created_at, datetime)
            self.assertIsInstance(instance.updated_at, datetime)
            self.assertEqual(instance.created_at, instance.updated_at)
            mock_storage.new.assert_called_once_with(instance)

    @patch('models.base_model.storage')
    def test_init_with_kwargs(self, mock_storage):
        """Test initialization with kwargs"""
        kwargs = {
            'id': '1234',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T01:00:00',
            'name': 'Test Model'
        }
        instance = BaseModel(**kwargs)
        
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at, datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(instance.updated_at, datetime.fromisoformat('2023-01-01T01:00:00'))
        self.assertEqual(instance.name, 'Test Model')
        mock_storage.new.assert_not_called()

    def test_str(self):
        """Test __str__ method"""
        instance = BaseModel()
        expected_str = f"[BaseModel] ({instance.id}) {instance.__dict__}"
        self.assertEqual(str(instance), expected_str)

    @patch('models.base_model.storage')
    def test_save(self, mock_storage):
        """Test save method"""
        instance = BaseModel()
        old_updated_at = instance.updated_at
        instance.save()
        
        self.assertNotEqual(instance.updated_at, old_updated_at)
        self.assertTrue(instance.updated_at > old_updated_at)
        mock_storage.new.assert_called_with(instance)
        mock_storage.save.assert_called_once()

    def test_to_dict(self):
        """Test to_dict method"""
        instance = BaseModel()
        instance_dict = instance.to_dict()
        
        self.assertEqual(instance_dict['__class__'], 'BaseModel')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'], instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'], instance.updated_at.isoformat())

    @patch('models.base_model.uuid.uuid4', return_value='1234')
    @patch('models.base_model.datetime')
    @patch('models.base_model.storage')
    def test_attributes_types(self, mock_storage, mock_datetime, mock_uuid):
        """Test if attributes are of correct type"""
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)
        
        instance = BaseModel()
        self.assertIsInstance(instance.id, str)
        self.assertEqual(instance.id, '1234')
        self.assertIsInstance(instance.created_at, datetime)
        self.assertEqual(instance.created_at, datetime(2023, 1, 1, 0, 0, 0))
        self.assertIsInstance(instance.updated_at, datetime)
        self.assertEqual(instance.updated_at, datetime(2023, 1, 1, 0, 0, 0))
        mock_storage.new.assert_called_once_with(instance)


if __name__ == '__main__':
    unittest.main()

