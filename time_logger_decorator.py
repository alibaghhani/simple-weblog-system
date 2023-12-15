from datetime import datetime
def logger(func):
    def inner(*args, **kwargs):
        called_at = datetime.now()
        to_execute = func(*args, **kwargs)
        with open("weblog_logs.txt","a") as loger_file:
            loger_file.write(f"{func.__name__} done. logged at {called_at}\n")
        return to_execute
    return inner

