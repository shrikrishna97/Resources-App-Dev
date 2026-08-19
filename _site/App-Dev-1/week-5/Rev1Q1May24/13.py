from jinja2 import Template as T1
from string import Template as T2

info = {'city1': 'Mumbai', 'city2': 'Delhi',
        'city3': 'city2', 'city4': 'city1',
        'country1':'India', 'country2':'country1'}

t1 = T1("${{city3}} and ${{city4}} are the national and financial capitals of ${{country2}} respectively.")
# t1 = T2("{{$city3}} and {{$city4}} are the national and financial capitals of {{$country2}} respectively.")

out1 = t1.render(info)
# out1 = t1.substitute(info)
print(out1)
out2 = T2(out1)
# out2 = T1(out1)
print(out2.substitute(info))
# print(out2.render(info))