from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pandas_geojson import to_geojson

fields_dict = {
    "chain_name": [],
    "brand": [],
    "type": [],
    "chain_id": [],
    "name": [],
    "phones": [],
    "website": [],
    "addr:country": [],
    "addr:full": [],
    "latitude": [],
    "longitude": [],
}

TGB_URL = "https://tgbhyd.in/branch-locator"

driver = webdriver.Chrome()
driver.get(TGB_URL)

wait = WebDriverWait(driver, 10)

popup = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wzrk-cancel"]')))
popup.click()

store_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="branch-details"]/li')))
# Wait for the branches to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "branch-locator-row")))

# Find all the branch elements on the page
branch_elements = driver.find_elements(By.CLASS_NAME, "branch-locator-row")

# Rest of the code remains the same as the previous selenium implementation...

# Close the driver
driver.quit()

TGB_API_URL = "https://tgbhyd.in/wp-json/store-locator/v1/locations"

# Send an HTTP GET request to the API URL and fetch the data
response = requests.get(TGB_API_URL)
data = response.json()

for location in data:
    # Extract details for each location
    branch_name = location["title"]["rendered"]
    branch_address = location["address"]
    branch_phone = location["phone"]
    branch_latitude = location["lat"]
    branch_longitude = location["lng"]
    print(f"Name:{branch_name}, Addr:{branch_address}, Phone:{branch_phone}")

    # Append data to the dictionary
    fields_dict["chain_name"].append("TGB")
    fields_dict["brand"].append("TGB")
    fields_dict["type"].append("Chain")
    fields_dict["chain_id"].append(28417) 
    fields_dict["name"].append(branch_name)
    fields_dict["phones"].append(branch_phone)
    fields_dict["website"].append(TGB_API_URL)
    fields_dict["addr:country"].append("India")
    fields_dict["addr:full"].append(branch_address)
    fields_dict["latitude"].append(branch_latitude)
    fields_dict["longitude"].append(branch_longitude)

stores_df = pd.DataFrame(fields_dict)
print(stores_df.head())

# Convert DataFrame to GeoJSON
geo_json = to_geojson(df=stores_df, lat="latitude", lon="longitude", properties=stores_df.columns)

# Save GeoJSON data to a file
output_file_path = "tgb_branches.geojson"
with open(output_file_path, "w") as output_file:
    output_file.write(json.dumps(geo_json))

print(f"GeoJSON data has been written to {output_file_path}")


