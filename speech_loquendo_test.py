import urllib.request
from urllib.request import urlopen
from playsound import playsound
import os

audioFolder = "./audios"
audioFile = "audio.mp3"
url ="https://cache-a.oddcast.com/tts/gen.php?EID=3&LID=1&VID=3&TXT=Are%20you%20fucking%20retarded%3F&IS_UTF8=1&ACC=3314795&API=2292376&CB=vw_mc.vwCallback&HTTP_ERR=1&vwApiVersion=2"

rooturl = ["https://cache-a.oddcast.com/tts/gen.php?EID=3&LID=1&VID=3&TXT=",
           "&IS_UTF8=1&ACC=3314795&API=2292376&CB=vw_mc.vwCallback&HTTP_ERR=1&vwApiVersion=2"]
def playText(url):
    while(True):
        urllib.request.urlretrieve(url, audioFile)
        playsound(audioFile, True) #True for blocking action. Not asynchronous
        os.remove(audioFile)

#Points and exclamation signs are not replaced
characters ={
"," : "%2C",
" " : "%20",
"?" : "%3F",
"'" : "%27"
}

def parseText(phrase):
    for ch in characters:
        phrase = phrase.replace(ch,characters[ch])
        print(phrase)
    return phrase

if __name__ == "__main__":
    txt = "Hello! My name is nurse, how may I help you? It's my pleasure"
    txtUrl = parseText(txt)
    url = rooturl[0] + txtUrl + rooturl[1]
    print(url)
    urllib.request.urlretrieve(url, audioFile)

