"""Shared test fixtures for the test suite."""
import pytest
import json
from pathlib import Path


@pytest.fixture
def sample_valid_order():
    """A completely valid order for testing."""
    return {
        'order_id': 'ORD001',
        'timestamp': '2025-10-19T08:00:00Z',
        'item': 'Wireless Mouse',
        'quantity': 2,
        'price': 15.99,
        'payment_status': 'paid',
        'total': 31.98
    }


@pytest.fixture
def sample_orders_with_edge_cases():
    """Sample orders with various edge cases from the actual data."""
    return [
        {
            'order_id': 'ORD001',
            'timestamp': '2025-10-19T08:00:00Z',
            'item': 'Wireless Mouse',
            'quantity': 2,
            'price': '$15.99',
            'total': '$31.98',
            'payment_status': 'paid'
        },
        {
            'order_id': 'ORD002',
            'timestamp': '2025-10-19 08:05',
            'item': 'Laptop Sleeve',
            'quantity': '1',
            'price': '12.50',
            'total': '12.50',
            'payment_status': 'PAID'
        },
        {
            'order_id': 'ORD006',
            'timestamp': '2025/10/19T08:25Z',
            'item': 'Phone Case',
            'quantity': 3,
            'price': 'N2000',
            'total': 'N6000',
            'payment_status': 'PAID'
        }
    ]