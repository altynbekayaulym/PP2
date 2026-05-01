import re
s = input().strip()
sequences = re.findall(r'\d{2,}', s)
print(" ".join(sequences))