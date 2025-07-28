import requests
import os
import json
import getpass

import requests
import getpass
import argparse
import json
import os
from typing import List


def get_token(username: str, password: str) -> str:
    """
    Authenticates with the TCO Certified API and returns a bearer token.
    """
    auth_url = "https://api.tcocertified.com/token"
    credentials = {"username": username, "password": password}

    try:
        response = requests.post(auth_url, json=credentials)
        response.raise_for_status()
        token = response.json().get("token")

        if not token:
            raise ValueError("Authentication succeeded, but no token was returned.")
        
        return token

    except requests.RequestException as e:
        print("Token request failed:", e)
        raise


def fetch_gtin_data(
        token: str,
        product_type: str,
        jsonld: bool,
        page: int = None,
        page_range: str = None,
        output_file: str = "products.json"
        ) -> None:
    
    """
    Fetches paginated GTIN data from the TCO Certified API and optionally saves it to a JSON.
    """
    base_url = "https://api.tcocertified.com/generic/gtin"
    headers = {
        "X-Auth-Token": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    dynamic = False

    if page:
        pages_to_fetch = [page]
    elif page_range:

        try:
            start, end = map(int, page_range.split('-'))
            if start > end:
                raise ValueError
            pages_to_fetch = list(range(start, end + 1))

        except ValueError:
            print("Invalid page range format. Use e.g. --page_range 2-5")
            return
    else:
        # Unknown total at start: fetch all pages dynamically
        pages_to_fetch = []
        dynamic = True
        print("Fetching all available pages...")
        
        page = 1

    all_products = []
    while True:
        # For fixed pages
        if not pages_to_fetch and not dynamic:
            break
        elif not pages_to_fetch and dynamic:
            current_page = page
        else:
            if not pages_to_fetch:
                break
            current_page = pages_to_fetch.pop(0)

        params = {
            "page": current_page,
            "product_type": product_type,
            "jsonld": jsonld
        }

        response = requests.post("https://api.tcocertified.com/generic/gtin", headers=headers, params=params)

        if not response.ok:
            print(f"Request failed on page {current_page}: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        products = data.get("data", {}).get("products", [])

        if not products:
            print("No products found on this page.")
            if dynamic:
                break
            else:
                continue

        all_products.extend(products)

        if dynamic:
            meta = data.get("meta", {})
            current = meta.get("page", current_page)
            total = meta.get("totalPages", current)
            print(f"Page {current} / {total}", "fetched")
            if current >= total:
                print("All pages retrieved.")
                break
            page += 1

    save_products_to_json(all_products, output_file)


def save_products_to_json(products: list, filename: str) -> None:
    """
    Saves the full list of product dictionaries to a JSON file.
    """
    if not products:
        print("No data to save.")
        return

    try:
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(products, file, indent=2, ensure_ascii=False)
        print(f"All product data saved to '{os.path.abspath(filename)}'")
    except Exception as e:
        print(f"Failed to save JSON: {e}")


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch product certification data from the TCO Certified API."
    )

    # Product & output options
    parser.add_argument("--product_type", type=str, default="Desktops", help="Product type to fetch")
    parser.add_argument("--jsonld", action="store_true", help="Include JSON-LD in the response")
    parser.add_argument("--output", type=str, default="products.json", help="Output filename")

    # Mutually exclusive pagination options
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--page", type=int, help="Fetch only a specific page (e.g., --page 3)")
    group.add_argument("--page_range", type=str, help="Fetch a range of pages (e.g., --page_range 2-5)")

    return parser.parse_args()

    
if __name__ == "__main__":
    args = parse_args()

    print("Please enter your TCO Certified API credentials:")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        token = get_token(username, password)
    except Exception as e:
        print("Exiting due to authentication failure.")
        exit(1)

    fetch_gtin_data(
        token=token,
        product_type=args.product_type,
        jsonld=args.jsonld,
        page=args.page,
        page_range=args.page_range,
        output_file=args.output
    )


    """
    examples:
    
    # Fetch Desktops from page 1 with default output file
    python script.py

    
    # Fetch Displays from page 3 with JSON-LD included
    python script.py --product_type Displays --page 3 --jsonld

    # Save to a custom file
    python script.py --output my_certified_products.json
    
    
    """