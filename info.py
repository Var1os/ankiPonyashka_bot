buffer = 5
for i in range(12):
    if i != 0:
        buffer += (buffer * 5)+2
        print(buffer)