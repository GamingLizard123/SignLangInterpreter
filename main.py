import threading
import handtracker as ht
import algorithm



def main():
    
    thread1 = threading.Thread(target=ht.runTracker)
    thread2 = threading.Thread(target=algorithm.run)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


main()