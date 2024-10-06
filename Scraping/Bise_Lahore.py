import pandas as pd
import os
import sys
from time import sleep
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Scraping_Utils import search_result, scrape_data, driver, url

start = 565246

for rollno in range(start, start + 2):
    if not search_result(rollno):
        print(f"Skipping roll number {rollno} due to search error.")
        continue
    row = scrape_data(rollno)
    if row:
        df = pd.DataFrame([row], columns=[  
            "Roll Number", "Name", "CNIC", "Urdu Marks", "English Marks", "Islamiat Marks", 
            "Pak Study Marks", "Physics Marks", "Chemistry Marks", "Mathematics Marks", "Total Marks"
        ])
        
        df.to_csv("Scraping/biselahore_results.csv", mode='a', header=not os.path.isfile("Scraping/biselahore_results.csv"), index=False, encoding="utf-8")
    driver.get(url)
    sleep(1)

driver.quit()