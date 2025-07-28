# TCO-Certified-GTIN-API-Samples
This repository contains example scripts on how to retrieve data from the TCO Certified GTIN API 

## Examples

## Python example

This Python script allows you to authenticate with the **TCO Certified API** and retrieve certified product data (e.g., Desktops, Displays) using secure credentials and flexible pagination options.

It prints product summaries in the terminal and saves full product data as a `.json` file.

---
### Features

- Login with the username and password provided by TCO Development.
 
### Command line options

| Option	        |Description	                                        |Example                     |
|-----------------|-----------------------------------------------------|----------------------------|
| --product_type	| Product category to fetch (default: Desktops)     	| --product_type Displays    |
| --jsonld	      | Include JSON-LD context in the API response	        | --jsonld                   |
| --page	        | Fetch only a specific page	                        | --page 2                   |
| --page_range	  | Fetch a range of pages (inclusive)	                | --page_range 1-4           |
| --output	      | Filename for saved results (default: products.json)	| --output my_products.json  |

| Option  | Description | Example |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

Use either --page or --page_range, not both.

---
### Usage

```bash
python fetch_gtin.py [OPTIONS]






