import re
a = input()
b = input()
m = re.finditer(re.escape(b),a)
cnt = sum(True for i in m)
print(cnt)