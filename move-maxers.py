import os
urls = []
with open('downloads.txt') as f:
    for line in f:
        items = eval(line)
        urls.append(items[0])
                  
        
for item in os.listdir('.'):
    for url in urls:
        if url in item:
            os.move(item, 'maxers/'+item)