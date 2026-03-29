from datetime  import datetime

def get_month():
    return datetime.now().strftime("%B")