import json
import os

def TryParseInt(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

def removeItems(line, pairs):
    for pair in pairs:
        line = line.replace(pair[0],pair[1])
    return line
    
game_line_pairs = [
    (",", " "), 
    ("-", " "), 
    ("at", ""), 
    ("(", ""),
    (")", "")
]

def game_line(line):
    return removeItems(line, game_line_pairs)
    
            
class Game:
    def __init__(self, line):
        self.score = None
        self.timestamp = None
        self.line = line
        self.parts = None
        try:
            self.parseLine(line)
        except Exception as e:
            print(e, line)
            return
            
    def parseLine(self, line):
        line = game_line(line)
        parts = line.split()
        self.parts = parts
        first_el_index = None
        if len(parts[0]) == 3 and len(parts[1]) == 3:
            score = int(parts[0] + parts[1])
            self.score = score
            first_el_index = 2
        elif len(parts[0]) == 6:
            score = int(parts[0])
            self.score = score
            first_el_index = 1
        else:
            return
        
                
        hour = None
        minute = None
        second = None
        
        first_el = parts[first_el_index].strip()
        
        try:            
            if ('h' in first_el and 
                'm' in first_el and 
                's' in first_el):
                
                h_index = first_el.index('h')
                m_index = first_el.index('m')
                s_index = first_el.index('s')
                hour = (first_el[0:h_index])
                minute = (first_el[h_index+1:m_index])
                second = (first_el[m_index+1:s_index])  
                
            elif 'h' in first_el and 'm' not in first_el:
                hour = parts[first_el_index].replace('h','').strip()
                minute = parts[first_el_index+1].replace('m','').strip()
                second = parts[first_el_index+2].replace('s','').strip()
            elif len(first_el) >= 5:
                
                hms = first_el.split(":")
                
                if len(hms) == 3:
                    hour = hms[0]
                    minute = hms[1]
                    second = hms[2]
                elif len(hms) == 2:
                    hour = 0
                    minute = hms[0]
                    second = hms[1]
            
        except Exception as e:
            print ("Game fail parse time", parts)
            print (e)
        
        if (hour is not None and
            minute is not None and 
            second is not None):
            self.timestamp = (hour,minute,second)
        
    def valid(self):
        return (self.score is not None
            and self.timestamp is not None)
        
    def __str__(self):
        return (self.line + "\n" +
        str(self.score) + " : " + str(self.timestamp))
        
class Qualifier:
    def __init__(self):
        self.vod = None
        self.player = None
        self.twitch = None
        self.games = []
        self.gameFlag = False
        
    def parseLine(self, line):
        line = line.strip()
        lowerline = line.lower()
        
        if lowerline.startswith("vod"):
            self.vod = ":".join(line.split(":")[1:]).strip()
        elif lowerline.startswith("name"):
            self.player = line.split(":")[1].strip()
        elif lowerline.startswith("twitch"):
            try:
                self.twitch = line.split(":")[1].strip()
            except:
                self.twitch = lowerline.replace("twitch","").strip()
            self.gameFlag = True
        elif lowerline.startswith("submit"):
            self.gameFlag = True
        elif self.gameFlag:
            game = Game(line)
            if game.valid():
                self.games.append(game)
            else:
                print ("Error parsing line:" + line, game.parts)
    
    def __str__(self):
        game_str = "\n".join([str(game) for game in self.games])
        return (f"VOD: {self.vod}\n" +
               f"Player: {self.player}\n" +
               f"Twitch: {self.twitch}\n" +
               f"Games:\n" + 
               game_str)
    
def load_player_vid_map():
    result = {}
    with open("maxer-videos.txt") as f:
        for line in f:
            items = eval(line)
            print(items)
            result[items[0].lower()] = items[3].lower()
    return result
    
def generate_timestamp(data):
    h,m,s = data
    h = int(h)
    m = int(m)
    s = int(s)
    s -= 5
    if s < 0:
        s += 60
        m -= 1
    if m < 0:
        m += 60
        h -= 1
    if h < 0:
        h = 0
        m = 0
        s = 0
    return ("%02d" % h +":"+
           "%02d" % m +":"+
           "%02d" % s)
        
VIDEO_ROOT = "T:/ctwc-qual/maxers/"
if __name__ == '__main__':
    data = {}
    with open("qualifier.json") as f:
        data = json.load(f)
    video_map = load_player_vid_map()
    
    quals = []
        
    for item in data["messages"]:
        content = item["content"]
        lines = content.split("\n")
        q = Qualifier()
        for line in lines:
            q.parseLine(line)
        quals.append(q)
        
    to_download = []
    num_max = 0
    quals.sort(key=lambda x: x.games[0].score, reverse=True)
    for qual in quals:        
        for i, game in enumerate(qual.games):
            if game.score == 999999:
                qual.video = VIDEO_ROOT + video_map[qual.twitch.lower()]
                timestamp = generate_timestamp(game.timestamp)
                print (f"ffmpeg -i {qual.video} -ss {timestamp} -t 600 -c:v copy {VIDEO_ROOT}{qual.twitch}{i+1}.mp4")
            else:
                break
        
    
        