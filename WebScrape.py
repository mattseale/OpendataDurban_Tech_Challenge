from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
driver.get("https://valuation2022.durban.gov.za/")

# Set up WebDriverWait
wait = WebDriverWait(driver, 100)

# Switch to the frame with id "mainFrame"
wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mainFrame")))

# Function to scrape data for full title property
def scrape_full_title_data():
    # Wait for and select the appropriate option from the dropdown
    select_element = wait.until(EC.presence_of_element_located((By.ID, "drpSearchType")))
    select = Select(select_element)
    select.select_by_value("1")
    
    # Wait for and click the 'Go' button
    go_button = wait.until(EC.element_to_be_clickable((By.NAME, "btnGo")))
    go_button.click()
    
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frmSearchCriter")))

    # Wait for the new page to load
    wait.until(EC.presence_of_element_located((By.NAME, "drpVolumeNo")))
        
    # Select option 1 (Full title) from the 'drpVolumeNo' dropdown
    volume_select = Select(driver.find_element(By.NAME, "drpVolumeNo"))
    volume_select.select_by_index(1)
    
    # Wait for and click the 'Search' button
    search_button = wait.until(EC.element_to_be_clickable((By.NAME, "btnSearch")))
    search_button.click()

    driver.switch_to.default_content()
    
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mainFrame")))
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frameSearch")))
    
    # Wait for the results page to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchResultTable")))
    
    # Scrape data from the table with class 'searchResultTable'
    data = []
    iLoop = 0
    table_rows = driver.find_elements(By.XPATH, "//table[@class='searchResultTable']/tbody/tr")
    for row in table_rows:
        iLoop = iLoop + 1
        columns = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in columns])
    
    return data

# Scrape data for full title property
full_title_data = scrape_full_title_data()


# Close the browser
driver.quit()
