from selenium import webdriver
import time

# Set up the Selenium web driver
cService = webdriver.ChromeService(executable_path='/home/indra/trash/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service = cService)

driver.get("https://events.venn.buzz/")

# Wait for the page to load (adjust the wait time as needed)
time.sleep(5)

# Get the page source (HTML content)
html_content = driver.page_source

# Close the browser
driver.quit()

# Save the HTML content to a file
with open("event_page.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML content has been saved to 'event_page.html'.")

