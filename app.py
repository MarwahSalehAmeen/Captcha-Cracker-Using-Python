from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image, ImageDraw, ImageFont
import io
import random
import string
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for the session

# Generate captcha
def generate_captcha():
    captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return captcha

# Generate captcha image
def generate_captcha_image(captcha):
    width, height = 400, 200
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    font = ImageFont.truetype('arial.ttf', size=100)
    draw = ImageDraw.Draw(image)
    draw.text((80, 50), captcha, fill=(0, 0, 0), font=font)
    
    # Save the image to a byte buffer
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)
    
    image_path = os.path.join('static', 'captcha.png')
    image.save(image_path, format='PNG', overwrite=True)

    # Encode the image bytes as base64
    img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
    
    return img_base64

# Landing page with login form
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_captcha = request.form['captcha']

        # Validate captcha
        if user_captcha == session['captcha']:
            # Validate username and password
            if username == 'username' and password == 'password':
                return redirect(url_for('success'))
            else:
                captcha = generate_captcha()
                captcha_image = generate_captcha_image(captcha)
                session['captcha'] = captcha
                return render_template('login.html', message='Invalid username or password', captcha=captcha, captcha_image=captcha_image)
        else:
            captcha = generate_captcha()
            captcha_image = generate_captcha_image(captcha)
            session['captcha'] = captcha
            return render_template('login.html', message='Invalid captcha', captcha=captcha, captcha_image=captcha_image)
            

    captcha = generate_captcha()
    captcha_image = generate_captcha_image(captcha)
    session['captcha'] = captcha
    return render_template('login.html', captcha=captcha, captcha_image=captcha_image)

# Success page
@app.route('/success')
def success():
    return "Login successful!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
