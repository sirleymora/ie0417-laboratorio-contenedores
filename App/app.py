from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    mensaje = os.environ.get("MENSAJE", "Hola desde Flask en Docker")
    return f"""
    <h1>{mensaje}</h1>
    <p>Este texto lo cambié desde mi computadora.</p>
    """


@app.route("/info")
def info():
    return {
        "app": "Laboratorio de contenedores",
        "curso": "IE0417",
        "tema": "Docker"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
