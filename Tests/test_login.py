import pytest
from selenium import webdriver
from Utils.CommonActions import CommonActions
from Pages.LoginPage import LoginPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_valid_login(driver):
    actions = CommonActions(driver) 

    driver.get(LoginPage.URL)

    actions.enter_text(LoginPage.USERNAME_FIELD, "student")
    actions.enter_text(LoginPage.PASSWORD_FIELD, "Password123")
    actions.click_element(LoginPage.LOGIN_BUTTON)

    assert actions.is_element_visible(LoginPage.SUCCESS_MESSAGE) is True

def test_invalid_login(driver):
    actions = CommonActions(driver) 
    
    driver.get(LoginPage.URL)

    actions.enter_text(LoginPage.USERNAME_FIELD, "wrongUser")
    actions.enter_text(LoginPage.PASSWORD_FIELD, "wrongPass")
    actions.click_element(LoginPage.LOGIN_BUTTON)

    assert actions.is_element_visible(LoginPage.ERROR_MESSAGE) is True