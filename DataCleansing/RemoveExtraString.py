"""
Fund name data cleasing
remove the ISIN string in the fund name

"""

import csv
import pandas as pd

# Define the input and output file names
input_file = 'ref_fund_href_dtl_backup.csv'
output_file = 'ref_fund_href_dtl.csv'

output_headers = ["ProviderName","FundName","ISIN","Href"]

# Open the input and output files
with open(input_file, mode='r', newline='') as input_csv, open(output_file, mode='w', newline='') as output_csv:
    reader = csv.DictReader(input_csv)
    fieldnames = reader.fieldnames

    # Create the output CSV writer with the same fieldnames
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the rows in the input CSV
    for row in reader:
        row['Fund Name'] = row['Fund Name'][:-len(row['ISIN Code'])]
        writer.writerow(row)
