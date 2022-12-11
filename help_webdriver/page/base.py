import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.remote.webdriver import WebDriver


class WebPage(object):
    def __init__(self, web_driver: WebDriver):
        self._web_driver = web_driver

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self.__getattribute__(name)._set_value(self._web_driver, value)
        else:
            super(WebPage, self).__setattr__(name, value)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)
        if not item.startswith('_') and not callable(attr):
            try:
                attr._web_driver = self._web_driver
                attr._page = self
            except:
                return attr
        return attr

    def get(self, url: str, waid_loaded: int = 2):
        """ Прокрутите страницу до элемента. """
        self._web_driver.get(url)
        if waid_loaded:
            self.wait_page_loaded(sleep_time=waid_loaded)

    def go_back(self, waid_loaded: int = None):
        """ Назад. """
        self._web_driver.back()
        if waid_loaded:
            self.wait_page_loaded(sleep_time=waid_loaded)

    def refresh(self, waid_loaded: int = None):
        """ Перезагрузка. """
        self._web_driver.refresh()
        if waid_loaded:
            self.wait_page_loaded(sleep_time=waid_loaded)

    def get_current_url(self):
        """ Текущий Url. """
        return self._web_driver.current_url

    def screenshot(self, file_name: str = 'screenshot.png'):
        """ Скриншот всей страницы. """
        self._web_driver.save_screenshot(file_name)

    def scroll(self, up_down: str = '', offset: int = 0):
        """ Прокрутка вверх вниз. """
        if offset:
            self._web_driver.execute_script(
                f'window.scrollTo(0, {up_down}{offset});')
        else:
            self._web_driver.execute_script(
                f'window.scrollTo(0, {up_down}document.body.scrollHeight);')

    def switch_to_iframe(self, iframe):
        """ Переключиться на фрейм по его имени """
        self._web_driver.switch_to.frame(iframe)

    def switch_out_iframe(self):
        """ Выйти из фрейма. """
        self._web_driver.switch_to.default_content()

    def get_page_source(self):
        """ Возращает теги текущей страницы. """
        try:
            return self._web_driver.page_source
        except:
            return None

    def wait_page_loaded(self, timeout=60, check_js_complete=True,
                         check_page_changes=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear='',
                         sleep_time=2):
        """ Эта функция ждет, пока страница не загрузится полностью.
            Мы используем много разных способов определить, загружена ли страница или нет:
            1) Проверить статус JS
            2) Проверить модификацию в исходном коде страницы
            3) Убедитесь, что ожидаемые элементы, представленные на странице
        """
        page_loaded = False
        if sleep_time:
            time.sleep(sleep_time)

        try:
            source = self._web_driver.page_source
        except:
            source = ''
        while not page_loaded and timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5
            if check_js_complete:
                try:
                    self._web_driver.execute_script(
                        'window.scrollTo(0, document.body.scrollHeight);')
                    page_loaded = self._web_driver.execute_script(
                        "return document.readyState == 'complete';")
                except Exception as e:
                    pass

            if page_loaded and check_page_changes:
                try:
                    new_source = self._web_driver.page_source
                    check_page_changes = False
                except:
                    new_source = ''
                page_loaded = new_source == source
                source = new_source

            if page_loaded and wait_for_xpath_to_disappear:
                try:
                    WebDriverWait(self._web_driver, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, wait_for_xpath_to_disappear)))
                    wait_for_xpath_to_disappear = False
                except:
                    pass

            if page_loaded and wait_for_element:
                try:
                    WebDriverWait(self._web_driver, 0.1).until(
                        EC.element_to_be_clickable(wait_for_element._locator))
                    wait_for_element = False
                except:
                    pass
        self._web_driver.execute_script(
            'window.scrollTo(document.body.scrollHeight, 0);')
        return page_loaded

    def switch_to_window(self, handless: int = -1):
        """ Переход между вкладками """
        self._web_driver.switch_to.window(
            self._web_driver.window_handles[handless])

    def add_cookies(self, cookies):
        """ Вставка куки """
        for cookie in cookies:
            self._web_driver.add_cookie(cookie)
        self.refresh()

    def window_size(self, x: int = 900, y: int = 788):
        """ Размеры окна """
        self._web_driver.set_window_size(x, y)
