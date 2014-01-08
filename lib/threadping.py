import Queue
import threading
import subprocess
import logging
import socket


class ThreadPing (threading.Thread):

	__idth		= 0
	__log		= ''
	__queue		= Queue.Queue()
	__resultado 	= {}

	def __init__(self, queue,out_queue, idth, log):
		threading.Thread.__init__(self)

		self.__idth 	= idth
		self.__queue 	= queue
		self.__log 	= log
		self.__oqueue	= out_queue


	def __ping ( self, host ):
		return ( subprocess.call("ping -c 1 %s" % host, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT) )

	def __getname ( self, ip ):
		try:
			salida = socket.gethostbyaddr( ip )[0]
		except:
			salida = 0

		return salida
		

	def run(self):

		estado = []

		while True:
			estado = []
			#Recogemos de la cola
			host 	= self.__queue.get()

			nombre 	= self.__getname ( host )


			estado.append ( nombre )

			if ( self.__ping ( host ) == 0 ):
				mensaje = 'el host %s estaba vivo' % ( host )
				estado.append (1)
			else:
				mensaje = 'el host %s NO estaba vivo' % ( host )
				estado.append ( 0 )

			Salida= {}
			Salida [host] = estado
			self.__oqueue.put ( Salida )
			self.__resultado [ host ] = estado


			identificador = ( ' [%s]:%s (%s): ' % ( self.__idth , mensaje, nombre ) )
			if  self.__log:
				logging.debug ( identificador + mensaje )

			#marcamos tarea como finalizada:
			self.__queue.task_done()


	def getResultados ( self ):
		return self.__resultado

	def testing ( self ):
		print 'testing'

