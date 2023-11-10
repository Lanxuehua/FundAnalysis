import csv
import requests
from bs4 import BeautifulSoup

# Define the input and output file names
input_file = 'ref_fund_href_dtl.csv'
output_file = 'output.csv'

# Define the headers for the output CSV file
output_headers = [
    "Fund Type", "Morningstar Category", "IMA Sector", "Launch Date", "Price Currency",
    "Domicile", "ISIN", "Pricing Frequency", "Fund Size", "Share Class Size",
    "Ongoing Charge", "Initial Charge", "Max Annual Charge", "Exit Charge",
    "Min Initial Investment", "Min Additional Investment", "Asset Type", "Top 5 Sectors"
]

# Define a function to extract text from an element, handling NoneType
def get_text(element):
    if element:
        return element.find_next("td").get_text(strip=True)
    return ""

# Initialize an empty list to store the data
output_data = []


# Open the input CSV file
with open(input_file, mode='r', encoding='latin-1') as csv_provider_file:
        csv_reader = csv.reader(csv_provider_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            url = row[3]
            print(url)
            
            # Send an HTTP GET request to the link
            response = requests.get(url)
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
    
                # Extract the required information
                fund_type = get_text(soup.find("th", string="Fund type"))
                morningstar_category = get_text(soup.find("th", string="Morningstar category"))
                ima_sector = get_text(soup.find("th", string="IMA sector"))
                launch_date = get_text(soup.find("th", string="Launch date"))
                price_currency = get_text(soup.find("th", string="Price currency"))
                domicile = get_text(soup.find("th", string="Domicile"))
                isin = get_text(soup.find("th", string="ISIN"))
                pricing_frequency = get_text(soup.find("th", string="Pricing frequency"))
                fund_size = get_text(soup.find("th", string="Fund size"))
                share_class_size = get_text(soup.find("th", string="Share class size"))
                ongoing_charge = get_text(soup.find("th", string="Ongoing charge"))
                initial_charge = get_text(soup.find("th", string="Initial charge"))
                max_annual_charge = get_text(soup.find("th", string="Max annual charge"))
                exit_charge = get_text(soup.find("th", string="Exit charge"))
                min_initial_investment = get_text(soup.find("th", string="Min. initial investment"))
                min_additional_investment = get_text(soup.find("th", string="Min. additional investment"))
                
                # Extract Asset Type
                # Extract Asset Type
                asset_type = soup.find('div', {'data-mod-state': 'Asset type'})
                if asset_type:
                    asset_type_table = asset_type.find('table', {'class': 'mod-ui-table'})
                    asset_type_rows = asset_type_table.find_all('tr')
                    asset_type_info = {}
                    for row in asset_type_rows:
                        columns = row.find_all('td')
                        asset_type_info[columns[0].text.strip()] = columns[1].text.strip()
                else:
                    asset_type_info = {} 
    
                # Extract Top 5 Sectors
                top_5_sectors = soup.find('div', {'data-mod-section': 'Sector'})
                if top_5_sectors:
                    top_5_sectors_table = top_5_sectors.find('table', {'class': 'mod-ui-table'})
                    top_5_sectors_rows = top_5_sectors_table.find_all('tr')
                    top_5_sectors_info = {}
                    for row in top_5_sectors_rows:
                        columns = row.find_all('td')
                        sector_name = columns[0].text.strip()
                        sector_percentage = columns[1].text.strip()
                        top_5_sectors_info[sector_name] = sector_percentage
                else:
                    top_5_sectors_info = {}  # Set it to an empty dictionary if not found
    
                # Add the extracted data to the output_data list
                output_data.append([
                    fund_type, morningstar_category, ima_sector, launch_date, price_currency,
                    domicile, isin, pricing_frequency, fund_size, share_class_size,
                    ongoing_charge, initial_charge, max_annual_charge, exit_charge,
                    min_initial_investment, min_additional_investment,
                    asset_type_info, top_5_sectors_info
                ])
        
# Write the extracted data to the output CSV file
with open(output_file, mode='w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow(output_headers)
    writer.writerows(output_data)

print("Data extraction and writing complete.")
