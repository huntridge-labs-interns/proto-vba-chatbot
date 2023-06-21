#%%
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.errorhandler import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

### ---------------------------------------------------------------------------------------------------------
### ---------------------------------------------------------------------------------------------------------
### ---------------------------------------------------------------------------------------------------------

########################################### ONE CHAPTER SCRAP ########################################### 

# %%
# Set up the Selenium Chrome driver
#options = Options()
#options.add_argument("--headless")  # Run the browser in headless mode
# Replace with the actual path to chromedriver executable
#driver = webdriver.Chrome((ChromeDriverManager().install()), options=options)

# Open the URL
#url = "https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000144554/M28CIVB1-Evaluation-Process%3FarticleViewContext=article_view_related_article"
#driver.get(url)

# Find the relevant elements on the page
#title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
#title = title_element.text.strip()

#hr_elements = driver.find_elements(By.CSS_SELECTOR, 'hr')
#headings = []
#content = []
#tokens_count = []
#if len(hr_elements) >= 2:
 #   start_hr = hr_elements[1]
  #  elements_between_headings = start_hr.find_elements(By.XPATH, './following-sibling::*[self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::p or self::ul]')
    
   # heading = None
    #content_text = ""
    
    #for element in elements_between_headings:
     #   if element.tag_name.startswith("h"):
      #      if re.match(r"\d+\.\d+ ", element.text.strip()):  # Check if the heading starts with a number followed by a period
                # Save the previous heading and content
       #         if heading and content_text:
        #            headings.append(heading.text.strip())
         #           content.append(content_text.strip())
          #          tokens_count.append(len(content_text.strip().split()))
                
                # Start a new heading
           #     heading = element
            #    content_text = ""
            #else:
                # Append the subheading text to the content
             #   content_text += element.text.strip() + " "
        #else:
            # Append the element's text to the content
         #   content_text += element.text.strip() + " "
    
    # Save the last heading and content
    #if heading and content_text:
     #   headings.append(heading.text.strip())
      #  content.append(content_text.strip())
       # tokens_count.append(len(content_text.strip().split()))

#Quit the driver
#driver.quit()

# Create a Pandas DataFrame
#data = {'Title': title, 'Heading': headings, 'Content': content, 'Tokens': tokens_count}
#df = pd.DataFrame(data)
# Print the DataFrame
#print("Title:", title)
#print(df)


########################################### DATA SCRAPPING THROUGH ALL CHAPTERS ########################################### 
#%% 
# Set up the Selenium Chrome driver
options = Options()
# options.add_argument("--headless")  # Run the browser in headless mode
driver = webdriver.Chrome((ChromeDriverManager().install()), options=options)

# Open the URL
url = "https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000146267/M28CIA1-Veteran-Readiness-and-Employment-Manual%3FarticleViewContext=article_view_related_article"
driver.get(url)

chapter_titles = []
headings = []
content = []
tokens_count = []

while True:
    try:
        # Find the relevant elements on the page
        title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
        chapter_title = title_element.text.strip()

        hr_elements = driver.find_elements(By.CSS_SELECTOR, 'hr')

        if len(hr_elements) >= 2:
            start_hr = hr_elements[1]
            elements_between_headings = start_hr.find_elements(By.XPATH, './following-sibling::*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::p or self::ul]')

            heading = None
            content_text = ""

            for element in elements_between_headings:
                if element.tag_name.startswith("h") or element.tag_name == "p":
                    if re.match(r"\d+\.\d+|\d+\.\d+\.\d+ ", element.text.strip()) and element.text.strip() != "1.01 Chapter and Paragraph":
                        # Save the previous heading and content
                        if heading and content_text:
                            if len(content_text) <= 32000:
                                headings.append(heading.text.strip())
                                content.append(content_text.strip())
                                tokens_count.append(len(content_text.strip().split()))
                                chapter_titles.append(chapter_title)  # Append the chapter title here
                            else:
                                split_index = content_text.rfind(" ", 0, 32000)  # Find the last space before the character limit
                                content_part1 = content_text[:split_index].strip()
                                content_part2 = content_text[split_index:].strip()
                                headings.append(heading.text.strip())
                                content.append(content_part1)
                                tokens_count.append(len(content_part1.split()))
                                chapter_titles.append(chapter_title)  # Append the chapter title here
                                headings.append(heading.text.strip())
                                content.append(content_part2)
                                tokens_count.append(len(content_part2.split()))
                                chapter_titles.append(chapter_title)  # Append the chapter title here

                        # Start a new heading
                        heading = element
                        content_text = ""
                    else:
                        # Append the subheading text to the content
                        content_text += element.text.strip() + " "
                else:
                    # Append the element's text to the content
                    content_text += element.text.strip() + " "

            # Save the last heading and content
            if heading and content_text:
                if len(content_text) <= 32000:
                    headings.append(heading.text.strip())
                    content.append(content_text.strip())
                    tokens_count.append(len(content_text.strip().split()))
                    chapter_titles.append(chapter_title)  # Append the chapter title here
                else:
                    split_index = content_text.rfind(" ", 0, 32000)  # Find the last space before the character limit
                    content_part1 = content_text[:split_index].strip()
                    content_part2 = content_text[split_index:].strip()
                    headings.append(heading.text.strip())
                    content.append(content_part1)
                    tokens_count.append(len(content_part1.split()))
                    chapter_titles.append(chapter_title)  # Append the chapter title here
                    headings.append(heading.text.strip())
                    content.append(content_part2)
                    tokens_count.append(len(content_part2.split()))
                    chapter_titles.append(chapter_title)  # Append the chapter title here

        try:
            next_chapter_button = driver.find_element(By.LINK_TEXT, 'Next Chapter')
            if not next_chapter_button.is_enabled():
                break
            next_chapter_button.click()

            # Wait for the page to load
            time.sleep(3)
        except NoSuchElementException:
            break

    except StaleElementReferenceException:
        # Re-find the elements after the exception occurs
        continue

# Quit the driver
driver.quit()

# Create a Pandas DataFrame
data = {'Chapter Title': chapter_titles, 'Heading': headings, 'Content': content, 'Tokens': tokens_count}
df = pd.DataFrame(data)
print(df)

########################################### CSV OUTPUT ##################################################### 
# %%
df.to_csv('M28C_Scrap.csv', index=False)

########################################## DATA SCRAP THROUGH ALL CHAPTERS LIMITING TOKENS ######################################################################
# %%
# Set up the Selenium Chrome driver
options = Options()
# options.add_argument("--headless")  # Run the browser in headless mode
driver = webdriver.Chrome((ChromeDriverManager().install()), options=options)

# Open the URL
url = "https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000146267/M28CIA1-Veteran-Readiness-and-Employment-Manual%3FarticleViewContext=article_view_related_article"
driver.get(url)

chapter_titles = []
headings = []
content = []
tokens_count = []

while True:
    try:
        # Find the relevant elements on the page
        title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
        chapter_title = title_element.text.strip()

        hr_elements = driver.find_elements(By.CSS_SELECTOR, 'hr')

        if len(hr_elements) >= 2:
            start_hr = hr_elements[1]
            elements_between_headings = start_hr.find_elements(By.XPATH, './following-sibling::*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::p or self::ul]')

            heading = None
            content_text = ""

            for element in elements_between_headings:
                if element.tag_name.startswith("h") or element.tag_name == "p":
                    if re.match(r"\d+\.\d+|\d+\.\d+\.\d+ ", element.text.strip()) and element.text.strip() != "1.01 Chapter and Paragraph":
                        # Save the previous heading and content
                        if heading and content_text:
                            if len(content_text) <= 3500:
                                headings.append(heading.text.strip())
                                content.append(content_text.strip())
                                tokens_count.append(len(content_text.strip().split()))
                                chapter_titles.append(chapter_title)  # Append the chapter title here
                            else:
                                # Split the content into multiple rows at the nearest word to 3500 tokens
                                words = content_text.strip().split()
                                content_parts = []
                                current_part = ""
                                for word in words:
                                    current_part += word + " "
                                    if len(current_part) >= 3500:
                                        content_parts.append(current_part.strip())
                                        current_part = ""
                                if current_part:
                                    content_parts.append(current_part.strip())
                                for part in content_parts:
                                    headings.append(heading.text.strip())
                                    content.append(part)
                                    tokens_count.append(len(part.split()))
                                    chapter_titles.append(chapter_title)  # Append the chapter title here

                        # Start a new heading
                        heading = element
                        content_text = ""
                    else:
                        # Append the subheading text to the content
                        content_text += element.text.strip() + " "
                else:
                    # Append the element's text to the content
                    content_text += element.text.strip() + " "

            # Save the last heading and content
            if heading and content_text:
                if len(content_text) <= 3500:
                    headings.append(heading.text.strip())
                    content.append(content_text.strip())
                    tokens_count.append(len(content_text.strip().split()))
                    chapter_titles.append(chapter_title)  # Append the chapter title here
                else:
                    # Split the content into multiple rows at the nearest word to 3500 tokens
                    words = content_text.strip().split()
                    content_parts = []
                    current_part = ""
                    for word in words:
                        current_part += word + " "
                        if len(current_part) >= 3500:
                            content_parts.append(current_part.strip())
                            current_part = ""
                    if current_part:
                        content_parts.append(current_part.strip())
                    for part in content_parts:
                        headings.append(heading.text.strip())
                        content.append(part)
                        tokens_count.append(len(part.split()))
                        chapter_titles.append(chapter_title)  # Append the chapter title here

        try:
            next_chapter_button = driver.find_element(By.LINK_TEXT, 'Next Chapter')
            if not next_chapter_button.is_enabled():
                break
            next_chapter_button.click()

            # Wait for the page to load
            time.sleep(3)
        except NoSuchElementException:
            break

    except StaleElementReferenceException:
        # Re-find the elements after the exception occurs
        continue

# Quit the driver
driver.quit()

# Create a Pandas DataFrame
data = {'Chapter Title': chapter_titles, 'Heading': headings, 'Content': content, 'Tokens': tokens_count}
df = pd.DataFrame(data)
print(df)

# %%
df.to_csv('Drive1.csv', index=False)
# %%