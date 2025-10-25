import re
from typing import List, Dict, Any


class Transformer:
    """Transforms and normalizes order data."""
    
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform list of orders.
        
        Args:
            data: List of valid orders
            
        Returns:
            List of transformed orders
        """
        transformed = []
        
        for order in data:
            transformed_order = self._transform_order(order.copy())
            transformed.append(transformed_order)
        
        return transformed
    
    def _transform_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a single order."""
        # Convert to numeric
        order['quantity'] = self._to_numeric(order['quantity'])
        order['price'] = self._to_numeric(order['price'])
        order['total'] = self._to_numeric(order['total'])
        
        # Normalize payment status
        order['payment_status'] = self._normalize_payment_status(
            order['payment_status']
        )
        
        # Clean text fields
        if 'item' in order:
            order['item'] = self._clean_text(order['item'])
        
        # Recalculate total for consistency
        order['total'] = round(order['quantity'] * order['price'], 2)
        
        return order
    
    def _to_numeric(self, value: Any) -> float:
        """Convert value to numeric."""
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove currency symbols and text
            cleaned = re.sub(r'[^0-9.]', '', value)
            return float(cleaned) if cleaned else 0.0
        
        return float(value)
    
    def _normalize_payment_status(self, status: str) -> str:
        """Normalize payment status to lowercase."""
        if isinstance(status, str):
            normalized = status.strip().lower()
            # Map variations
            if normalized in ['paid', 'complete', 'completed', 'success']:
                return 'paid'
            elif normalized in ['pending', 'processing', 'awaiting']:
                return 'pending'
            elif normalized in ['refunded', 'refund', 'cancelled', 'canceled']:
                return 'refunded'
            return normalized
        return str(status).strip().lower()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text fields."""
        if not isinstance(text, str):
            return str(text)
        
        # Trim whitespace
        text = text.strip()
        
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text