import Queue
import threading
import subprocess
import logging



class ThreadPing (threading.Thread):

	__idth		= 0
	__log		= ''
	__queue		= Queue.Queue()
	__resultado 	= {}

	def __init__(self, queue, idth, log):
		threading.Thread.__init__(self)

		self.__idth 	= idth
		self.__queue 	= queue
		self.__log 	= log


	def __ping ( self, host ):
		return ( subprocess.call("ping -c 1 %s" % host, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT) )
		

	def run(self):
		while True:
			#Recogemos de la cola
			host = self.__queue.get()
			if ( self.__ping ( host ) == 0 ):
				mensaje = 'el host %s estaba vivo' % ( host )
				self.__resultado [ host ] = 1
			else:
				mensaje = 'el host %s NO estaba vivo' % ( host )
				self.__resultado [ host ] = 0


			identificador = ( ' [%s]: ' % self.__idth )
			if  self.__log:
				logging.debug ( identificador + mensaje )

			#marcamos tarea como finalizada:
			self.__queue.task_done()


	def getResultados ( self ):
		return self.__resultado

	def testing ( self ):
		print 'testing'

