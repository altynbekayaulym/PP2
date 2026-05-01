import re
s = input().strip()
pattern = input().strip()
parts = re.split(pattern, s)
print(",".join(parts))