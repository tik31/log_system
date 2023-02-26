import time
import zmq


class test_subscriber():
    
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def connect(self):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        
        try:
            self.subscriber.connect("tcp://localhost:5559")
        except zmq.ZMQError as error:
            print("Error during connecting to ZMQ proxy:", error)        

    def recv(self):
        [address, contents] = self.subscriber.recv_multipart()
        print(f"[{address}] {contents}")

    def subscribe(self):
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    
sub = test_subscriber("GUI", "tcp://localhost:5559")
sub.connect()
sub.subscribe()
try:
    while True:
        sub.recv()
except KeyboardInterrupt:
    print("Exited by user")
finally:
    sub.subscriber.close()
    sub.context.term()
    del(sub)
