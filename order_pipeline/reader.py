import json
from typing import List, Dict, Any
from pathlib import Path


class Reader:
    """Reads order data from JSON files."""
    
    def __init__(self, filepath: str):
        """
        Initialize the Reader with a file path.
        
        Args:
            filepath: Path to the JSON file
        """
        self.filepath = Path(filepath)
    
    def read(self) -> List[Dict[str, Any]]:
        """
        Read data from JSON file.
        
        Returns:
            List of order dictionaries
            
        Raises:
            ValueError: If file format is unsupported or file is empty
            FileNotFoundError: If file doesn't exist
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        if self.filepath.suffix.lower() != '.json':
            raise ValueError(f"Unsupported file format: {self.filepath.suffix}")
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        
        if not data:
            raise ValueError("File is empty")
        
        if not isinstance(data, list):
            raise ValueError("JSON must contain a list of orders")
        
        return data