from PIL import Image

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, List


class WebElements(WebElement):
    def __init__(self, by: By, value: str):
        self.locator = (by, value,)

    def wait_find(self, timeout_wait: int | float = 10) -> WebElement:
        """ Поиск элемента. """
        return WebDriverWait(self._web_driver, timeout_wait).until(
            EC.presence_of_element_located(self.locator))

    def wait_find_all(self, timeout_wait: int | float = 10) -> List[WebElement] | List:
        """ Поиск элементов. """
        return WebDriverWait(self._web_driver, timeout_wait).until(
            EC.presence_of_all_elements_located(self.locator))

    def wait_to_be_clickable(self, timeout_wait: int | float) -> WebElement | None:
        """" Подождёт пока элемент не станет виден и проверит можно ли на него нажать"""
        return WebDriverWait(self._web_driver, timeout_wait).until(
            EC.element_to_be_clickable(self.locator))

    def wait_to_be_element_visible(self, timeout_wait: int | float):
        return WebDriverWait(self._web_driver, timeout_wait).until(
            EC.visibility_of_element_located(self.locator))

    def more_send_keys(self, send_text: Tuple[str | Keys], timeout_wait: int | float, click: bool = False, clear: bool = False) -> None:
        if elem := self.wait_find(timeout_wait=timeout_wait):
            if click:
                elem.click()
            if clear:
                elem.clear()
            elem.send_keys(*send_text)

    def human_click(self, timeout_wait: int | float, hold_seconds: int | float = 0,
                    x_offset: int | float = 1, y_offset: int | float = 1) -> None:
        """ Человеческое нажатие. """
        if elem := self.wait_find(timeout_wait=timeout_wait):
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(elem, x_offset, y_offset).\
                pause(hold_seconds).click(on_element=elem).perform()

    def click(self, search_timeout: int | float = 3):
        """ Нажатие """
        if elem := self.wait_find(timeout_wait=search_timeout):
            elem.click()

    def screenshot_elements(self, timeout_wait: int | float, filename: str):
        """ Скриншот веб элемента """
        if elem := self.wait_find(timeout_wait=timeout_wait):
            self._web_driver.save_screenshot(filename)
            fullImg = Image.open(filename)
            fullImg.crop((
                *elem.location_once_scrolled_into_view.values(),
                *elem.size.values())) .save(filename)

    def scroll_to_element(self, timeout_wait: int | float):
        """ Прокрутите страницу до элемента. """
        if elem := self.wait_find(timeout_wait=timeout_wait):
            self._web_driver.execute_script(
                "arguments[0].scrollIntoView();", elem)

    def delete(self, timeout_wait: int):
        """ Удаляет элемент со страницы. """
        if elem := self.wait_find(timeout_wait=timeout_wait):
            self._web_driver.execute_script("arguments[0].remove();", elem)
