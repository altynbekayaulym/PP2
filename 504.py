import re
a = input()
b = re.findall(r'\d',a)
print(' '.join(b))