import re
a = input()
b = input()
m = re.search(b,a)
if m:
    print("Yes")
else:
    print("No")