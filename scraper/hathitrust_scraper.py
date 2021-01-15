from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.set_headless()
assert opts.headless
browser = Chrome(options=opts)
browser.get('https://www.google.com/')
browser.quit()