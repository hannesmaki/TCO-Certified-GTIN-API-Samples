import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { Command } from 'commander';
import prompt from 'prompt-sync';

// --- Setup CLI
const program = new Command();
program
  .option('--product_type <type>', 'Product type to fetch', 'Desktops')
  .option('--jsonld', 'Include JSON-LD', false)
  .option('--page <number>', 'Fetch a specific page', parseInt)
  .option('--page_range <range>', 'Fetch a page range (e.g. 2-4)')
  .option('--output <filename>', 'Output filename', 'products.json')
  .parse(process.argv);

const options = program.opts();

// --- Secure user input
const input = prompt({ sigint: true });
console.log('Please enter your TCO Certified API credentials:');
const username = input('Username: ');
const password = input.hide('Password: ');

// --- Get API token
async function getToken(username, password) {
  try {
    const res = await axios.post('https://api.tcocertified.com/token', {
      username,
      password,
    });
    if (!res.data.token) throw new Error('No token returned');
    console.log('Token received');
    return res.data.token;
  } catch (err) {
    console.error('Failed to authenticate:', err.message);
    process.exit(1);
  }
}

// --- Main fetch logic
async function fetchGTIN(token) {
  const allProducts = [];
  let dynamic = false;
  let pagesToFetch = [];

  // Determine which pages to fetch
  if (options.page) {
    pagesToFetch = [options.page];
  } else if (options.page_range) {
    const [start, end] = options.page_range.split('-').map(Number);
    if (isNaN(start) || isNaN(end) || start > end) {
      console.error('Invalid page range. Use --page_range 2-4');
      process.exit(1);
    }
    pagesToFetch = Array.from({ length: end - start + 1 }, (_, i) => start + i);
  } else {
    dynamic = true;
    pagesToFetch = [];
  }

  let currentPage = dynamic ? 1 : null;

  while (dynamic || pagesToFetch.length) {
    const page = dynamic ? currentPage : pagesToFetch.shift();

    const params = {
      page,
      product_type: options.product_type,
      jsonld: options.jsonld,
    };

    try {
      console.log(`Fetching page ${page}...`);
      const res = await axios.post('https://api.tcocertified.com/generic/gtin', null, {
        headers: {
          'X-Auth-Token': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        params,
      });

      const products = res.data?.data?.products ?? [];
      if (!products.length) {
        console.log('No products on this page.');
        if (dynamic) break;
        continue;
      }

      allProducts.push(...products);

      if (dynamic) {
        const meta = res.data.meta ?? {};
        if (meta.page >= meta.totalPages) {
          console.log('All pages retrieved.');
          break;
        }
        currentPage++;
      }
    } catch (err) {
      console.error(`Failed on page ${page}:`, err.message);
      break;
    }
  }

  // Save to file
  try {
    const outPath = path.resolve(process.cwd(), options.output);
    fs.writeFileSync(outPath, JSON.stringify(allProducts, null, 2), 'utf-8');
    console.log(`Data saved to ${outPath}`);
  } catch (err) {
    console.error('Failed to save output file:', err.message);
  }
}

// --- Run
const token = await getToken(username, password);
await fetchGTIN(token);
