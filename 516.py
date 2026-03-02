import re
s = input().strip()
match = re.match(r'Name: (.+), Age: (.+)', s)
if match:
    name = match.group(1)
    age = match.group(2)
    print(name, age)