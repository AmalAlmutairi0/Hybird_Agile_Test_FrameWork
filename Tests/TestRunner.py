# Hybrid_Agile_Framework/Tests/TestRunner.py
# Tests/TestRunner.py

import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from Utils.CommonActions import CommonActions
from Pages.LoginPage import LoginPage


BROWSER = os.getenv("BROWSER", "chrome").strip().lower()
HEADLESS = os.getenv("HEADLESS", "0") in ("1", "true", "yes")

DATA_FILE = Path(__file__).resolve().parents[1] / "TestData" / "LoginData.csv"
REPORT_DIR = Path(__file__).resolve().parents[1] / "results"
REPORT_DIR.mkdir(exist_ok=True)


def _build_driver():
    if BROWSER == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions

        options = FirefoxOptions()
        if HEADLESS:
            options.add_argument("-headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    elif BROWSER == "edge":
        from selenium.webdriver.edge.options import Options as EdgeOptions

        options = EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    from selenium.webdriver.chrome.options import Options as ChromeOptions

    options = ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _determine_actual_result(actions: CommonActions, login: LoginPage) -> str:
    if actions.is_element_visible(LoginPage.SUCCESS_MESSAGE):
        return "Success"
    return "Failure"


def run_hybrid_tests() -> pd.DataFrame:
    print("--- Starting Hybrid Test Automation ---")
    print(f"Using browser: {BROWSER} | headless={HEADLESS}")
    print(f"Reading data from: {DATA_FILE}")

    test_data = pd.read_csv(DATA_FILE)

    results = []
    driver = _build_driver()
    driver.maximize_window()
    driver.get(LoginPage.URL)

    login_page = LoginPage(driver)
    actions = CommonActions(driver)

    for index, row in test_data.iterrows():
        start_time = time.time()

        current_username = "" if pd.isna(row.get("Username")) else str(row["Username"])
        current_password = "" if pd.isna(row.get("Password")) else str(row["Password"])
        expected = "" if pd.isna(row.get("Expected_Result")) else str(row["Expected_Result"])

        actions.enter_text(LoginPage.USERNAME_FIELD, current_username)
        actions.enter_text(LoginPage.PASSWORD_FIELD, current_password)
        actions.click_element(LoginPage.LOGIN_BUTTON)

        actual = _determine_actual_result(actions, login_page)

        duration = time.time() - start_time

        if actual == "Success":
            driver.get(LoginPage.URL)

        results.append(
            {
                "Scenario": f"Test {index + 1}",
                "Username": current_username,
                "Expected": expected,
                "Actual_Result": actual,
                "Match": "PASS" if actual == expected else "FAIL",
                "Duration (s)": round(duration, 2),
            }
        )

    results_df = pd.DataFrame(results)

    pass_rate = (results_df["Match"] == "PASS").mean() if not results_df.empty else 0.0
    avg_duration = results_df["Duration (s)"].mean() if not results_df.empty else 0.0

    print("\n--- Final Hybrid Framework Results ---")
    try:
        from tabulate import tabulate

        print(tabulate(results_df, headers="keys", tablefmt="grid", showindex=False))
    except Exception:
        print(results_df.to_string(index=False))

    print(f"\nPass rate: {pass_rate:.1%} | Avg duration: {avg_duration:.2f}s")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = REPORT_DIR / f"results_{BROWSER}_{stamp}.csv"
    html_path = REPORT_DIR / f"results_{BROWSER}_{stamp}.html"

    results_df.to_csv(csv_path, index=False)
    results_df.to_html(html_path, index=False)

    print(f"\nSaved CSV → {csv_path}")
    print(f"Saved HTML → {html_path}")

    driver.quit()
    return results_df


if __name__ == "__main__":
    run_hybrid_tests()