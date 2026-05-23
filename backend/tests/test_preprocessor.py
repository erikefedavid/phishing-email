import pytest
from app.services.preprocessor import preprocess


def test_strip_html():
    result = preprocess("<html><body>Hello <b>world</b></body></html>")
    assert "hello" in result
    assert "world" in result
    assert "<html>" not in result


def test_lowercase():
    result = preprocess("HELLO World")
    assert result == "hello world"


def test_whitespace_normalized():
    result = preprocess("hello    world")
    assert result == "hello world"


def test_empty_string():
    result = preprocess("")
    assert result == ""
