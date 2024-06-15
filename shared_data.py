import threading

running = True

shared_data = []

lock = threading.Lock()

written = False

def share_data(data):
    share_data = data