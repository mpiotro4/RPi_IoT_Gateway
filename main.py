from flask import Flask

app = Flask(__name__)


@app.route("/")
def Hell():
    return "Hello"


@app.route("/example")
def exa():
    return "<h1> This is an example </h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
