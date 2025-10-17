from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def run_traditional_test():
    start_time = time.time()
    driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()))
    driver.get("https://practicetestautomation.com/practice-test-login/")
    
    driver.find_element(By.ID, "username").send_keys("student")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()
    
    try:
        driver.find_element(By.LINK_TEXT, "Log out")
    except:
        pass

    driver.quit()
    end_time = time.time()
    
    print(f"\nTraditional Test Time (Single Run): {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    run_traditional_test()