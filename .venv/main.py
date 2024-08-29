# main.py

import superc_script
import maxi_script
from datetime import datetime
import mongodb_integration

def print_and_save_cheapest_products():
    # Get today's date
    today = datetime.today().strftime('%Y-%m-%d')

    # Get the cheapest products from both Maxi and Super C
    maxi_results = maxi_script.scrape_maxi()
    superc_results = superc_script.scrape_superc()

    # Combine the results
    all_results = maxi_results + superc_results

    # Create a MongoDB collection
    collection = mongodb_integration.create_database()

    # Print and save the details
    print(f"\nCheapest Products for {today}:\n")
    for result in all_results:
        grocery_store = result['grocery_store']
        grocery_item = result['grocery_item']
        cheapest_product = result['cheapest_product']
        print(f"Date: {today}, Grocery Store: {grocery_store}, Grocery Item: {grocery_item}")
        print(f"Product Brand: {cheapest_product['Product_Brand']}")
        print(f"Product Title: {cheapest_product['Product_Title']}")
        print(f"Product Price: {cheapest_product['Product_Price']}")
        print(f"Product Info: {cheapest_product['Product_Info']}")
        print(f"Unity: {cheapest_product['Unity']}")
        print(f"Price per Quantity: {cheapest_product['Price_Qty']}\n")

        # Insert data into MongoDB
        mongodb_integration.insert_into_database(collection, grocery_store, grocery_item, cheapest_product)

    # Retrieve and print all data from MongoDB to verify
    all_products = mongodb_integration.retrieve_data(collection)
    print("\nRetrieved Products from MongoDB:")
    for product in all_products:
        print(product)

if __name__ == "__main__":
    print_and_save_cheapest_products()
