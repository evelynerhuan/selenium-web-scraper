# Web Scraping Project with Selenium

This project demonstrates how to use Selenium (Python) to control a WebDriver for automating interactions with a web-based shopping system. It provides a practical example of automating the process of logging in, searching for products, placing orders, and handling CAPTCHA challenges.

## Project Overview

The project is designed to interact with a mock shopping website, automating various tasks such as placing orders and retrieving information about products. It also includes handling CAPTCHA images using OCR technology.

### Website Example: CDS Shop

This project interacts with a fictional online store. The system requires users to log in, search for products, add them to the cart, and complete the checkout process.

## Setting Up Your Environment

To get started, you'll need to set up your Python environment and install the necessary dependencies.

```bash
conda create -n selenium_scraping python=3.9
conda activate selenium_scraping
conda install selenium=4.12.0 -c conda-forge
pip install ddddocr
```

Make sure to run your code within the `selenium_scraping` environment for consistent results.

## Project Tasks

### 1. Automate Order Placement

This script automates the process of placing an order for a specific item (e.g., "IPHONE 11 PRO 256GB MEMORY"). The script will:

1. Log in to the website using the provided account credentials.
2. Navigate to the specific item’s page.
3. Add the item to the shopping cart.
4. Proceed to checkout.
5. Fill in the required shipping and payment information.
6. Place the order.
7. Handle CAPTCHA challenges using OCR.

#### CAPTCHA Handling

The CAPTCHA is bypassed by capturing the image rendered on an HTML canvas element, saving it locally, and processing it with an OCR tool. The following resources were helpful in developing this feature:

- [Capturing HTML Canvas](https://stackoverflow.com/questions/923885/capture-html-canvas-as-gif-jpg-png-pdf)
- [ddddocr Library](https://github.com/sml2h3/ddddocr)

### 2. Find the Top-X Most Expensive Products for a Given Keyword

The script automates the search for products based on a keyword, collects their prices, and returns the top X most expensive products. The results are saved in a CSV file, including the product name, price, and description, sorted in descending order by price.

Example output:

```csv
product_name,product_price,description
"APPLE PENCIL(2ND GENERATION)",296.99,"Compatible with iPad mini(6th generation),..."
"APPLE MACBOOK AIR 11 INCHES",269,"Includes: 1-Pack MacBook Air 11 inches MD223LL/A..."
"APPLE WATCH SERIES 5",249.99,"GPS;Always-On Retina display;30% larger screen;Swim..."
```

### 3. Place Orders for the Top-X Products

After identifying the top X most expensive products, this script automates the process of placing orders for those items. 

### 4. Additional Features (TBA)

This section is reserved for future enhancements or additional functionalities that might be added to the project.

## Tips and Best Practices

- **Change Account Password:** If you're using a real account, ensure your password is secure.
- **Code Optimization:** Replace hard-coded delays with dynamic waits using [WebDriver Waits](https://www.selenium.dev/documentation/webdriver/waits/).
- **Headless Mode:** Consider running the browser in headless mode to improve execution speed.
- **Testing:** Test your scripts on items with ample stock to ensure your automation works as expected.
- **Monitoring:** If you wish to monitor specific items (e.g., limited stock items), design your script to be efficient and respectful of server resources.

---

## Project Structure

The project is organized into several key files and directories:

```plaintext
selenium-web-scraper/
│
├── src/
│   ├── scraper.py           # Main script containing the web automation logic
│   └── utils.py             # Utility functions used across the project
│
├── results/                 # Directory where output files (e.g., CSVs, images) are saved
│   ├── top_x_products_<keyword>.csv
│   └── captcha_image.jpg
│
└── README.md                # Project documentation
```

### File Descriptions

- **`scraper.py`**: This is the main script that performs web automation tasks such as placing orders, finding the most expensive products, and handling CAPTCHA challenges.
  
- **`utils.py`**: Contains utility functions like opening a web browser and searching for keywords, which are used across the project to avoid redundancy and keep the code modular.

- **`results/`**: This directory is where all output files are stored, including the list of top expensive products in CSV format and any images processed during the CAPTCHA solving process.

## Running the Project

### 1. Install Dependencies

Ensure you have the necessary Python packages installed. You can do this by running:

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

To avoid hardcoding sensitive information like login credentials, you can use environment variables. Create a `.env` file or set the environment variables in your shell session.

Example `.env` file:

```plaintext
SHOP_URL=http://xx.xxx.xxx.xxx （private website）
SHOP_USERNAME=your_email@example.com
SHOP_PASSWORD=your_password
```

Load these variables in your script using `python-dotenv` or similar packages.

### 3. Execute the Scripts

To run the scripts, navigate to the project directory and execute the main script:

```bash
python src/scraper.py
```

This will:
1. Place an order for a specific product.
2. Find and save the top 3 most expensive products related to the keyword "apple".
3. Automatically place orders for the top 2 most expensive products related to the keyword "phone".

### 4. Review the Results

After running the script, check the `results/` directory for output files such as:

- `top_x_products_<keyword>.csv`: A CSV file listing the top X expensive products found during the search.
- `captcha_image.jpg`: The CAPTCHA image that was processed by the OCR tool.

## Future Improvements

Here are some potential enhancements for this project:

1. **Headless Mode**: To speed up execution and reduce resource usage, the browser can be run in headless mode, where it operates without a visible UI.
  
2. **Advanced CAPTCHA Handling**: Implement a more robust CAPTCHA-solving technique, or integrate a third-party service for CAPTCHA bypassing.
  
3. **Error Handling**: Add more comprehensive error handling to gracefully manage unexpected issues like network interruptions or element not found exceptions.

4. **Continuous Integration (CI)**: Integrate with a CI tool like GitHub Actions to automatically run tests on each commit, ensuring the scraper works as expected.

5. **Monitoring and Alerts**: Set up a monitoring system that alerts you when a specific product becomes available or its price drops below a certain threshold.


## Acknowledgments

This project was inspired by the need to automate repetitive tasks in web-based environments. Special thanks to the maintainers of Selenium and other open-source tools that made this project possible.
