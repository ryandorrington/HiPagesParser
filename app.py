from typing import List
from flask import Flask, render_template
import os

app = Flask(__name__)
messages: List[str] = ["placeholder"]


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
