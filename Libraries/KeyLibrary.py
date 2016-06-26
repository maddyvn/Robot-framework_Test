from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

'''
	Library to work with keyboard input for robot-framework
	Refer: https://seleniumhq.github.io/selenium/docs/api/py/_modules/selenium/webdriver/common/keys.html#Keys
'''

class KeyLibrary(object):
	def _driver(self): return BuiltIn().get_library_instance('Selenium2Library')._current_browser()
	def _action(self): return ActionChains(self._driver())
	def _element(self, locator):
		s = str(locator).split('=', 1)
		return self._driver().find_element(s[0], s[1])
	
	# Focus to the element
	def _focus(self, locator):
		self._driver().execute_script("arguments[0].focus();", self._element(locator))
		
	def key_input(self, key, locator=None):
		'''
			Sends keys to element. If no element is specified then send key to focused element
		'''
		if locator != None: self._focus(locator)
		self._action().send_keys(key).perform()
		
	def key_paste(self, locator=None):
		'''
			Perform Ctrl + V to paste a clipboard value. If no element is specified then execute on focused element
		'''
		if locator != None: self._focus(locator)
		self._action().key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	
	def key_select_all(self, locator=None):
		'''
			Perform Ctrl + A to select all text of an element. If no element is specified then execute on focused element
		'''
		if locator != None: self._focus(locator)
		self._action().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
