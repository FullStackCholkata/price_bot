from datetime import datetime

# Returns the timestamp used for printing out the control and debug messages
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
