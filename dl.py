
with open('downloads.txt') as f:
    for line in f:
        items = eval(line)
        url = items[1]
        command = str(f"twitch-dl download -q source {url}")
        print (command)        
                
        
