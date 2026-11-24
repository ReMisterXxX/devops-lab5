import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import calculator  # noqa: E402
from app import app  # noqa: E402


def test_add():
    assert calculator.add(2, 3) == 5


def test_subtract():
    assert calculator.subtract(10, 4) == 6


def test_multiply():
    assert calculator.multiply(3, 4) == 12


def test_divide():
    assert calculator.divide(10, 4) == 2.5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        calculator.divide(1, 0)


def test_api_add():
    response = app.test_client().get("/api/add?a=2&b=3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_api_unknown_operation():
    assert app.test_client().get("/api/modulo?a=1&b=2").status_code == 404


def test_api_missing_parameters():
    assert app.test_client().get("/api/add?a=1").status_code == 400


def test_health():
    assert app.test_client().get("/health").get_json()["status"] == "ok"
