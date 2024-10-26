import sys
from jinja2 import Template

vars = sys.argv
myTech = {'mad 1': 'backend', 'mad 2': 'frontend'}

temp = Template("This course focuses on {{var}} development.")

print(vars)
# if vars[2] == 'mad 1':
#     print(temp.render(var=myTech['mad 1']))
# elif vars[2] == 'mad 2':
#     print(temp.render(var=myTech['mad 2']))
# else:
#     print("Mention the course name specifically.")
if vars[2] == 'mad 1':
    print(temp.render(var=myTech['mad 1']))
elif vars[2] == 'mad 2':
    print(temp.render(myTech['mad 2']))
else:
    print("Mention the course name specifically.")