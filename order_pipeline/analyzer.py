from typing import List, Dict, Any


class Analyzer:
    """Analyzes order data and computes statistics."""
    
    def analyze(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze order data.
        
        Args:
            data: List of transformed orders
            
        Returns:
            Dictionary with analysis results
        """
        if not data:
            return {
                'total_orders': 0,
                'total_revenue': 0.0,
                'average_revenue': 0.0,
                'payment_status_counts': {
                    'paid': 0,
                    'pending': 0,
                    'refunded': 0
                }
            }
        
        total_revenue = sum(order['total'] for order in data)
        payment_counts = self._count_payment_statuses(data)
        
        return {
            'total_orders': len(data),
            'total_revenue': round(total_revenue, 2),
            'average_revenue': round(total_revenue / len(data), 2),
            'payment_status_counts': payment_counts
        }
    
    def _count_payment_statuses(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count orders by payment status."""
        counts = {'paid': 0, 'pending': 0, 'refunded': 0}
        
        for order in data:
            status = order.get('payment_status', '').lower()
            if status in counts:
                counts[status] += 1
            else:
                # Count unknown statuses as pending
                counts['pending'] += 1
        
        return counts