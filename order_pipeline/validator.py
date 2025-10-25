import re
from typing import List, Dict, Any, Optional, Tuple


class Validator:
    """Validates order data."""
    
    REQUIRED_FIELDS = [
        'order_id', 'timestamp', 'item', 
        'quantity', 'price', 'payment_status', 'total'
    ]
    
    def __init__(self):
        self.invalid_rows = []
        self.validation_summary = {
            'total_rows': 0,
            'valid_rows': 0,
            'invalid_rows': 0,
            'reasons': {}
        }
    
    def validate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate list of orders.
        
        Args:
            data: List of order dictionaries
            
        Returns:
            List of valid orders
        """
        valid_orders = []
        self.validation_summary['total_rows'] = len(data)
        
        for idx, order in enumerate(data):
            is_valid, reason = self._validate_order(order)
            
            if is_valid:
                valid_orders.append(order)
                self.validation_summary['valid_rows'] += 1
            else:
                self.invalid_rows.append({'index': idx, 'order': order, 'reason': reason})
                self.validation_summary['invalid_rows'] += 1
                self.validation_summary['reasons'][reason] = \
                    self.validation_summary['reasons'].get(reason, 0) + 1
        
        return valid_orders
    
    def _validate_order(self, order: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate a single order.
        
        Returns:
            Tuple of (is_valid, reason_if_invalid)
        """
        # Check required fields
        missing_fields = [field for field in self.REQUIRED_FIELDS 
                         if field not in order or order[field] is None or order[field] == '']
        if missing_fields:
            return False, f"Missing fields: {', '.join(missing_fields)}"
        
        # Validate quantity
        try:
            qty = self._extract_numeric(order['quantity'])
            if qty <= 0:
                return False, "Quantity must be positive"
        except (ValueError, TypeError):
            return False, "Invalid quantity format"
        
        # Validate price
        try:
            price = self._extract_numeric(order['price'])
            if price <= 0:
                return False, "Price must be positive"
        except (ValueError, TypeError):
            return False, "Invalid price format"
        
        # Validate total
        try:
            total = self._extract_numeric(order['total'])
            if total <= 0:
                return False, "Total must be positive"
        except (ValueError, TypeError):
            return False, "Invalid total format"
        
        return True, None
    
    def _extract_numeric(self, value: Any) -> float:
        """Extract numeric value from various formats."""
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove currency symbols, whitespace, and common text
            cleaned = re.sub(r'[^0-9.]', '', value)
            if cleaned:
                return float(cleaned)
        
        raise ValueError(f"Cannot convert to numeric: {value}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        return self.validation_summary