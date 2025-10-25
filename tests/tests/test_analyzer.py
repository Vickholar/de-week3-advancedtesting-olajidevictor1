import pytest
from order_pipeline.analyzer import Analyzer


class TestAnalyzer:
    """Tests for Analyzer class."""
    
    def test_analyze_total_orders(self):
        """Test total orders count."""
        analyzer = Analyzer()
        orders = [
            {'order_id': '1', 'total': 50.0, 'payment_status': 'paid'},
            {'order_id': '2', 'total': 30.0, 'payment_status': 'paid'},
            {'order_id': '3', 'total': 100.0, 'payment_status': 'pending'}
        ]
        
        result = analyzer.analyze(orders)
        
        assert result['total_orders'] == 3
    
    def test_analyze_total_revenue(self):
        """Test total revenue calculation."""
        analyzer = Analyzer()
        orders = [
            {'total': 50.0, 'payment_status': 'paid'},
            {'total': 50.0, 'payment_status': 'paid'},
            {'total': 100.0, 'payment_status': 'pending'}
        ]
        
        result = analyzer.analyze(orders)
        
        assert result['total_revenue'] == 200.0
    
    def test_analyze_payment_status_counts(self):
        """Test payment status counting."""
        analyzer = Analyzer()
        orders = [
            {'total': 50.0, 'payment_status': 'paid'},
            {'total': 50.0, 'payment_status': 'paid'},
            {'total': 100.0, 'payment_status': 'pending'},
            {'total': 45.0, 'payment_status': 'refunded'}
        ]
        
        result = analyzer.analyze(orders)
        counts = result['payment_status_counts']
        
        assert counts['paid'] == 2
        assert counts['pending'] == 1
        assert counts['refunded'] == 1
    
    def test_analyze_empty_data(self):
        """Test analysis with empty data."""
        analyzer = Analyzer()
        
        result = analyzer.analyze([])
        
        assert result['total_orders'] == 0
        assert result['total_revenue'] == 0.0
        assert result['average_revenue'] == 0.0