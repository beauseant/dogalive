#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import logging
import argparse
import datetime


class grabarDB:
	_name	= 'sqlite.db'
	_con	= None
	_dir	= ''
	
	def crearTablas ( self, db ):
		db.crearTablaHosts()
		db.crearTablaFechas()
		db.crearTablaEscaneo()

	def __init__ ( self, direct ):

		self._dir = direct

		try:
		    self._con = lite.connect( self._name )            
		    
		except lite.Error, e:
		    
		    print "Error %s:" % e.args[0]
		    sys.exit(1)    

	def __del__ ( self ):
		if self._con:
			self._con.close()


	def crearTablaHosts ( self ):
		with self._con:  
			#Creando tabla con los distintos hosts
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS hosts")
			sql_sen = '''CREATE TABLE hosts (
				id_host INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				ip VARCHAR(15) UNIQUE NOT NULL, 
				name VARCHAR(30))'''
			cur.execute(sql_sen)
			self._con.commit()

	def crearTablaFechas ( self ):
		with self._con:  
			#Creando tabla de fechas
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS dates")
			sql_sen = '''CREATE TABLE dates (
				id_date INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				date DATE NOT NULL)'''
			cur.execute(sql_sen)
			self._con.commit()


	def crearTablaEscaneo ( self ):
		with self._con:  
			#Creando tabla con la fecha de realizacion de los distintos pings a los hosts
			#Status 0=No responde 1=Activo
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS scan")
			sql_sen = '''CREATE TABLE scan (
				id INTEGER NOT NULL, 
				date INTEGER NOT NULL, 
				status INT(1) NOT NULL,
				PRIMARY KEY (id,date),
				FOREIGN KEY (id) REFERENCES hosts(id_host),
				FOREIGN KEY (date) REFERENCES dates(id_date)
				)'''   
			cur.execute(sql_sen)
			self._con.commit()


	def insertarHosts( self, hosts ):
		with self._con:    
			#Insertando los hosts a escanear
			cur = self._con.cursor()
			for key,value in hosts.items():
				cur.execute ("INSERT INTO hosts (id_host, ip, name) VALUES (NULL,?,?)", (key, value))
			self._con.commit()

	def insertarFecha ( self, date ):
		with self._con:    
			#Insertando la fecha del escaneo
			cur = self._con.cursor()
			cur.execute ("INSERT INTO dates (id_date, date) VALUES (NULL, ?)", (date))
			self._con.commit()

	def insertarEscaneo ( self, id_host, id_date, status ):
		with self._con:    
			#Insertando los datos del escaneo de hosts
			cur = self._con.cursor()
			cur.execute ("INSERT INTO scan VALUES (?,?,?)", (id_host, id_date, status))
			self._con.commit()

	
if __name__ == "__main__":
	parser	= argparse.ArgumentParser ( description= '' )
	parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')

	args	 =	parser.parse_args()

	if args.d:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

	db = GrabarDB ('SQLitePrueba/')

	hosts = {"192.168.149.19":"charran","192.168.149.20":"loro","192.168.149.21":"piquituerto"}

	db.crearTablas ( db )
	date = datetime.date.today()
	db.insertarEscaneo (1,1,0)
	db.mostrarHosts ()
	
	print 'Fin del proceso'






