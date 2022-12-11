from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from user_agent.base import generate_user_agent
from typing import Any, Optional

# путь до дривер
PATH_DRIVER: str = ""


def firefox_params(
        executable_path: str = PATH_DRIVER,
        profile_path: Optional[str] = None,
        generate_random_user_agent: bool = True,
        proxy: Optional[str] = None,
        private: bool = True,
        headless: bool = False,
        undetected: bool = False) -> dict[str, Any]:

    params: ... = {
        "executable_path": executable_path,
        "options": FirefoxOptions()}

    if profile_path:
        params["options"].set_preference('profile', profile_path)

    if generate_random_user_agent:
        params["options"].set_preference(
            "general.useragent.override", generate_user_agent())

    if proxy:
        params["seleniumwire_options"] = {'proxy': {
            'http': proxy, 'https': proxy,
            'no_proxy': 'localhost, 127.0.0.1:8888'}}

    params["options"].set_preference(
        "browser.privatebrowsing.autostart", private)
    params["options"].headless = headless

    if undetected:
        params["options"].set_preference("dom.webdriver.enabled", False)
        params["options"].set_preference("useAutomationExtension", False)

    params["options"].set_preference("browser.cache.disk.enable", False)
    params["options"].set_preference("browser.cache.memory.enable", False)
    params["options"].set_preference("browser.cache.offline.enable", False)
    return params


def chrome_params(
    executable_path: str = PATH_DRIVER,
    generate_random_user_agent: bool = True,
    proxy: Optional[str] = None,
    private: bool = True,
    headless: bool = False
) -> dict[str, Any]:

    params: ... = {
        "executable_path": executable_path,
        "chrome_options": ChromeOptions()
    }

    if generate_random_user_agent:
        params["chrome_options"].add_argument(
            f'user-agent={generate_user_agent()}')

    if proxy:
        params["seleniumwire_options"] = {'proxy': {
            'http': proxy, 'https': proxy,
            'no_proxy': 'localhost, 127.0.0.1:8888'}}
    if private:
        params["chrome_options"].add_argument("--incognito")

    if headless:
        params["chrome_options"].add_argument("--headless")
        params["chrome_options"].add_argument("--disable-gpu")
    return params
