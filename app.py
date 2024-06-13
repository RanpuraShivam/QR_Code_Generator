from flask import Flask, render_template, request, send_file
import qrcode
import os
from urllib.parse import quote

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Allowed image formats for download

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    colors = ['black', 'white', 'blue', 'red', 'green']  # Color options
    sizes = [1, 2, 3, 4, 5]  # QR code size options (modules)
    return render_template('index.html', colors=colors, sizes=sizes)

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form['url']
    color = request.form['color']
    size = int(request.form['size'])

    qr = qrcode.QRCode(version=1, box_size=size*10, border=4)  # Adjust box_size and border
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white")

    # Generate unique filename with proper escaping
    filename = f'qr_{quote(url)}.png'  # Escape special characters

    # Save image in static folder with full path (ensure the folder exists)
    img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', filename))

    return render_template('result.html', filename=filename, url=url)

@app.route('/download/<filename>')
def download_file(filename):
    if allowed_file(filename):
        return send_file(os.path.join(app.static_folder, filename), as_attachment=True)
    else:
        return 'Invalid file format.', 400

if __name__ == '__main__':
    app.run(debug=True)
