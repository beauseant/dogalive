import Queue
import time
import argparse
import logging
import lib.threadping


def main( queue, log, args ):

	num_hilos 	= args.hilos
	inicio		= args.inicio
	final		= args.final
	direc_base	= args.segmento + '.' 
	
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

	for k,v in Salida.iteritems ():
		print k
		print v


if __name__ == "__main__":


	log = 0
	parser    = argparse.ArgumentParser ( description= 'ping con hilos' )
	parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')
	parser.add_argument('hilos', type=int, help='numero de hilos a lanzar')
	parser.add_argument('segmento', help='segmento a analizar, ej: 192.168.149')
	parser.add_argument('inicio', type=int, help='maquina inicial, ej:30 empezaria en [segmento].30')
	parser.add_argument('final', type=int, help='maquina final, ej:200')

	args     =    parser.parse_args()


	if args.d:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		log = 1


	queue = Queue.Queue()

	start = time.time()

	main( queue, log, args )


	logging.debug ( "Elapsed Time: %s" % (time.time() - start) )
