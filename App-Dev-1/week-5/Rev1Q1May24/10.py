from jinja2 import Template

my_gadgets = {"first":"Television","second":"Smart phone","third":"Tablet",
                           "fourth":"Computer"}

for item in my_gadgets:
     statement = Template("My {{item}} gadget is {{gadget}}.")
     print(statement.render(item = item,gadget = my_gadgets[item]))

     # my_gadgets["first"]
