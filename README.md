# TCO-Certified-GTIN-API-Samples
This repository contains example scripts on how to retrieve data from the TCO Certified GTIN API 

## Examples

## Python example

This Python script allows you to authenticate with the **TCO Certified API** and retrieve certified product data (e.g., Desktops, Displays) using secure credentials and flexible pagination options.

It prints product summaries in the terminal and saves full product data as a `.json` file.

---
### Features

- Secure login with username and hidden password prompt
- Fetch:
  - A specific page (`--page 2`)
  - A range of pages (`--page_range 1-5`)
  - All available pages (default)
- Output:
  - Pretty-printed raw JSON
  - Terminal display of `name`, `gtin`, `certificateId`
- Works from command line or in automated pipelines

---

### Usage

```bash
python fetch_gtin.py [OPTIONS]


