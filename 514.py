import re
s = input().strip()
pattern = re.compile(r'^\d+$')
if pattern.match(s):
    print("Match")
else:
    print("No match")