import zmq
import threading
import time

class proxy(threading.Thread):

	def __init__(self, xpub_port, xsub_port):
		super(proxy, self).__init__(daemon = True)

		self.context = zmq.Context()

		# Socket facing producers
		self.frontend = self.context.socket(zmq.XPUB)
		
		try:
			self.frontend.bind("tcp://*:" + str(xpub_port))
		except zmq.ZMQError as error:
			print("Error during creating XPUB")

		# Socket facing consumers
		self.backend = self.context.socket(zmq.XSUB)
		
		try:
			self.backend.bind("tcp://*:" + str(xsub_port))
		except zmq.ZMQError as error:
			print("Error during creating XSUB")
		

	def run(self):
		zmq.proxy(self.frontend, self.backend)

	def listen(self, event):
		# self.event = event
		self.start()