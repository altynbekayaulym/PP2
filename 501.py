import re
a = input()
m = re.match("Hello",a)
if m:
    print("Yes")
else:
    print("No")