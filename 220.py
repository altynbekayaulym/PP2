import sys
input = sys.stdin.readline
n = int(input())
doc = {}
for i in range(n):
    line = input()
    if line.startswith('set'):
        i, key, value = line.strip().split()
        doc[key] = value
    else: 
        key = line[4:].strip()
        if key in doc:
            print(doc[key])
        else:
            print(f"KE: no key {key} found in the document")
