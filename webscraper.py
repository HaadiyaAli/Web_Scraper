import requests 
from bs4 import BeautifulSoup
from pprint import pprint
from IPython.display import Markdown, display
import tkinter as tk

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 
    'Accept-Language': 'en-US,en;q=0.9',
}


# Extracts product info (like title and price) from a given product URL and returns it as a dictionary
# Takes a product URL as a string and returns product info as a dictionary (type hints for clarity only)
def get_product_details(product_url: str) -> dict:
    #Create an empty ptoduct details dictionary
    product_details = {}

    #Get the product page content and create a soup, by seing a https request to the product url
    page = requests.get(product_url, headers= headers)
    soup = BeautifulSoup(page.content, features='lxml')

    try:
        #Extract the product title 
        title =soup.find('span',attrs={'id': 'productTitle'}).get_text().strip()

        #Extract the product price
        # Note: The class name for the price may vary, so you might need to adjust it based on the actual HTML structure
        extracted_price = soup.find('span', attrs={'class': 'a-price'}).get_text().strip()
        #Fix the double price issue by removing the second price 
        #Split it at at $ ['', '14.99', '14.99'] and get the secound value 
        price = extracted_price.split('$')[1]# Assuming the first part is the price

        #Get rating information 
        rating = soup.find('span', attrs = {'class': 'a-icon-alt'}).get_text().strip()
        number_of_reviews = soup.find('span', attrs = {'id': 'acrCustomerReviewText'}).get_text().strip()

        about_items = soup.find('div', id='feature-bullets').find_all('span', class_='a-list-item')
        about_text = [item.get_text().strip() for item in about_items if item.get_text().strip()]


        #put into product details dictionary 
        product_details['title'] = title
        product_details['price'] = '$'+ price
        product_details['rating'] = rating + ' with ' + number_of_reviews
        product_details['about'] = ', '.join(about_text)

        return product_details
    except Exception as e:
        print('Could not fetch product data')
        print(f'Faled with error{e}')

    

#intialize the window 
window = tk.Tk()
window.geometry("600x400")  
window.title("WebScrapper!")
label = tk.Label(window, text="Welcome to WebScrapper!", font=("Arial", 24), fg="black")
label.pack(pady=20)

#input box
url = tk.Entry(window, font=("Arial", 10), width=30)
url.pack(pady=10)
url.insert(0, "Enter product URL here...")  # Placeholder text

def show_input():
    product_url = url.get()
    product_details = get_product_details(product_url)
    #Get all the product details and join them 
    result_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in product_details.items()])
    
    output_label.config(state="normal")
    output_label.delete("1.0", "end")
    output_label.insert("1.0", result_text)
    output_label.config(state="disabled")


# Submit button
submit_button = tk.Button(window, text="Submit", command=show_input)
submit_button.pack(pady=5)

# Output frame (after Submit button)
output_frame = tk.Frame(window, padx=10, pady=10, bd=1, relief="groove")
output_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Scrollbar and output text area
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output_label = tk.Text(
    output_frame,
    font=("Arial", 12),
    wrap="word",
    yscrollcommand=scrollbar.set
)
output_label.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output_label.yview)
output_label.config(state="disabled")

# Run the app
window.mainloop()