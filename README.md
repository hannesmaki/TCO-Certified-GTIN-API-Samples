# TCO-Certified-GTIN-API-Samples
This repository contains example scripts on how to retrieve data from the TCO Certified GTIN API 

## Python example

This Python script allows you to authenticate with the **TCO Certified API** and retrieve certified product data (e.g., Desktops, Displays) using secure credentials and flexible pagination options.

It saves retrieved product data as a `.json` file in the same folder as the scipt is located in. 

---
### Features

- Login with the username and password provided by TCO Development.
 
### Command line options

| Option	        |Description	                                        |Example                     |
|-----------------|-----------------------------------------------------|----------------------------|
| --product_type	| Product category to fetch (default: Desktops)       	| --product_type Displays    |
| --jsonld	      | Include JSON-LD context in the API response	        | --jsonld                   |
| --page	        | Fetch only a specific page	                         | --page 2                   |
| --page_range	  | Fetch a range of pages (inclusive)	                 | --page_range 1-4           |
| --output	      | Filename for saved results (default: products.json)	| --output my_products.json  |


Use either --page or --page_range, not both.

---
### Usage examples

Base
```bash
python fetch_gtin.py [OPTIONS]
```

Fetch only page 2 of Displays:
```bash
python fetch_gtin.py --product_type Displays --page 2
```

Fetch pages 1 through 5 of Displays with JSON-LD and custom output:
```bash
python fetch_gtin.py --product_type Displays --jsonld --page_range 1-5 --output displays.json
```
### Output
retrieved product data is saved as a `.json` file in the same folder as the scipt is located in. 

```json

[
  {
    "certificationInfo": {
      "agency": "TCO Development",
      "agencyURL": "https://tcocertified.com/",
      "certificateId": "D1024110043",
      "endDate": "2026-12-22",
      "id": "https://tcocertified.com/product-finder/?cert=D1024110043",
      "program": "TCO Certified",
      "standard": "TCO Certified, generation 10, for displays",
      "startDate": "2024-12-04",
      "status": "ACTIVE",
      "type": "CertificationDetails"
    },
    "gtin": "05397184821671",
    "id": "https://id.gs1.org/01/05397184821671",
    "name": "P2425",
    "type": "Product"
  },
...
]


```



