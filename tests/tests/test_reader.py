import pytest
import json
from pathlib import Path
from pathlib import Path
from order_pipeline.reader import Reader


class TestReader:
    """Tests for Reader class."""
    
    def test_read_valid_json(self, tmp_path):
        """Test reading valid JSON file."""
        data = [
            {"order_id": "1", "item": "Widget", "quantity": 2},
            {"order_id": "2", "item": "Gadget", "quantity": 1}
        ]
        file_path = tmp_path / "test.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        reader = Reader(str(file_path))
        result = reader.read()
        
        assert len(result) == 2
        assert result[0]['order_id'] == '1'
        assert result[1]['item'] == 'Gadget'
    
    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        reader = Reader('nonexistent.json')
        with pytest.raises(FileNotFoundError):
            reader.read()
    
    def test_unsupported_format(self, tmp_path):
        """Test error for unsupported file format."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,name\n1,test")
        
        reader = Reader(str(csv_file))
        with pytest.raises(ValueError, match="Unsupported file format"):
            reader.read()
    
    def test_empty_file(self, tmp_path):
        """Test error for empty JSON file."""
        file_path = tmp_path / "empty.json"
        with open(file_path, 'w') as f:
            json.dump([], f)
        
        reader = Reader(str(file_path))
        with pytest.raises(ValueError, match="File is empty"):
            reader.read()
    
    def test_invalid_json(self, tmp_path):
        """Test error for invalid JSON."""
        file_path = tmp_path / "invalid.json"
        with open(file_path, 'w') as f:
            f.write("{ invalid json }")
        
        reader = Reader(str(file_path))
        with pytest.raises(ValueError, match="Invalid JSON format"):
            reader.read()
    
    def test_json_not_list(self, tmp_path):
        """Test error when JSON is not a list."""
        file_path = tmp_path / "dict.json"
        with open(file_path, 'w') as f:
            json.dump({"order_id": "1"}, f)
        
        reader = Reader(str(file_path))
        with pytest.raises(ValueError, match="must contain a list"):
            reader.read()