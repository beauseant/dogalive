import Queue
import time
import argparse
import logging
import lib.threadping
import datetime


def main( queue, log ):

	num_hilos 	= 3
	inicio		= 10
	final		= 13
	direc_base	= '192.168.1.'
	
	#generamos los hilos que queremos y en cada uno pasamos la cola como instancia y el identificador:
	for i in range( num_hilos ):
		t = lib.threadping.ThreadPing (queue, i, log )
		t.setDaemon ( True )
		t.start()

	#Metemos en la cola lo que queremos procesar y que sera recogido por los hilos anteriores:
	for host in range ( inicio , int (final) ) :
		queue.put(direc_base + str (host) )

	#Nos quedamos esperando a que no quede nada por procesar:
	queue.join()

	#Recogemos los datos de cada uno de los hilos:
	Salida = {}
	for i in range( num_hilos ):
		Salida.update ( t.getResultados () )


	#Aqui debemos llamar a la libreria que se encarga de grabar el log de las operaciones
	#debemos pasarle, ademas la fecha
	date = datetime.today()
	#hist = grabarDB ( fechaactual)
	for k,v in Salida.iteritems ():
		#hist.addMaquina (k ,v)
		print k
		print v


if __name__ == "__main__":


	log = 0
	parser    = argparse.ArgumentParser ( description= 'ping con hilos' )
	parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')

	args     =    parser.parse_args()

	if args.d:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		log = 1


	queue = Queue.Queue()

	start = time.time()

	main( queue, log )

	print "Elapsed Time: %s" % (time.time() - start)
