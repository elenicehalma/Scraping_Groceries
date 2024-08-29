# mongodb_integration.py

from pymongo import MongoClient
from datetime import datetime

def create_database():
    """
    Connect to MongoDB and create the database and collection if they don't exist.
    Returns the collection to be used for further operations.
    """
    # Connect to MongoDB server running on localhost at port 27017
    client = MongoClient('localhost', 27017)

    # Access the GroceriesPricesTest database
    db = client.GroceriesPricesTest

    # Access the ProductsTest collection
    collection = db.ProductsTest

    # To verify the connection, let's print the names of the collections in the database
    print("Collections in GroceriesPricesTest:", db.list_collection_names())

    return collection  # Return the collection for further operations

def insert_into_database(collection, grocery_store, grocery_item, product):
    """
    Insert a single product entry into the MongoDB collection if the same date, grocery_store, grocery_item,
    Product_Brand, and Product_Title do not already exist.
    """

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Check 
    existing_document = collection.find_one({
        "date": today,
        "grocery_store": grocery_store,
        "grocery_item": grocery_item,
        "product_details.product_brand": product['Product_Brand'],
        "product_details.product_title": product['Product_Title']
    })

    
    if not existing_document:
        product_details = {
            "date": today,
            "grocery_store": grocery_store,
            "grocery_item": grocery_item,
            "product_details": {
                "product_brand": product['Product_Brand'],
                "product_title": product['Product_Title'],
                "product_price": product['Product_Price'],
                "product_info": product['Product_Info'],
                "unity": product['Unity'],
                "price_qty": product['Price_Qty']
            }
        }

        # Insert the document into the collection
        collection.insert_one(product_details)
        print("Product inserted successfully!")
    else:
        print("Duplicate product found; skipping insertion.")

def retrieve_data(collection, query={}):
    """
    Retrieve data from MongoDB based on the provided query.
    """
    return list(collection.find(query))
