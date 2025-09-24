from datetime import datetime
import functools
from pathlib import Path
import os

PATH_ROOT = Path(__file__).parent

def log_transaction(func):
    @functools.wraps(func)
    def log_info(*args, **kwargs):
        success = func(*args, **kwargs)
        if success:
            normalize = lambda s: s.strip().replace("_", " ").lower()
            operation = normalize(func.__name__)
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            PATH_LOG = PATH_ROOT / "logs" / "transaction_log.txt"
            os.mkdir(PATH_LOG.parent) if not os.path.exists(PATH_LOG.parent) else None
            with open(PATH_LOG, "a", newline='') as log_file:
                log_file.write(f"[{data_hora}] - Função {operation} executada com argumentos {args} e {kwargs}. Retornou: {success}\n")
    
    return log_info