from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pandas_geojson import to_geojson
import uuid

fields_dict = {
    "chain_name": [],
    "brand": [],
    "Type": [],
    "chain_id": [],
    "name": [],
    "Website": [],
    "addr:country": [],
    "addr:full": [],
    "Latitude": [],
    "Longitude": [],
    "ref":[],
    "@spider":[],
}

FOREVER_21_URL = "https://www.Forever21.in/content/storelocator?source=footer"

driver = webdriver.Chrome()
driver.get(FOREVER_21_URL)

wait = WebDriverWait(driver, 10)

#popup = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wzrk-cancel"]')))
#popup.click()

store_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@id="stores-list"]/li')))

for store in store_list:
    # First get the normal info
    store_name = store.find_element(By.TAG_NAME, "h4").text
    store_addr = store.find_element(By.CLASS_NAME, "store__addr").text
    #phone_number = store.find_element(By.CLASS_NAME, "store__contact").text
    reference = uuid.uuid4().hex
    print(f"Name: {store_name}, Addr: {store_addr}")

    # Open and switch to new window
    driver.execute_script(f"window.open('{FOREVER_21_URL}', '_blank')")
    driver.switch_to.window(driver.window_handles[1])
    
    #wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wzrk-cancel"]')))
    
    new_tab_store_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@id="stores-list"]/li')))
    
    # Find the corresponding store element in the new tab
    new_tab_store = None
    for s in new_tab_store_list:
        if s.find_element(By.TAG_NAME, "h4").text == store_name:
            new_tab_store = s
            break
    
    if new_tab_store is None:
        print(f"Could not find store {store_name} in new tab")
        continue
    
    # Click the button
    button = new_tab_store.find_element(By.TAG_NAME, "button")
    button.click()
    
    # Wait for the modal dialog to open
    wait.until(EC.visibility_of_element_located((By.ID, 'storeModal')))
    
    map_itm = driver.find_element(By.XPATH, '//div[@id="map2"]/iframe')
    
    google_maps_addr = map_itm.get_attribute("src")
    
    lat_lon = google_maps_addr.split("?")[1].split("&")[0].split("=")[1].split(",")
    
    lat = lat_lon[0]
    lon = lat_lon[1]
    
    print(f"Lat: {lat}, Lon: {lon}")

    # 2nd window work done. Switch back to first one
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    fields_dict["chain_name"].append("Forever21")
    fields_dict["brand"].append("Forever21")
    fields_dict["Type"].append("Chain")
    fields_dict["chain_id"].append(4196)
    fields_dict["name"].append(store_name)
    #fields_dict["phones"].append(phone_number)
    fields_dict["Website"].append(FOREVER_21_URL)
    fields_dict["@spider"].append("Forever_21")
    
    fields_dict["addr:country"].append("India")
    fields_dict["addr:full"].append(store_addr)
    fields_dict["Latitude"].append(float(lat))
    fields_dict["Longitude"].append(float(lon))
    fields_dict["ref"].append(reference)
stores_df = pd.DataFrame(fields_dict)
print(stores_df.head())


geo_json = to_geojson(df=stores_df, lat="Latitude", lon="Longitude", properties=stores_df.columns)
#geo_json = to_geojson(df=stores_df, lat="Latitude", lon="Longitude")
print(geo_json)

import json

# Your existing code for creating the DataFrame 'stores_df' and converting to GeoJSON
# ...

# Convert DataFrame to GeoJSON
geo_json = to_geojson(df=stores_df, lat="Latitude", lon="Longitude", properties=stores_df.columns)

# Save GeoJSON data to a file named 'stores.geojson'
output_file = 'stores.geojson'
with open(output_file, 'w') as file:
    json.dump(geo_json, file)

print(f"GeoJSON data has been saved to {output_file}.")
