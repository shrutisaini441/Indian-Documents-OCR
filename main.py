from flask import Flask
from api.ocr import OCR_app

app = Flask(__name__)
app.register_blueprint(OCR_app)


@app.route('/')
def index():
    return "backend of OCR app"


if __name__ == '__main__':
    app.run(debug=True)
