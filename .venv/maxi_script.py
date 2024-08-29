# maxi_script.py

from selenium_setup import setup_driver
from selenium.webdriver.common.by import By 
import time


def scrape_maxi():
    # Set up the driver
    driver = setup_driver()

    # Define the groceries list and their URLs for Maxi grocery store
    groceries_list = {
        "rice": "https://www.maxi.ca/food/pantry/rice/long-grain/c/29682",
        "flours": "https://www.maxi.ca/food/pantry/baking-essentials/flours/c/29695",
        "sugar": "https://www.maxi.ca/food/pantry/baking-essentials/sugar-sweetener/c/29878",
        "milk": "https://www.maxi.ca/food/dairy-eggs/milk-cream/regular-milk/c/29789"
    }

    maxi_results = []

    for grocery_item, url in groceries_list.items():
        driver.get(url)
        time.sleep(5)

        pagination_links = driver.find_elements(By.XPATH, '//nav[@aria-label="Pagination"]//a')

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
            time.sleep(5)

            products = driver.find_elements(By.XPATH, '//div[@class="chakra-linkbox css-vhnn8v"]')

            page_cheapest_product = None

            for product in products:
                try:
                    product_brand = product.find_element(By.XPATH,
                                                         './/p[contains(@class,"chakra-text css-1ecdp9w")]').text
                    product_title = product.find_element(By.XPATH,
                                                         './/h3[contains(@class, "chakra-heading css-6qrhwc")]').text
                    product_price = product.find_element(By.XPATH, './/span[contains(@class, "css-idkz9h")]').text
                    product_info = product.find_element(By.XPATH,
                                                        './/p[@class="chakra-text css-1yftjin" and @data-testid="product-package-size"]').text

                    unity, info_price = product_info.split(', ')
                    price_per_qty = float(info_price.split('/')[0].replace('$', '').replace(',', '.').strip())
                    price_per_qty = round(price_per_qty, 2)

                    product_details = {
                        'Grocery_Item': grocery_item,
                        'Product_Brand': product_brand,
                        'Product_Title': product_title,
                        'Product_Price': product_price,
                        'Product_Info': info_price,
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
            maxi_results.append({
                'grocery_store': 'Maxi',
                'grocery_item': grocery_item,
                'cheapest_product': grocery_item_cheapest_product
            })

    driver.quit()
    return maxi_results
