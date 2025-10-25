import pytest
import json
from pathlib import Path
from order_pipeline.pipeline import Pipeline


class TestPipelineIntegration:
    """Integration tests for complete pipeline."""
    
    def test_full_pipeline_execution(self, tmp_path):
        """Test complete pipeline execution."""
        input_data = [
            {
                'order_id': 'ORD001',
                'timestamp': '2025-10-19T08:00:00Z',
                'item': 'Widget',
                'quantity': 5,
                'price': '$10.00',
                'payment_status': 'PAID',
                'total': 50.0
            },
            {
                'order_id': 'ORD002',
                'timestamp': '2025-10-19T08:05:00Z',
                'item': 'Gadget',
                'quantity': 2,
                'price': 'N2500',
                'payment_status': 'pending',
                'total': 5000
            }
        ]
        
        input_file = tmp_path / "input.json"
        output_file = tmp_path / "output.json"
        
        with open(input_file, 'w') as f:
            json.dump(input_data, f)
        
        pipeline = Pipeline(str(input_file), str(output_file))
        results = pipeline.run()
        
        assert results['total_processed'] == 2
        assert output_file.exists()
        
        with open(output_file) as f:
            output = json.load(f)
        
        assert len(output['orders']) == 2
        assert 'statistics' in output
    
    def test_pipeline_with_invalid_data(self, tmp_path):
        """Test pipeline filters out invalid data."""
        input_data = [
            {
                'order_id': 'ORD001',
                'timestamp': '2025-10-19',
                'item': 'Valid',
                'quantity': 2,
                'price': 10,
                'payment_status': 'paid',
                'total': 20
            },
            {
                'order_id': 'ORD002',
                'item': 'Invalid',
                'quantity': -5,
                'price': 10,
                'payment_status': 'paid',
                'total': 50
            }
        ]
        
        input_file = tmp_path / "input.json"
        output_file = tmp_path / "output.json"
        
        with open(input_file, 'w') as f:
            json.dump(input_data, f)
        
        pipeline = Pipeline(str(input_file), str(output_file))
        results = pipeline.run()
        
        assert results['total_processed'] == 1
        assert results['validation_summary']['invalid_rows'] == 1