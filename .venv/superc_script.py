# superc_script.py

from selenium_setup import setup_driver
from selenium.webdriver.common.by import By 
import time


def scrape_superc():
    # Set up the driver
    driver = setup_driver()

    # Define the groceries list and their URLs for Super C grocery store
    groceries_list = {
        "rice": "https://www.superc.ca/en/aisles/pantry/pasta-rice-beans/rice",
        "flours": "https://www.superc.ca/en/aisles/pantry/baking-ingredients/flour-baking-essentials",
        "sugar": "https://www.superc.ca/en/aisles/pantry/baking-ingredients/sugar-sweeteners",
        "milk": "https://www.superc.ca/en/aisles/dairy-eggs/milk-cream-butter/2-whole-milk"
    }

    def close_popup(driver):
        try:
            if len(driver.find_elements(By.ID, 'onetrust-reject-all-handler')) > 0:
                refuse_button = driver.find_element(By.ID, 'onetrust-reject-all-handler')
                refuse_button.click()
                time.sleep(2)
        except Exception as e:
            print(f"An error occurred while trying to close the popup: {e}")

    driver.get(groceries_list['rice'])
    time.sleep(5)
    close_popup(driver)

    superc_results = []

    for grocery_item, url in groceries_list.items():
        driver.get(url)
        time.sleep(5)

        pagination_links = driver.find_elements(By.XPATH, '//div[@class="ppn--pagination"]/a')

        page_list = []
        base_url = driver.current_url.split('?')[0]

        for link in pagination_links:
            href = link.get_attribute('href')
            if href:
                if href.startswith("http"):  # Full URL
                    full_url = href
                else:  # Relative URL
                    full_url = base_url + href
                if full_url not in page_list:
                    page_list.append(full_url)

        if not page_list:
            page_list.append(driver.current_url)

        grocery_item_cheapest_product = None

        for page in page_list:
            driver.get(page)
            time.sleep(3)

            products = driver.find_elements(By.XPATH, '//div[contains(@class, "default-product-tile")]')

            page_cheapest_product = None

            for product in products:
                try:
                    product_brand = product.find_element(By.XPATH, './/span[contains(@class,"head__brand")]').text
                    product_title = product.find_element(By.XPATH, './/div[contains(@class, "head__title")]').text
                    product_price = product.find_element(By.XPATH, './/span[contains(@class, "price-update")]').text
                    product_info = product.find_element(By.XPATH,
                                                        './/div[contains(@class, "pricing__secondary-price")]').text
                    unity = product.find_element(By.XPATH, './/span[contains(@class, "head__unit-details")]').text

                    price_per_qty = float(product_info.split('/')[0].replace('$', '').replace(',', '.').strip())
                    price_per_qty = round(price_per_qty, 2)

                    product_details = {
                        'Grocery_Item': grocery_item,
                        'Product_Brand': product_brand,
                        'Product_Title': product_title,
                        'Product_Price': product_price,
                        'Product_Info': product_info,
                        'Unity': unity,
                        'Price_Qty': price_per_qty
                    }

                    if page_cheapest_product is None or price_per_qty < page_cheapest_product['Price_Qty']:
                        page_cheapest_product = product_details

                except Exception as e:
                    continue

            if page_cheapest_product:
                if grocery_item_cheapest_product is None or page_cheapest_product['Price_Qty'] < \
                        grocery_item_cheapest_product['Price_Qty']:
                    grocery_item_cheapest_product = page_cheapest_product

        if grocery_item_cheapest_product:
            superc_results.append({
                'grocery_store': 'Super C',
                'grocery_item': grocery_item,
                'cheapest_product': grocery_item_cheapest_product
            })

    driver.quit()
    return superc_results
