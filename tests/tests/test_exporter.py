import pytest
import json
from order_pipeline.exporter import Exporter


class TestExporter:
    """Tests for Exporter class."""
    
    def test_export_creates_file(self, tmp_path):
        """Test that export creates output file."""
        output_file = tmp_path / "output.json"
        exporter = Exporter(str(output_file))
        
        orders = [{'order_id': '1', 'total': 50.0}]
        exporter.export(orders)
        
        assert output_file.exists()
    
    def test_export_valid_json(self, tmp_path):
        """Test that exported file contains valid JSON."""
        output_file = tmp_path / "output.json"
        exporter = Exporter(str(output_file))
        
        orders = [{'order_id': '1', 'total': 50.0}]
        exporter.export(orders)
        
        with open(output_file) as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
        assert 'orders' in data
        assert 'metadata' in data
    
    def test_export_with_stats(self, tmp_path):
        """Test export with statistics included."""
        output_file = tmp_path / "output.json"
        exporter = Exporter(str(output_file))
        
        orders = [{'order_id': '1', 'total': 50.0}]
        stats = {'total_revenue': 50.0}
        
        exporter.export(orders, stats)
        
        with open(output_file) as f:
            data = json.load(f)
        
        assert 'statistics' in data
        assert data['statistics']['total_revenue'] == 50.0