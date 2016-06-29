from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

'''
	Extend the Selenium2Library with customized methods for checking element state (it is check, not assert)
	Require:
		- Selenium2Library (pip install robotframework-selenium2library)
	How to use:
		- Import as custom library
		- Call method on current focused WebDriver (browser) of Selenium2Library
	
	Version: 1.0
'''

class Element(object):
	def __init__(self, locator):
		self._validate(locator)
		
	def _validate(self, locator):
		s = str(locator).split('=', 1)
		if s[0] not in ['id','name','xpath','tag name','partial link text','link text','css selector','class name']:
			raise ValueError('Wrong identifier definion of locator: ' + s[0] + '=' + s[1])
		self._elem = s[0], s[1]	#By.class, value
	
	def _get(self): return self._elem

def _driver(): return BuiltIn().get_library_instance('Selenium2Library')._current_browser()
def _cache(): return BuiltIn().get_library_instance('Selenium2Library')._cache
def _action(): return ActionChains(_driver())
def _timeOut(s): return 0 if int(s) < 0 else int(s)
def _wait(s): return WebDriverWait(_driver(), _timeOut(s))
def _findElem(locator):
	elem = Element(locator)._get()
	return _driver().find_element(elem[0],elem[1])

##################### Verify element conditions ##################
##################################################################

def does_element_exists(locator, timeOut=0):
	'''
		Checking that an element is present on the DOM of a page.\n
		This does not necessarily mean that the element is visible.\n
		Locator - used to find the element returns True once it is located
	'''
	try: _findElem(locator)
	except WebDriverException: return False
	return True

def is_element_visible(locator, timeOut=0):
	'''
		Checking that an element is present on the DOM of a page and visible.\n
		Visibility means that the element is not only displayed but also has a height and width that is greater than 0.\n
		Locator - used to find the element returns True once it is located and visible
	'''
	try: _wait(timeOut).until(EC.visibility_of_element_located(Element(locator)._get()))
	except WebDriverException: return False
	return True

def is_element_invisible(locator, timeOut=0):
	'''
		Checking that an element is either invisible or not present on the DOM.\n
		Locator used to find the element
	'''
	try: _wait(timeOut).until(EC.invisibility_of_element_located(Element(locator)._get()))
	except WebDriverException: return False
	return True

def is_element_clickable(locator, timeOut=0):
	'''
		Checking an element is visible and enabled such that you can click it.
	'''
	try: _wait(timeOut).until(EC.element_to_be_clickable(Element(locator)._get()))
	except WebDriverException: return False
	return True

def is_element_selected(locator, timeOut=0):
	'''
		Check whether the element to be located is selected
	'''
	try: return _wait(timeOut).until(EC.element_located_to_be_selected(Element(locator)._get()))
	except WebDriverException: return False

def is_text_present_in_element(locator, text, timeOut=0):
	'''
		Checking if the given text is present in the specified element\n
	'''
	try: _wait(timeOut).until(EC.text_to_be_present_in_element_value(Element(locator)._get(), text))
	except WebDriverException: return False
	return True

def is_alert_present(timeOut=0):
	'''
		Check whether an alert to be present.\n
	'''
	try: _wait(timeOut).until(EC.alert_is_present())
	except WebDriverException: return False
	return True

def is_frame_available(locator, timeOut=0):
	'''
		Checking whether the given frame is available to switch to.\n
		If the frame is available it switches the given driver to the specified frame
	'''
	try: _wait(timeOut).until(EC.frame_to_be_available_and_switch_to_it(Element(locator)._get()))
	except WebDriverException: return False
	return True

def is_title_equals(text, timeOut=0):
	'''
		An expectation for checking that the title contains a case-sensitive substring. \n
		Title is the fragment of title expected returns True when the title matches, False otherwise
	'''
	return _wait(timeOut).until(EC.title_is(text))
	
def is_title_contains(text, timeOut=0):
	'''
		Checking the title of a page.\n
		Title is the expected title, which must be an exact match returns True if the title matches, false otherwise.
	'''
	return _wait(timeOut).until(EC.title_contains(text))

def get_opened_browsers():
	'''
		Return all opened browser instances in a list
	'''
	return _cache().get_open_browsers()
	
def get_closed_browsers():
	'''
		Return all closed browser instances in a list
	'''
	return _cache()._closed
	
def get_focused_browser():
	'''
		Return the current focused browser instance
	'''
	return _cache().current

def get_focused_browser_alias():
	'''
		Return the current focused browser alias. If no browsers or focused browser does not has alias return None
	'''
	cur = get_focused_browser()
	for i, b in enumerate(get_opened_browsers()):
		if cur == b:
			try: return _cache()._aliases._data.keys()[_cache()._aliases._data.values().index(i+1)]
			except Exception: return None
	
def is_browser_opened(alias_or_index=None):
	'''
		Check whether the browser exists or not by non-casesensitive registered alias or index\n
		If no index or alias is used, if at least 1 instance of WebDriver is opened will return true
	'''
	if alias_or_index == None:
		return True if len(get_opened_browsers()) > 0 else False
		
	try: browser = _cache().get_connection(alias_or_index.lower())
	except RuntimeError: return False
	
	for i, b in enumerate(get_opened_browsers()):
		if browser == b: return True
	return False
	
def close_browser_by_alias(alias_or_index):
	'''
		Switch then close an opening browser with the expected alias or index. Do nothing if no browsers are found with the expected alias\n
		Return True/False for successfully/fail close action
	'''
	if is_browser_opened(alias_or_index):
		try:
			_cache().switch(alias_or_index.lower())
			_cache().close()
			return True
		except Exception: raise Exception('Failed to close browser instance by runtime error.')
	else:
		print('Skip due to found no browsers with the alias: \'' + str(alias_or_index) + '\' to close')
		return False
	
def move_to_element(locator):
	'''
		Focus to the element by locator.
	'''
	_findElem(locator).send_keys(Keys.NULL)

##################### Keyboard input ##################
#######################################################
		
def key_input(key, locator=None):
	'''
		Sends keys to element. If no element is specified then send key to focused element
	'''
	if locator != None: move_to_element(locator)
	_action().send_keys(key).perform()
		
def key_paste(locator=None):
	'''
		Perform Ctrl + V to paste from a clipboard value. If no element is specified then execute on focused element
	'''
	if locator != None: move_to_element(locator)
	_action().key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	
def key_select_all(locator=None):
	'''
		Perform Ctrl + A to select all content of focused element. If no element is specified then execute on focused area
	'''
	if locator != None: move_to_element(locator)
	_action().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
	
def key_copy(locator=None):
	'''
		Perform Ctrl + C to copy selected content of an element. If no element is specified then execute on focused element
	'''
	if locator != None: move_to_element(locator)
	_action().key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()