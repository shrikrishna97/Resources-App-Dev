from string import Template
g = 'GET'
p = 'POST'

statement = "$g http method is used to retrieve information while $p for sending information"

out = Template(statement)

# print(=== OUTPUT ===)

print(out.substitute({'g':'GET'}))

print(out.substitute({'g':'GET','p':'POST', 'd': 'delete'}))


print(out.safe_substitute({'g':'GET'})) #print var as it is


print(out.safe_substitute({'g':'GET','p':'POST', 'd': 'delete'}))



