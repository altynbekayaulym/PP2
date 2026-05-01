import re
s = input().strip()
if re.search(r'cat|dog', s):
    print("Yes")
else:
    print("No")