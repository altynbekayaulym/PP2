import re
s = input().strip()
words = re.findall(r'\b\w{3}\b', s)
print(len(words))