import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ['PATH'] += r"D:\Seleniumdrivers"
driver = webdriver.Chrome()

# Provided data
license_data = [
    {"Licensee Name": "WILLOWCREEK GROUP INC", "Address Line 1": "PO BOX 160215", "City": "ALTAMONTE SPRINGS", "State": "FL"},
    {"Licensee Name": "CORNERSTONE HOMES LLC", "Address Line 1": "5632 ORTEGA PARK BLVD", "City": "JACKSONVILLE", "State": "FL"},
    {"Licensee Name": "BUILDING CONCEPTS OF TAMPA BAY, LLC", "Address Line 1": "6635 GLENCOE DRIVE", "City": "TAMPA", "State": "FL"},
    {"Licensee Name": "GKE, LLC", "Address Line 1": "3631 SE 12TH PLACE", "City": "OCALA", "State": "FL"},
    {"Licensee Name": "EVERETTE WHITEHEAD & SON INC", "Address Line 1": "601-6TH S W STREET", "City": "WINTER HAVEN", "State": "FL"}
]

# Create a CSV file
csv_file_path = 'extracted_data.csv'
header = ["Licensee Name", "Phone", "Address", "Email", "Website"]

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    for data in license_data:
        driver.get("https://www.yellowpages.com/")

        # Locate search and location bars
        search_bar = driver.find_element(By.ID, 'query')
        location_bar = driver.find_element(By.ID, 'location')

        # Enter search criteria
        search_bar.send_keys(data["Licensee Name"])
        location_bar.clear()
        location_bar.send_keys(data["State"])
        location_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        wait = WebDriverWait(driver, 10)

        try:
            businesses = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//h2[@class='n']//a[@class='business-name']")))
        except:
            print(f"No information found for {data['Licensee Name']}. Moving to the next entry.")
            csv_writer.writerow([data["Licensee Name"], pd.NaT, pd.NaT, pd.NaT, pd.NaT])
            continue

        # Check if there are any businesses listed
        if businesses:
            # Click on the first business link
            first_business = businesses[0]
            first_business_name = first_business.text
            print(f"Clicking on the link for the first business ({data['Licensee Name']}): {first_business_name}")
            first_business.click()

            # Wait for the business details to load
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'business-card')))

            # Extract information from the business page
            try:
                business_name = driver.find_element(By.CLASS_NAME, 'business-name').text
                phone = driver.find_element(By.CLASS_NAME, 'phone').text
                address = driver.find_element(By.CLASS_NAME, 'address').text
                email = driver.find_element(By.CLASS_NAME, 'email-business').get_attribute('href')
                website = driver.find_element(By.CLASS_NAME, 'other-links').get_attribute('href')

                # Write extracted information to CSV
                csv_writer.writerow([business_name, phone, address, email, website])
                print("Licensee Name:", business_name)
                print("Phone:", phone)
                print("Address:", address)
                print("Email:", email)
                print("Website:", website)
            except:
                print(f"Information extraction failed for {data['Licensee Name']}.")

        # Go back to the search results page for the next iteration
        driver.back()

# Close the browser
driver.quit()
