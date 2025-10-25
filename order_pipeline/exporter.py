import json
from pathlib import Path
from typing import List, Dict, Any


class Exporter:
    """Exports cleaned data to JSON."""
    
    def __init__(self, output_path: str):
        """
        Initialize Exporter.
        
        Args:
            output_path: Path for output file
        """
        self.output_path = Path(output_path)
    
    def export(self, data: List[Dict[str, Any]], 
               stats: Dict[str, Any] = None) -> None:
        """
        Export data to JSON file.
        
        Args:
            data: List of cleaned orders
            stats: Optional statistics to include
            
        Raises:
            IOError: If file cannot be written
        """
        output = {
            'orders': data,
            'metadata': {
                'total_orders': len(data)
            }
        }
        
        if stats:
            output['statistics'] = stats
        
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Failed to write file: {e}")