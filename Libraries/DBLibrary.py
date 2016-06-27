#!/usr/bin/python
#_*_ coding: utf-8

import pymssql
import csv
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from collections import defaultdict
from robot.api import logger

class DBLibrary(object):
	'''
		Database Library for Robot-Framework
			Prequisite:
				- xlsxwriter (Excel file library) #http://xlsxwriter.readthedocs.io/index.html
				- pymssql 2.1.1 (Microsoft SQL Server API library) #http://www.pymssql.org/en/latest/ref/pymssql.html
				
			Install from cmd:
				pip install pymssql==2.1.1
				pip install xlsxwriter
	'''
	
	def __init__(self): self._dbconnection = None	#Database connection
	def _encode_val(self, s): return unicode(s).encode("utf-8")
	def connect_to_database(self, dbServer, dbUser, dbPass, dbDatabase, dbPort=1433, dbQTimeout=0, dbLoginTimeout=60, charSet='UTF-8'):
		'''
			Connect to database. Must be called before calling any query actions.
		'''
		try:
			self._dbconnection = pymssql.connect(server=dbServer, user=dbUser, password=dbPass, database=dbDatabase, port=int(dbPort), timeout=int(dbQTimeout), login_timeout=int(dbLoginTimeout), charset=charSet, as_dict=False)
		except Exception as e:
			logger.error(e)
	
	def connect_to_database_by_cfFile(self, filename):
		'''
			Connect to database. Must be called before calling any query actions.
			Format:
				dbServer=@value\n
				dbPort=@value\n
				dbUser=@value\n
				dbPassword=@value\n
				dbDataBase=@value\n
				dbQueryTimeout=0\n
				dbLoginTimeout=60\n
		'''
		dict = {}
		f = open(filename)
		for lines in f:
			items = lines.split('=', 1)
			dict[items[0]]=items[1].rstrip('\n')
			
		self.connect_to_database(dict.get('dbServer'), dict.get('dbUser'), dict.get('dbPassword'), dict.get('dbDataBase'), dict.get('dbPort'), dict.get('dbQueryTimeout'), dict.get('dbLoginTimeout'))
	
	def disconnect_from_database(self):
		'''
			Disconnect from current database connection. Should be called after finishing all query actions.
		'''
		self._dbconnection.close()
	
	def get_query_result_csv(self, sql, csvFile, header=True):
		'''
			Build a csv file from result set of the sql command \n
			Example: get query result csv		select * from customer		test.csv
		'''
		
		cur = self._dbconnection.cursor()
		cur.execute(sql + ';')
		rows = cur.fetchall()
		
		with open(csvFile, "wb") as outfile:
			writer = csv.writer(outfile)
			if header: writer.writerow([column[0] for column in cur.description])	#Write header column
			for row in rows: writer.writerow([unicode(s).encode("utf-8") for s in row])
	
	def format_list_to_string(self, list, type='Number'):
		'''
			Return a string from a list with sql formated. Useful for IN condition
		'''
		if type == 'Number': return str(list).strip('[]').replace('u','').replace('\'','').replace(' ','')
		else: return str(list).strip('[]').replace('u','').replace(' ','')
	
	def get_query_result_excel(self, sql, excelFile, header=True):
		'''
			Build an excel file from result set of the sql command \n
			Example: get query result excel		select * from customer		test.xlsx
		'''
		
		cur = self._dbconnection.cursor()
		cur.execute(sql + ';')
		rows = cur.fetchall()
		
		workbook = Workbook(excelFile)
		sheet = workbook.add_worksheet()
		format = workbook.add_format({'bold': True})
		
		if header:
			for i, val in enumerate([column[0] for column in cur.description]): sheet.write(0, i, self._encode_val(val), format)	#Write header column
		for r, row in enumerate(rows):
			for c, cell in enumerate(row): sheet.write(r+1, c, cell) # Write table data
		workbook.close()
	
	def get_query_result_dict(self, sql):
		'''
			Return a list of dictionary which stands for each row in queried table
		'''
		cur = self._dbconnection.cursor()
		cur.execute(sql + ';')
		rows = cur.fetchall()
		return [dict(zip([column[0] for column in cur.description], map(self._encode_val, row))) for row in rows]
		
	def get_query_result_list(self, sql, header=True):
		'''
			Return a list of list which stands for each row in queried table
		'''
		cur = self._dbconnection.cursor()
		cur.execute(sql + ';')
		rows = cur.fetchall()
		
		data = []
		if header: data.append([column[0] for column in cur.description]) 	#Write header column
		for row in rows: data.append(row)
		return data