import sys
from jinja2 import Template

vars = sys.argv
myTech = {'Apple': 'backend', 'mad2': 'frontend', "v" : "Apple"}

temp = Template("This course focuses on {{v}} development.")

# if vars[2] == 'mad1':
    # print(temp.render(v=myTech['mad1']))
print(temp.render(myTech))
# elif vars[2] == 'mad2':
    # print(temp.render(v=myTech['mad2']))
print(temp.render(v=myTech['mad2']))
# else:
    # print("Mention the course name specifically.")

