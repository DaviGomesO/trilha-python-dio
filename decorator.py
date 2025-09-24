from datetime import datetime
import functools

def log_transaction(func):
    @functools.wraps(func)
    def log_info(*args, **kwargs):
        success = func(*args, **kwargs)
        if success:
            normalize = lambda s: s.strip().replace("_", " ").lower()
            operation = normalize(func.__name__)
            print(f"Transação: {operation}, Data: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    
    return log_info