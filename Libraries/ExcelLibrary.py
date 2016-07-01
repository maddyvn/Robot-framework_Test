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
		try:
			if int(i) < 1: raise Exception('Wrong index number provided. Should >= 1')
		except Exception as err: raise Exception('Wrong index number providedaa. Should >= 1' + err)
		return i
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

# Public function
	def get_sheet_content_in_list(self, file, sheet, header='True'):
		'''
			Return a two dimentions list which represent the content of a sheet.\n
			Use action "log list" to print the list as table view
		'''
		return self._data(file, sheet, False)[0] if header.lower() == 'true' else self._data(file, sheet)[0]

	def get_sheet_content_in_dict(self, file, sheet):
		'''
			Return a list of dictionary which represent the content of a sheet.\n
			Use action "log list" to print the list under dictionary format
		'''
		data, header = self._data(file, sheet)
		return [dict(zip(header, map(str, row))) for row in data]
		
	def get_row_by_index(self, file, sheet, rowIndex=1):
		'''
			Return a list which represent data of a row by row index in the sheet.\n
		'''
		for index, row in enumerate(self._data(file, sheet, False)[0]):
			if index == self._validate_index(rowIndex)-1: return row
		
	def get_rows_by_reference(self, file, sheet, refColumn, refValue):
		listDict = self.get_sheet_content_in_dict(file, sheet)
		result = []
		for r, dict in enumerate(listDict):
			if dict[refColumn] == refValue: result.append(dict.values())
		return result
	
	def get_row_by_reference(self, file, sheet, refColumn, refValue, index=1):
		try: return self.get_rows_by_reference(file, sheet, refColumn, refValue)[self._validate_index(index)-1]
		except Exception as err: return None
		
	def get_column_by_index(self, file, sheet, rowIndex=1):
		return None
		
	def get_column_by_header(self, file, sheet, refColumn, refValue):
		return None
		
	def get_cell_value_by_index(self, file, sheet, columnIndex=1, rowIndex=1):
		return None
		
	def get_cell_value_by_reference(self, file, sheet, refColumn, refValue, returnColumn):
		return None
	
	def search_column_by_condition(self, file, sheet, column, refValue, condition):
		return None