# import pytest



# @pytest.fixture
# def sample_list():
#     return [salary(100,10), salary(200,20), salary(300,30)]

# def salary(base, bonus=10):
#     return base + bonus

# def test_sum(sample_list):
#     assert sum(sample_list) == 660

# import pytest

# @pytest.mark.parametrize("a,b,result", [(1, 2, 3), (3, 4, 5), (5, 5, 10)])
# def test_addition(a, b, result):
#     assert a + b == result

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'