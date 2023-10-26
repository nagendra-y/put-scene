from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from unshortenit import UnshortenIt
from selenium import webdriver

# Option 1: Read HTML from a file
#with open("event_page.html", "r", encoding="utf-8") as file:
    #html_content = file.read()

# Option 2: Use Selenium to fetch the page
# Set up the Selenium web driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://events.venn.buzz/")

# Get the page source (HTML content)
html_content = driver.page_source

# Convert the HTML content to a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find the first <div> with class "chakra-stack"
first_stack_div = soup.find('div', class_='chakra-stack')

# Select all top-level <a> elements with class "chakra-link" inside the first div
event_cards = first_stack_div.find_all('a', class_='chakra-link', recursive=False)

print(len(event_cards))

# Initialize an empty list to store event dictionaries
event_list = []

# Iterate over each event card
for card in event_cards:
    event_dict = {}
   
    # Extract title
    title = card.select_one('.chakra-heading').text
    event_dict['title'] = title

    # Extract description (the first <p> element)
    description = card.select('p')[0].text
    event_dict['description'] = description

    # Extract time info (the second <p> element)
    time_info = card.select('p')[1].text
    event_dict['time'] = time_info

    # Extract location from the second <a> element
    location_element = card.find_all('a')[1]
    location = location_element.text
    location_link = location_element['href']
    event_dict['location'] = location
    event_dict['location_link'] = location_link

    event_link = card['href']
    event_dict['event_link'] = event_link
    
    # Append the event dictionary to the list
    event_list.append(event_dict)

# Close the browser
#driver.quit()

# Define a function to convert the time to a sortable format
def sort_by_time(event):
    time_str = event['time'].replace('@', '')
    return datetime.strptime(time_str, '%dth %B %I:%M %p')

# Create an UnshortenIt instance
unshortener = UnshortenIt()

# Function to expand Bit.ly links
def expand_bitly_links(event):
    if event.get('event_link'):
        expanded_link = unshortener.unshorten(event['event_link'])
        event['event_link'] = expanded_link

for event in event_list:
    expand_bitly_links(event)

# Sort the events by time
sorted_events = sorted(event_list, key=sort_by_time)


event_text = ""

for event in sorted_events:
    event_text += f"{event['title']}\n"
    event_text += f"{event['description']}\n"
    event_text += f"{event['time']}\n"
    event_text += f"{event['location']}\n"
    event_text += f"{event['location_link']}\n"
    event_text += f"{event['event_link']}\n"
    event_text += "=====\n"

# Print or save 'event_text' to a file
print(event_text)
