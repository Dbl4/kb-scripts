import json
import time

from selenium import (
    webdriver,
)
from selenium_stealth import (
    stealth,
)


options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = 'https://chizhik.club/catalog/maslo-sousy-spetsii'
driver.get(url)


# time.sleep(5)
driver.quit()