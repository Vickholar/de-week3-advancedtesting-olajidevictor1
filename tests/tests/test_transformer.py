import pytest
from order_pipeline.transformer import Transformer


class TestTransformer:
    """Tests for Transformer class."""
    
    def test_transform_converts_to_numeric(self):
        """Test numeric conversion of string values."""
        transformer = Transformer()
        order = {
            'order_id': 'ORD001',
            'item': 'Widget',
            'quantity': '5',
            'price': '$10.50',
            'payment_status': 'PAID',
            'total': 'N5250'
        }
        
        result = transformer.transform([order])[0]
        
        assert isinstance(result['quantity'], float)
        assert isinstance(result['price'], float)
        assert isinstance(result['total'], float)
        assert result['quantity'] == 5.0
        assert result['price'] == 10.50
    
    def test_normalize_payment_status_variations(self):
        """Test payment status normalization."""
        transformer = Transformer()
        
        assert transformer._normalize_payment_status('PAID') == 'paid'
        assert transformer._normalize_payment_status('Paid') == 'paid'
        assert transformer._normalize_payment_status('paid') == 'paid'
        assert transformer._normalize_payment_status('  Paid  ') == 'paid'
        assert transformer._normalize_payment_status('pending') == 'pending'
        assert transformer._normalize_payment_status('refunded') == 'refunded'
    
    def test_clean_text_fields(self):
        """Test text field cleaning."""
        transformer = Transformer()
        order = {
            'order_id': 'ORD001',
            'item': '  Widget   with   spaces  ',
            'quantity': 1,
            'price': 10,
            'payment_status': 'paid',
            'total': 10
        }
        
        result = transformer.transform([order])[0]
        
        assert result['item'] == 'Widget with spaces'
        assert '  ' not in result['item']
    
    def test_recalculate_total(self):
        """Test total recalculation for consistency."""
        transformer = Transformer()
        order = {
            'order_id': 'ORD001',
            'item': 'Widget',
            'quantity': 3,
            'price': 10.0,
            'payment_status': 'paid',
            'total': 999
        }
        
        result = transformer.transform([order])[0]
        
        assert result['total'] == 30.0
    
    def test_currency_parsing(self):
        """Test various currency formats."""
        transformer = Transformer()
        
        assert transformer._to_numeric('$15.99') == 15.99
        assert transformer._to_numeric('N2000') == 2000.0
        assert transformer._to_numeric('45 dollars') == 45.0
        assert transformer._to_numeric('5usd') == 5.0