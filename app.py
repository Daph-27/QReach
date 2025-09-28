from flask import Flask, render_template, request, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# In-memory QR history
history = []

# Size mapping
size_map = {'small': 200, 'medium': 300, 'large': 400}

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code = None
    url = None

    if request.method == 'POST':
        url = request.form['url']
        size_str = request.form['size']
        size = size_map.get(size_str, 300)

        # Generate QR code
        qr_img = qrcode.make(url)
        qr_img = qr_img.resize((size, size))

        # Convert to base64 for browser
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        qr_code = f"data:image/png;base64,{img_str}"

        # Save to history
        history.append({'url': url, 'qr_code': qr_code})

    return render_template('index.html', qr_code=qr_code, url=url)

@app.route('/history')
def view_history():
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
