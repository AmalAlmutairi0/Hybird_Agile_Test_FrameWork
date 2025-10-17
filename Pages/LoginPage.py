from selenium.webdriver.common.by import By

class LoginPage:
    URL = "https://practicetestautomation.com/practice-test-login/"

    USERNAME_FIELD = (By.ID, "username")       
    PASSWORD_FIELD = (By.ID, "password")     
    LOGIN_BUTTON = (By.ID, "submit")
    
    SUCCESS_MESSAGE = (By.LINK_TEXT, "Log out") 
    ERROR_MESSAGE = (By.ID, "error") 

    def __init__(self, driver):
        self.driver = driver