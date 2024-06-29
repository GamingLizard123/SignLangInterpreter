import threading
import handtracker as ht
import algorithm



def main():
    ht.runTracker()
 

try:
    main()
except Exception as e:
    print(e)