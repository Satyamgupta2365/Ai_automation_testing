# USERS THE SCREENSHOT FUNCTION TO DEBUG THE GOOGLE SEARCH RESULTS
# This script uses Groq to query LLaMA and Selenium with undetected_chromedriver to scrape Google search results.
# It handles cookie notices, waits for elements to load, and extracts text from various parts of the page.
# It also includes error handling and debugging features like screenshots.
import os
import time
from dotenv import load_dotenv
from groq import Groq
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

uc.Chrome.__del__ = lambda self: None
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in environment. Please set it in .env file.")

groq_client = Groq(api_key=GROQ_API_KEY)

def ask_llm(query: str) -> str:
    """
    Send `query` to LLaMA (via Groq) with instructions for a concise answer,
    then truncate to the first sentence.
    """
    messages = [
        {"role": "system", "content": "Answer in one sentence."},
        {"role": "user", "content": query}
    ]
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        max_tokens=30
    )
    ans = response.choices[0].message.content.strip()
    return ans.split('. ')[0].rstrip('.') + '.'


def debug_screenshot(driver, name="debug_screenshot.png"):
    """Save a screenshot for debugging"""
    try:
        driver.save_screenshot(name)
        print(f"Saved screenshot as {name}")
    except Exception as e:
        print(f"Could not save screenshot: {e}")

def get_google_answer(query: str) -> str:
    """
    Use Selenium + undetected_chromedriver to search Google for `query` and
    return the first sentence of the top answer.
    """
    options = uc.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = None
    snippet = ""
    
    try:
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(30) 
        
        print("Navigating to Google...")
        driver.get("https://www.google.com")
        time.sleep(2)
        
        try:
            cookie_buttons = driver.find_elements(By.XPATH, 
                "//button[contains(text(), 'Accept') or contains(text(), 'Agree') or contains(text(), 'I agree')]")
            if cookie_buttons:
                cookie_buttons[0].click()
                time.sleep(1)
        except Exception as e:
            print(f"Cookie notice handling error (non-critical): {e}")
        
        print("Entering search query...")
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Search input error: {e}")
            debug_screenshot(driver, "search_error.png")
            return "Error with Google search input."
        
        print("Waiting for search results...")
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            time.sleep(5)
        except TimeoutException:
            debug_screenshot(driver, "timeout_error.png")
            return "Timeout waiting for Google results."
        
        page_source = driver.page_source
        print(f"Page source length: {len(page_source)} characters")

        debug_screenshot(driver, "search_results.png")
    
        location_selectors = [
            "//div[contains(@class, 'kp-header')]//div[contains(@class, 'xx')]",
            "//div[contains(@data-attrid, 'location')]//span",
            "//div[contains(@class, 'kp-wholepage')]//div[contains(@class, 'TrT0Xe')]",
            "//div[contains(@class, 'LrzXr kno-fv')]",
            "//span[@class='hgKElc']",
            "//div[@class='Z0LcW XcVN5d']"
        ]
        
        print("Trying location-specific selectors...")
        for selector in location_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) > 5:
                        print(f"Found with selector {selector}: {text}")
                        snippet = text
                        break
                if snippet:
                    break
            except Exception as e:
                print(f"Selector {selector} error: {str(e)}")
        
        if not snippet:
            print("Trying knowledge panel selectors...")
            try:
                knowledge_panel = driver.find_element(By.XPATH, "//div[contains(@class, 'kp-wholepage')]")
                snippet = knowledge_panel.text.split('\n')[0]
                print(f"Knowledge panel found: {snippet}")
            except Exception as e:
                print(f"Knowledge panel error: {str(e)}")
        
        if not snippet:
            print("Trying featured snippet selectors...")
            try:
                featured = driver.find_element(By.XPATH, "//div[contains(@class, 'xpdopen')]")
                snippet = featured.text.split('\n')[0]
                print(f"Featured snippet found: {snippet}")
            except Exception as e:
                print(f"Featured snippet error: {str(e)}")
        
        if not snippet:
            print("Trying regular search results...")
            try:
                results = driver.find_elements(By.XPATH, "//div[@class='g']")
                if results:
                    snippet = results[0].text.split('\n')[0]
                    print(f"Regular result found: {snippet}")
            except Exception as e:
                print(f"Regular results error: {str(e)}")
        
        if not snippet:
            print("Using fallback text extraction...")
            try:
                search_div = driver.find_element(By.ID, "search")
                all_text = search_div.text
                snippet = all_text.split('\n')[3] 
                print(f"Fallback extraction: {snippet}")
            except Exception as e:
                print(f"Fallback extraction error: {str(e)}")
                snippet = "Could not extract answer from Google."
                
    except Exception as e:
        print(f"Main error: {str(e)}")
        snippet = f"Google search error: {str(e)}"
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Driver quit error: {str(e)}")

    if snippet:
        first_sentence = snippet.split('. ')[0]
        return first_sentence.rstrip('.') + '.'
    else:
        return "No answer found on Google."

def main():
    query = input("Ask a question: ")
    
    print("\n🔄 Getting concise LLM response...")
    llm_ans = ask_llm(query)
    
    print("🔎 Searching Google...")
    google_ans = get_google_answer(query)
    
    print(f"\n🧠 LLM Answer: {llm_ans}")
    print(f"🌍 Google Answer: {google_ans}")

if __name__ == "__main__":
    main()