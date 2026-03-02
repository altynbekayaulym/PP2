import re
s = input().strip()
words = re.findall(r'\w+', s)
print(len(words))