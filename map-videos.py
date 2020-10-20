import os
all_items = []
with open('downloads.txt') as f:
    for line in f:
        items = list(eval(line))
        all_items.append(items)
                  
for item in all_items:
    url = item[0]
    for file in os.listdir('.'):
        if url.lower() in file.lower():
            item.append(file)
            break
for item in all_items:
    print(item)
    
print(len(all_items))
            
    