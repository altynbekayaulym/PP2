n = int(input())
cnt = {}

for i in range(n):
    number = input().strip()
    if number in cnt:
        cnt[number] += 1
    else:
        cnt[number] = 1

answer = 0
for number in cnt:
    if cnt[number] == 3:
        answer += 1

print(answer)
