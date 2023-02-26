import time
import zmq
import datetime
import json
import event

class test_publisher:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def connect(self):
        self.context = zmq.Context()

        self.publisher = self.context.socket(zmq.PUB)

        try:
            self.publisher.connect(self.address)
        except zmq.ZMQError as error:
            print("Error during connecting to ZMQ proxy:", error)

        time.sleep(0.1)

    def send(self, s):
        self.publisher.send_multipart([self.name.encode("utf-8"), s.encode("utf-8")])


pub = test_publisher("MULTIMETR", "tcp://localhost:5560")
pub.connect()
time.sleep(1)
l = []

ev = event.event()
for i in range(0, 10):
    

    ev.Parameter = "MB1"
    ev.Level = "INFO"
    ev.Source = "MULTIMETR"
    ev.Time = str(datetime.datetime.now())
    ev.Value = "1.2345"

    l.append(ev)
    # s = json.dumps(ev.__dict__)


    # print(s)
    # pub.send(s)
    time.sleep(0.1)

s = json.dumps([ob.__dict__ for ob in l])
# s = json.dumps(ev.__dict__)
print(s)
pub.send(s)
        

pub.publisher.close()
pub.context.term()

del(pub)