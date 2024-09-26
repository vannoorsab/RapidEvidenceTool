from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join('uploads', file.filename))
        return 'File uploaded successfully'
    return 'File upload failed'

if __name__ == '__main__':
    app.run(debug=True)
