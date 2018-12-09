from flask import Flask, render_template, url_for, request, send_from_directory
from flask_bootstrap import Bootstrap
from mandelbrot import Mandelbrot
from flask import jsonify


import numpy as np


m = Mandelbrot(2, 50)


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)


@app.route("/api", methods=['GET', 'POST'])
def mandelbrotAPI():
    if request.method == 'POST':
        json = request.get_json(force=True)
        limits = json['limits']
        img_width = int(json['img_width'])
        img_height = int(json['img_height'])
        print('Generating image')
        img = m.genImage(limits, img_width, img_height)

        print('Adding alpha')
        alpha = np.ones((img_height, img_width))
        img = np.dstack([img, alpha])

        print('Flattening')
        img = img * 255
        img = img.flatten()
        img = img.astype('uint8')

        print('Jsonifying')
        resp = jsonify(
            img=img.tolist()
        )

        print('Done')
        print(resp)
        return resp


if __name__ == '__main__':
    app.run(debug=True)
