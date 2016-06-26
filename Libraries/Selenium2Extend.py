from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
	Extend the Selenium2Library with customized methods for checking element state (it is check, not assert)
	Require:
		- Selenium2Library (pip install robotframework-selenium2library)
	How to use:
		- Import as custom library
		- Call method on current focused WebDriver (browser) of Selenium2Library
	
	Version: 1.0
'''

class myElement(object):
	def __init__(self, locator):
		address = str(locator).split('=', 1)
		self._elem = address[0], address[1]	#By.class, value
		self._validate_locator()
		
	def _validate_locator(self):
		if not By.is_valid(self._elem[0]): raise Exception('ERROR: Wrong definion of locator: ' + self._elem[0] + '=' + self._elem[1])
	
	def _myElem(self): return self._elem

def _driver(): return BuiltIn().get_library_instance('Selenium2Library')._current_browser()
def _timeOut(s): return 0 if int(s) < 0 else int(s)
def _wait(s): return WebDriverWait(_driver(), _timeOut(s))

##################### Verify element conditions ##################
##################################################################

def is_element_visible(locator, timeOut=0):
	'''
		An expectation for checking that an element is present on the DOM of a page and visible.\n
		Visibility means that the element is not only displayed but also has a height and width that is greater than 0.\n
		Locator - used to find the element returns True once it is located and visible
	'''
	logger.debug('Check if element ' + locator + ' is visible for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.visibility_of_element_located(myElement(locator)._myElem()))
	except Exception: return False
	return True
	
def does_element_exists(locator, timeOut=0):
	'''
		An expectation for checking that an element is present on the DOM of a page.\n
		This does not necessarily mean that the element is visible.\n
		Locator - used to find the element returns True once it is located
	'''
	logger.debug('Check if element ' + locator + ' exists for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.presence_of_element_located(myElement(locator)._myElem()))
	except Exception: return False
	return True

def is_element_clickable(locator, timeOut=0):
	'''
		An Expectation for checking an element is visible and enabled such that you can click it.
	'''
	logger.debug('Check if element ' + locator + ' is enabled for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.element_to_be_clickable(myElement(locator)._myElem()))
	except Exception: return False
	return True

def is_element_invisible(locator, timeOut=0):
	'''
		An Expectation for checking that an element is either invisible or not present on the DOM.\n
		Locator used to find the element
	'''
	logger.debug('Check if element ' + locator + ' is invisible for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.invisibility_of_element_located(myElement(locator)._myElem()))
	except Exception: return False
	return True

def is_element_selected(locator, timeOut=0):
	'''
		An expectation for the element to be located is selected
	'''
	logger.debug('Check if element ' + locator + ' is invisible for ' + str(_timeOut(timeOut)) + ' seconds')
	try: return _wait(timeOut).until(EC.element_located_to_be_selected(myElement(locator)._myElem()))
	except Exception: return False

def is_text_present_in_element(locator, text, timeOut=0):
	'''
		An expectation for checking if the given text is present in the specified element\n
	'''
	logger.debug('Check if a text is present in element ' + locator + ' for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.text_to_be_present_in_element_value(myElement(locator)._myElem(), text))
	except Exception: return False
	return True

def is_alert_present(timeOut=0):
	'''
		Expect an alert to be present.\n
	'''
	logger.debug('Check if an alert is present for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.alert_is_present())
	except Exception: return False
	return True

def is_frame_available(locator, timeOut=0):
	'''
		An expectation for checking whether the given frame is available to switch to.\n
		If the frame is available it switches the given driver to the specified frame
	'''
	logger.debug('Check if the frame ' + locator + ' is available to switch to it for ' + str(_timeOut(timeOut)) + ' seconds')
	try: _wait(timeOut).until(EC.frame_to_be_available_and_switch_to_it(myElement(locator)._myElem()))
	except Exception: return False
	return True

def is_title_equals(text, timeOut=0):
	'''
		An expectation for checking that the title contains a case-sensitive substring. \n
		Title is the fragment of title expected returns True when the title matches, False otherwise
	'''
	logger.debug('Check if the page title equals to: "' + text + '" for ' + str(_timeOut(timeOut)) + ' seconds')
	return _wait(timeOut).until(EC.title_is(text))
	
def is_title_contains(text, timeOut=0):
	'''
		An expectation for checking the title of a page.\n
		Title is the expected title, which must be an exact match returns True if the title matches, false otherwise.
	'''
	logger.debug('Check if the page title contains case-sensitive substring: "' + text + '" for ' + str(_timeOut(timeOut)) + ' seconds')
	return _wait(timeOut).until(EC.title_contains(text))