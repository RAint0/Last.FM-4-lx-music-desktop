import pylast
import os
import json
import requests
import sseclient
import threading
import datetime
import time
import webbrowser
from win11toast import toast

# ⛔ 这里的API_KEY和API_SECRET仅仅是示例，你需要替换为你自己Last.FM的API_KEY和API_SECRET
# 🔑 申请地址： https://www.last.fm/api/account/create
API_KEY="b893f2ffe7a47ae04061766b3da5b21b"
API_SECRET="693bcc6913b6c9e4f10a5a424904a369"

SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")
network = pylast.LastFMNetwork(API_KEY, API_SECRET)
if not os.path.exists(SESSION_KEY_FILE):
    skg = pylast.SessionKeyGenerator(network)
    url = skg.get_web_auth_url()

    print(f"Please authorize this script to access your account: {url}\n")

    # 🌟 这里会自动跳转到last.FM进行验证登录以获取session_Key 
    # 🎄 只需要获取一次，如果要更换last.Fm账户请删除 ~/.session_key以重试(~表示用户目录,在windows下为C:\Users\用户名\)
    webbrowser.open(url)

    while True:
        try:
            session_key = skg.get_web_auth_session_key(url)
            with open(SESSION_KEY_FILE, "w") as f:
                f.write(session_key)
            break
        except pylast.WSError:
            time.sleep(1)
else:
    session_key = open(SESSION_KEY_FILE).read()

# 🎷以下代码为通过SSE订阅LX_Music的事件
network.session_key = session_key
reqUrl = "http://127.0.0.1:23330/subscribe-player-status"
params = {
    "filter":"status,name,singer,duration,collect"
}
headers = {'Accept': 'text/event-stream'}
request = requests.get(reqUrl, stream=True, headers=headers, params=params)
client = sseclient.SSEClient(request)
print("Listening for events...")

singerChange = False
nameChange = False
ready = False
track = None
singer = ""
name = ""
playDuration = 0
duration = 0
collect = False
status = ""
start_time = -1

# 🎸 这里是scrobbling的逻辑，当切歌或LX_Music软件退出时，会调用scrobbling函数
def scrobbling(track,playDuration,duration,status,start_time):
    # 🎤 如果track不为空，说明有歌曲正在播放
    if track:
        print("### track:",track.artist,track.title)
        print(duration,playDuration)
        # 🦖 如果正在播放，累计播放时间
        if status == "playing" and start_time != -1:
            playDuration += time.time() - start_time

        # 🦖 只有当音乐时长至少30s,且播放时间至少为时长的一半或播放时长超过4分钟才记录
        if duration>=30 and playDuration >= duration/2 or playDuration >= 240:
            print("playDuration:",playDuration," duration:",duration)
            print("!!! Scrobbling", rack.artist, "-", track.title, flush=True)
            toast("Scrobbling", track.artist+"-"+track.title) # 📣 弹出通知
            scrobbleResult=network.scrobble(track.artist, track.title, int(time.mktime(datetime.datetime.now().timetuple())))

try:
    for event in client.events():
        data = json.loads(event.data)
        print("#",event.event," ",data, flush=True)
        if event.event == "singer":
            singer = data
            singerChange = True
        elif event.event == "name":
            name = data
            nameChange = True
        elif event.event == "duration":
            if data > 30:
                duration = data
            print("@duration:",duration , type(data))
        elif event.event == "collect":
            collect = data
        elif event.event == "status":
            status = data

        # 🐬 判断是否可以scrobble（收集到新的歌手和歌名了）
        if(singerChange and nameChange):
            print("!!! Ready to scrobble", singer+"-"+name)
            track = network.get_track(singer, name)
            ready = True
            singerChange = False
            nameChange = False

        # ❓ 如果歌手和歌名有一方先变动，说明切歌了
        elif(singerChange!=nameChange):
            ready = False
            scrobbling(track,playDuration,duration,status,start_time)
            track = None
            playDuration = 0
            start_time = -1
            duration = 0
            collect = False

        if ready:
            if collect:

                # ❤️ 如果收藏了，就记录为love
                track.love()
                collect = False
                print("!!! Loved", singer, "-", name, flush=True)
            if status == "playing" and start_time == -1:
                start_time = time.time()

                # ▶️ 记录为正在播放  
                playingResult=network.update_now_playing(singer, name)
                # print("!!! Playing", singer, "-" , name, flush=True)
                toast("Playing", singer+"-"+name) # 📣 弹出通知
                # print("start_time:",start_time)
            elif status != "playing" and start_time!=-1:
                # ⏹️ 暂停或异常时，累计一次播放时间
                playDuration += time.time() - start_time      
                start_time = -1
                # print("end_time:",time.time())
                # print("playDuration:",playDuration," duration:",duration)              
            

except Exception as e:
    print(e)
    toast("Exit","LastFM4LX") # 📣 弹出通知
finally:
    scrobbling(track,playDuration,duration,status,start_time)
