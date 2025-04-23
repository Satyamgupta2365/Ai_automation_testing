import undetected_chromedriver as uc 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

driver.get("https://www.google.com")
search_box = driver.find_element(By.NAME, "q")

search_box.clear()
search_box.send_keys("Who is the PM of India")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

if "Modi" in driver.page_source:
    print("The current Prime Minister of India is Narendra Modi.")
else:
    print("The current Prime Minister of India is not Narendra Modi.")
driver.quit()

