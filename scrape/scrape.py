import re
import time
import random
import requests
from bs4 import BeautifulSoup


def getContents(url):
    time.sleep(2) # Avoid DDoS
    page = requests.get(url)
    if (page.status_code == 200):
        return page.content

def website(url):
    contents = getContents(url)

    if (contents != None):
        # Parse information table
        soup = BeautifulSoup(contents, 'html.parser')
        table = soup.find('table', {"class": "data_table lengthy"})
        table_rows = table.findAll('tr')

        # Initialize parent variables
        person = {}
        parent_urls = []

        # Loop through each row in table
        for table_row in table_rows:
            if (not table_row.find('td', {"class": "spacer"})):
                head_cells = table_row.findAll('th')
                data_cells = table_row.findAll('td')

                # Some rows has both th and td, others have only td
                if (len(head_cells) + len(data_cells) == 1):
                    person["Name"] = data_cells[0].text.strip()
                elif (len(head_cells) + len(data_cells) == 2):
                    if (len(head_cells) > 0):
                        key = head_cells[0].text.strip().replace(":", "")
                        value = data_cells[0].text.strip()
                    else:
                        key = data_cells[0].text.strip().replace(":", "")
                        value = re.sub(' +', ' ', data_cells[1].text.strip().replace('\n', ''))

                    # Parse parents from row related to 'Immediate Family'
                    if (key == 'Immediate Family'):
                        family_entities = data_cells[0].find('p')
                        if (family_entities.text.startswith("Son of") or family_entities.text.startswith("Daughter of")):
                            parents_text = family_entities.text.split("\n")[0]
                            all_links = family_entities.findAll('a')
                            
                            # Remove link text from row related to parents (since it may include the 'and' word)
                            # Removing this may cause a infinite loop
                            for all_link in all_links:
                                parents_text = parents_text.replace(all_link.text, "")

                            # Find the number of parents that exists
                            if ("and" in parents_text):
                                number_of_parents = 2
                            else:
                                number_of_parents = 1

                            # Fetch the links to the parents
                            parent_links = family_entities.findAll('a')
                            for parent_link in parent_links[:number_of_parents]:
                                parent_urls.append(parent_link['href'])
                        else:
                            parent_urls = []
                    
                    # Add each row to dictionary
                    person[key] = value

        # Return results
        return person, parent_urls
    else:
        print("No contents received from Geni...")
