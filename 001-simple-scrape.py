from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://tockify.com/eventosemjoinville/agenda")

# wait 2 seconds
page.wait_for_timeout(2000)
body = page.inner_html("body")
print(body)

browser.close()
playwright.stop()
