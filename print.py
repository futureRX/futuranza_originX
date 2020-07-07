action = []
for i in range(8):
    x = i+1
    y = x * -1
    action.append((x,y))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((y,x))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((x,x))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((y,y))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((x,0))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((y,0))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((0,x))
for i in range(8):
    x = i+1
    y = x * -1
    action.append((0,y))

print(action)