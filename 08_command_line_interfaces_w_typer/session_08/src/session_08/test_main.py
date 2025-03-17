import pytest
from typer.testing import CliRunner
from .main import app

runner = CliRunner()

# Greeting Tests

def test_greeting_empty_name():
    result = runner.invoke(app, ["hello"])
    assert "Welcome aboard!" in result.stdout

def test_greeting_random_name():
    result = runner.invoke(app, ["hello","--name","JohnDoe"])
    assert "Welcome aboard, JohnDoe!" in result.stdout

def test_formal_greeting_empty_name():
    result = runner.invoke(app, ["hello","--formal"])
    assert "Salutations and warmest regards!" in result.stdout

def test_formal_greeting_random_name():
    result = runner.invoke(app, ["hello","--formal","--name","JohnDoe"])
    assert "Salutations and warmest regards, Mx. JohnDoe!" in result.stdout
