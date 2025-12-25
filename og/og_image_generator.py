# This script generates OG images from web page.
# usage: python og_image_generator.py <html_file_name> [output_file_name]

import sys
import os
import asyncio
from pathlib import Path

# Try to import playwright, handle if missing
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Error: 'playwright' library is required. Please install it via 'pip install playwright' and run 'playwright install'.")
    sys.exit(1)

async def generate_og_image(html_path, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Standard OG Image size is usually 1200x630
        page = await browser.new_page(viewport={'width': 1200, 'height': 630})
        
        # Convert local path to URI so the browser can load it
        file_uri = Path(os.path.abspath(html_path)).as_uri()
        
        await page.goto(file_uri)
        await page.screenshot(path=output_path)
        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python og_image_generator.py <html_file_name> [output_file_name]")
        sys.exit(1)
        
    html_file = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = str(Path(html_file).with_name(f"{Path(html_file).stem}_og.png"))
    
    if not os.path.exists(html_file):
        print(f"Error: File '{html_file}' not found.")
        sys.exit(1)

    print(f"Generating OG image from {html_file} to {output_file}...")
    asyncio.run(generate_og_image(html_file, output_file))
    print("Done.")
