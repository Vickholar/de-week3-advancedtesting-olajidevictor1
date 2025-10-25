import pytest
from order_pipeline.validator import Validator


class TestValidator:
    """Tests for Validator class."""
    
    def test_validate_valid_order(self, sample_valid_order):
        """Test validation of valid order."""
        validator = Validator()
        result = validator.validate([sample_valid_order])
        
        assert len(result) == 1
        assert result[0]['order_id'] == 'ORD001'
        assert validator.validation_summary['valid_rows'] == 1
        assert validator.validation_summary['invalid_rows'] == 0
    
    def test_missing_required_field(self):
        """Test rejection of order with missing field."""
        validator = Validator()
        order = {
            'order_id': 'ORD123',
            'timestamp': '2025-01-15',
            'item': 'Widget'
            # Missing quantity, price, payment_status, total
        }
        result = validator.validate([order])
        
        assert len(result) == 0
        assert validator.validation_summary['invalid_rows'] == 1
    
    def test_empty_item_field(self):
        """Test rejection of order with empty item field."""
        validator = Validator()
        order = {
            'order_id': 'ORD005',
            'timestamp': '2025-10-19T08:20:00Z',
            'item': '',
            'quantity': 1,
            'price': '45 dollars',
            'total': 45,
            'payment_status': 'refunded'
        }
        result = validator.validate([order])
        
        assert len(result) == 0
        assert validator.validation_summary['invalid_rows'] == 1
    
    def test_negative_quantity(self):
        """Test rejection of negative quantity."""
        validator = Validator()
        order = {
            'order_id': 'ORD003',
            'timestamp': '19/10/2025 08:10 AM',
            'item': 'USB Cable',
            'quantity': -3,
            'price': '5usd',
            'total': 15,
            'payment_status': 'pending'
        }
        result = validator.validate([order])
        
        assert len(result) == 0
        assert validator.validation_summary['invalid_rows'] == 1
    
    def test_extract_numeric_currency_formats(self):
        """Test numeric extraction from various currency formats."""
        validator = Validator()
        
        assert validator._extract_numeric('$25.50') == 25.50
        assert validator._extract_numeric('N2000') == 2000
        assert validator._extract_numeric('45 dollars') == 45
        assert validator._extract_numeric('5usd') == 5
        assert validator._extract_numeric(100) == 100.0
    
    def test_extract_numeric_invalid(self):
        """Test numeric extraction fails for invalid values."""
        validator = Validator()
        
        with pytest.raises(ValueError):
            validator._extract_numeric('N/A')
    
    def test_validation_summary(self, sample_orders_with_edge_cases):
        """Test validation summary generation."""
        validator = Validator()
        validator.validate(sample_orders_with_edge_cases)
        summary = validator.get_summary()
        
        assert summary['total_rows'] == 3
        assert summary['valid_rows'] == 3