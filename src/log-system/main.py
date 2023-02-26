import proxy
import time
import sys
import os
import click
import threading

@click.command()
@click.option('--xpub_port', default = 5559, help='number of XPUB port')
@click.option('--xsub_port', default = 5560, help='number of XSUB port')
@click.argument('db_name', nargs = 1,)


def main(xpub_port, xsub_port, db_name):
	""" Help message """
	
	sys.path.insert(1, '../db_logger/src')
	try:
		import db_logger_zmq
	except ModuleNotFoundError as e:
		print("ERROR: ", e)
		quit()

	print("Starting Log-system...")

	event = threading.Event()

	try:
		# Создание и запуск брокера
		# TODO: Здесть должен быть обработчик ошибок. Сейчас все ощибки обрабатываются внутри
		broker = proxy.proxy(xpub_port, xsub_port)
		broker.listen(event)


		# Создание и запус логгера
		logger = db_logger_zmq.db_logger_zmq("tcp://localhost:5559")
		db_path = "../../db/"
		db_fname = "test.db"
		if not os.path.exists(db_path):
			os.makedirs(db_path)

		logger.open_database(db_path + db_fname)
		# TODO: Убрать параметр внутри db_logger
		logger.create_database("asdf")

		logger.connect()
		logger.subscribe(["MULT", "GEN", ])
		logger.listen()

		while True:
			pass

	except KeyboardInterrupt:
		print("Exited by user") 
		event.set()

	

if __name__ == '__main__':
    main()








# logger = db_logger_zmq.db_logger_zmq("tcp://localhost:5559")

# # Проверка и создание каталога для БД
# # TODO: должно браться из аргументов командной строки

# db_path = "../../db/"
# db_fname = "test.db"
# if not os.path.exists(db_path):
# 	os.makedirs(db_path)



# logger.open_database(db_path + db_fname)
# logger.create_database("asd")

# logger.connect()
# logger.subscribe(["MULT", "GEN", ])
# logger.listen()



# while True:
# 	print("567")
# 	time.sleep(1)

# try:
# 	p.listen()
# except KeyboardInterrupt as e:
# 	print("Exited by user")
# finally:
# 	p.frontend.close()
# 	p.backend.close()
# 	p.context.term()
# 	del(logger)

# del(p)
