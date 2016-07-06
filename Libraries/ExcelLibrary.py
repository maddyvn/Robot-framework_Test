from openpyxl import load_workbook
from decimal import Decimal

class ExcelLibrary(object):
	
# Private functions
	def _read(self, f, r=True): return load_workbook(filename=f, read_only=r)
	
	def _sheet(self, f, s, r=True): return self._read(f, r)[str(s)]
	
	def _float(self, s): return float(str(s)) if self._isfloat(s) else s
	
	def _format(self, s): return str(s).replace('u','').replace('\'','')
	
	def _isDigit(self, s): return s[1:].isdigit() if s[0] in ('-', '+') else s.isdigit()
	
	def _validate_index(self, i):
		if int(i) < 1: raise Exception('Wrong index number provided. Should >= 1')
		else: return int(i)
		
	def _parse(self, s):
		try:
			if str(s).isdigit():	# is s is only digit
				if isinstance(s, float): return str(s).rstrip('0').rstrip('.')
				elif isinstance(s, int): return int(s)
				elif isinstance(s, complex): return str(s)
			return str(s)
		except ValueError as err: raise Exception(err)
	
	def _data(self, file, sheet, noheader=True):
		data = [[self._parse(x.value) for x in row] for row in self._sheet(file, sheet).rows]
		header = data[0]
		if noheader: del data[0]
		return data, header
		
	def _list_to_dict(self, data, header): return [dict(zip(header, map(str, row))) for row in data]

# Public function
	def get_sheet_content(self, file, sheet, asDict='False', header='True'):
		'''
			Return a two dimentions list (or a list of dictionaries) which represent the content of a sheet.\n
			Indicate asDict = True to return the content as a list of Dictionary.\n
			If a two dimentions list is returned, header = True will print the column name also.
		'''
		if asDict.lower() == 'false':
			return self._data(file, sheet, False)[0] if header.lower() == 'true' else self._data(file, sheet)[0]
		else:
			data, header = self._data(file, sheet)
			return self._list_to_dict(data, header)
		
	def get_row_by_index(self, file, sheet, rowIndex=1):
		'''
			Return a list which represent data of a row by it's index in the sheet.\n
		'''
		for index, row in enumerate(self._data(file, sheet, False)[0]):
			if index + 1 == self._validate_index(rowIndex): return row
			
	def get_row_by_index_as_dict(self, file, sheet, rowIndex=1):
		'''
			Return a dictionary which represent data of a row by it's index in the sheet.\n
		'''
		return dict(zip(self._data(file, sheet)[1], self.get_row_by_index(file, sheet, int(rowIndex)+1)))
		
	def get_rows_by_reference(self, file, sheet, refColumn, refValue):
		'''
			Return a list of rows which match the search condition by index.\n
			For example: Let say the table has two rows with Name column is 'Lex':\n
			>>> Get Rows By Reference	File | Sheet | Name | Lex\n
			Result: a list of two dictionaries which represent the rows with name Lex
		'''
		listDict = self.get_sheet_content(file, sheet, 'True')
		result = []
		for r, dict in enumerate(listDict):
			if dict[refColumn] == refValue: result.append(dict.values())
		return result
	
	def get_row_by_reference(self, file, sheet, refColumn, refValue, index=1):
		'''
			Return a row which matches the search condition by index.\n
			For example: Let say the table has two rows with Name column is 'Lex':\n
			>>> Get Row By Reference	File | Sheet | Name | Lex | 2\n
			Result: the second row match the name Lex
		'''
		try: return self.get_rows_by_reference(file, sheet, refColumn, refValue)[self._validate_index(index)-1]
		except Exception as err: return None
		
	def get_row_by_reference_as_dict(self, file, sheet, refColumn, refValue, index=1):
		'''
			Return a dictionary format for a row which matches the search condition by index.\n
			For example: Let say the table has two rows with Name column is 'Lex':\n
			>>> Get Row By Reference	File | Sheet | Name | Lex | 2\n
			Result: the second row match the name Lex
		'''
		return dict(zip(self._data(file, sheet)[1], self.get_row_by_reference(file, sheet, refColumn, refValue, index)))
		
	def get_column_by_index(self, file, sheet, rowIndex=1):
		return None
		
	def get_column_by_header(self, file, sheet, refColumn, refValue):
		return None
		
	def get_cell_value_by_index(self, file, sheet, columnIndex, rowIndex):
		'''
			Return a cell value by the index of row and column in the excel file.\n
			The index starts at 1
		'''
		row = self.get_row_by_index(file, sheet, rowIndex)
		if row != None:
			for i, cell in enumerate(row):
				if i+1 == self._validate_index(columnIndex): return cell
		return None
		
	def get_cell_value_by_reference(self, file, sheet, refColumn, refValue, returnColumn, index=1):
		'''
			Return a cell value by the look up reference in the excel file.\n
			The index starts at 1
		'''
		row = self.get_row_by_reference_as_dict(file, sheet, refColumn, refValue, self._validate_index(index))
		if row != None:
			return row[returnColumn]
	
	def search_column_by_condition(self, file, sheet, column, refValue, condition):
		return None