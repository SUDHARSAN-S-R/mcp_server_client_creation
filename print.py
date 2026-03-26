
from datetime import datetime





def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def current_date():
    return datetime.now().strftime("%Y-%m-%d")

def current_time_only():
    return datetime.now().strftime("%H:%M:%S")

def current_month():
    return datetime.now().strftime("%B")

def current_year():
    return datetime.now().strftime("%Y")

