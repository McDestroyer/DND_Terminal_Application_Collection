from threading import Thread, Lock

data_lock = Lock()
data = ""


def test():
    with data_lock:
        print(data)


t = Thread(target=test)
t.start()


while True:
    in_data = input("Enter data: ")
    with data_lock:
        data = in_data
        print(data)
