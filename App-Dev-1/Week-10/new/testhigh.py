import math
import pytest
# @pytest.mark.xfail
@pytest.mark.hello
def test_sqrt():
   num = 25
   assert math.sqrt(num) == 6
@pytest.mark.skip
@pytest.mark.hello
def testsquare():
   num = 7
   assert 7*7 == 49
@pytest.mark.other  
def test_addition():
    assert 1 + 1 == 2   

