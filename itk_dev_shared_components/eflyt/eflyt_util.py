"""General helper funtions"""
from datetime import date


def format_date(_date: date) -> str:
    """Format date as %d-%m-%Y"""
    return _date.strftime("%d-%m-%Y")
