import os

from flask import Flask, jsonify, request

from calculator import OPERATIONS

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "local")


@app.get("/")
def index():
    return jsonify({"app": "lab5-calculator", "version": APP_VERSION, "environment": APP_ENV})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/<operation>")
def calculate(operation):
    if operation not in OPERATIONS:
        return jsonify({"error": f"Nieznana operacja: {operation}"}), 404
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
        result = OPERATIONS[operation](a, b)
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e) or "Wymagane parametry a i b"}), 400
    return jsonify({"operation": operation, "a": a, "b": b, "result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
