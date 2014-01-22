#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import logging
import argparse
import datetime


class operacionesDB:
	_name	= ''
	_con	= None
	_dir	= ''
	_date	= None


	def __init__ ( self, direct, database, date ):
		self._name = database
		self._dir = direct
		self._date = date
		self._name = direct + self._name

		try:
   		    logging.debug ( "Abriendo la bd: %s" % self._name )
		    self._con = lite.connect( self._name )            
		    
		except lite.Error, e:		    
		    print "Error %s:" % e.args[0]
		    sys.exit(1)   
 

	def __del__ ( self ):
		if self._con:
			self._con.close()

	#Creacion de todas las tablas de la DB
	def reiniciarDB ( self ):
		logging.debug ( "Creando desde cero la base de datos..." )	
		self.crearTablaHosts()
		self.crearTablaFechas()
		self.crearTablaEscaneo()


	#Crea tabla para almacenar los distintos hosts
	def crearTablaHosts ( self ):
		with self._con:  
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS hosts")
			sql_sen = '''CREATE TABLE hosts (
				id_host INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				ip VARCHAR(15) UNIQUE NOT NULL, 
				name VARCHAR(30))'''
			cur.execute(sql_sen)

			sql_index = '''CREATE INDEX indice_ip on hosts (ip)'''
			cur.execute(sql_index)

			self._con.commit()


	#Crea tabla para introducir la fecha de los escaneos
	def crearTablaFechas ( self ):
		with self._con:  
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS dates")
			sql_sen = '''CREATE TABLE dates (
				id_date INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				total INTEGER NOT NULL DEFAULT 0,
				vivos INTEGER NOT NULL DEFAULT 0,
				date DATE NOT NULL)'''
			cur.execute(sql_sen)
			self._con.commit()


	#Crea tabla con la fecha de realizacion de los distintos pings a los hosts
	#Status 0=No responde 1=Activo
	def crearTablaEscaneo ( self ):
		with self._con:  
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS scan")
			sql_sen = '''CREATE TABLE scan (
				id_host INTEGER NOT NULL, 
				id_date INTEGER NOT NULL, 
				status INT(1) NOT NULL,
				PRIMARY KEY (id_host,id_date),
				FOREIGN KEY (id_host) REFERENCES hosts(id_host),
				FOREIGN KEY (id_date) REFERENCES dates(id_date)
				)'''   
			cur.execute(sql_sen)
			self._con.commit()

	#Inserta un host
	def insertarHost( self, ip, name ):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT id_host FROM hosts WHERE ip=?", (ip,))
			h = cur.fetchone()
			if not (h):
				cur.execute ("INSERT INTO hosts (id_host, ip, name) VALUES (NULL,?,?)", (ip, name))
				#self._con.commit()
				#logging.debug ( "Insert host: %s" % ( ip ) )
				return cur.lastrowid
			else:
				#logging.debug ( "Load host: %s" % ( ip ) )
				return h[0]

	#Inserta una fecha de escaneo
	def insertarFecha ( self ):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT id_date FROM dates WHERE date=?", (self._date,))
			d = cur.fetchone()
			if not (d):
				cur.execute ("INSERT INTO dates (id_date, date) VALUES (NULL, ?)", (self._date,))
				self._con.commit()
				return cur.lastrowid
			else:
				return d[0]


	#Inserta la informacion del escaneo
	def insertarEscaneo ( self, id_host, id_date, status ):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM scan WHERE id_host=? AND id_date=?", (id_host, id_date))

			d = cur.fetchone()

			if not (d):
				#print ( "INSERT INTO scan VALUES (%s,%s,%s)" ) % (id_host, id_date, status)
				cur.execute ("INSERT INTO scan VALUES (?,?,?)", (id_host, id_date, status))
				self._con.commit()
			else:
				cur.execute ("UPDATE scan SET status=? WHERE id_host=? AND id_date=?", (status, id_host,id_date))
				self._con.commit()	


	#Actualiza los totales del escaneo (vivos y totales):
	def actualizarTotales ( self, id_date, total, vivos ):
		try:
			with self._con:    
				cur = self._con.cursor()
				cur.execute ("UPDATE dates SET total=?,vivos=? WHERE id_date=? ", (total, vivos,id_date))
				self._con.commit()
		except Exception as e:
			print e


	#Muestra los hosts existentes
	def recuperarHosts ( self ):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM hosts")
			hosts =	cur.fetchall()
			return hosts

	#Muestra las fechas en las que se realizaron escaneos
	def recuperarFechas ( self ):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM dates ORDER BY id_date DESC")
			dates =	cur.fetchall()
			return dates

	#Muestra los escaneos realizados
	def recuperarEscaneos ( self ):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM scan")
			scans =	cur.fetchall()
			return scans

	def recuperarEscaneosPorHost ( self, id_host):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM scan WHERE id_host =?", (id_host,))
			scans =	cur.fetchall()
			return scans


	def recuperarHostPorId ( self, id_host):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM hosts WHERE id_host =?", (id_host,))
			hosts =	cur.fetchall()
			return hosts

	def recuperarEscaneosPorFecha ( self, id_fecha):
		with self._con:    
			cur = self._con.cursor()
			cur.execute ("SELECT * FROM scan WHERE id_date =?", (id_fecha,))
			scans =	cur.fetchall()
			return scans


	def setTransaccion ( self, estado):
		with self._con:    
			cur 		= self._con.cursor()
			sentencia 	= "PRAGMA synchronous = %s" % (estado)
			cur.execute ( sentencia)
			logging.debug ( "PRAGMA sync fijado a: %s" % ( estado ) )





