#!/usr/bin/python3
import signal
import sys
import requests as req
from os import _exit
import os
statuso={0:"\033[91mdisabled\033[0m",
1:"\033[92menabeld\033[0m"}
API_KEY=None
PREFIX=None
if str(os.path.expanduser('~')).count("/")>=1:
    PREFIX=str(os.path.expanduser('~'))+"/"+".local2net_geras_api"
else:
    PREFIX=str(os.path.expanduser('~'))+"\\"+".local2net_geras_api"
def saver():
    global API_KEY
    try:
        apiikey=input("type your api key here for save : ")
        fileman=open(PREFIX,"w")
        fileman.write(apiikey)
        API_KEY=apiikey
    except Exception as e:
        print(e)
        _exit(1)
try:
    fileman=open(PREFIX,"r")
    API_KEY=fileman.read()
    fileman.close()
except:
    saver()
print("your api key : ",API_KEY)
TOKEN=None
ID=None
STOP=False
START=False
header={"accept":"*/*",
"Authorization":f"Bearer {API_KEY}"}
def api(f):
    return f"https://localtonet.com/api/{f}"

print("just waiting ...")
def GetToken():
    global TOKEN
    url=api("GetAuthTokens")
    r=req.get(url=url,headers=header)
    if r.status_code==200:
        try:
            j=r.json()
            k=j["result"][0]["token"]
            print("login sucess : token :",k)
            TOKEN=k
        except Exception as e:
            print(e)
            _exit(1)
    else:
        print(f"error code : {r.status_code}\n",r.text)
        ppp=input("you need to change api key ? y/n : ")
        if ppp.lower()=="y":
            saver()
            print("you can restart the tool now !!")
        _exit(1)
def GetTunnels():
    global ID
    url=api("GetTunnels")
    r=req.get(url=url,headers=header)
    if r.status_code==200:
        try:
            j=r.json()
            k=j["result"]
            
            ids=[]
            for i,id in enumerate(k):
                ids.append(id["id"])
                print("id"+str(i)+") = : \033[92m",id["id"],"\033[0m\n\t","serverDomain : ",id["serverDomain"],"\n\t",
                "local host:port = ",id["clientIp"]+":"+str(id["clientPort"]),"\n\t",
                "protocolType : ",id["protocolType"],"\nstatus : ",statuso[id["status"]])
            chosser=-1
            while chosser not in ids:
                if chosser !=-1:
                    print("please type valid id ")
                try:
                    chosser= int(input("\033[92mchoose the ID and type it\033[0m : "))
                except:
                    print("not type strings or float values ")
                    jjj=input("u want to exit y/n ? : ")
                    if jjj.lower()=="y":
                        _exit(1)
                    chosser=-1
            ID=chosser
        except Exception as e:
            print(e)
            _exit(1)
    else:
        print(f"error code : {r.status_code}\n",r.text)
        _exit(1)

def StartTunnel():
    url=api("StartTunnel/"+str(ID))
    r=req.get(url=url,headers=header)
    if r.status_code==200:
        try:
            j=r.json()          
            if j["hasError"]==True:
                print(j)
                if list(j["errors"]).count('Please Start or Update localtonet app!')==1:
                    print("before this tool , start the \033[92m./localtonet\033[0m command into second terminal !")
            else:
                print("check the port now")
        except Exception as e:
            print(e)
            _exit(1)
    else:
        print(f"error code : {r.status_code}\n",r.text)
        _exit(1)
def StopTunnel():
    url=api("StopTunnel/"+str(ID))
    r=req.get(url=url,headers=header)
    if r.status_code==200:
        try:
            j=r.json()          
            if j["hasError"]==True:
                print(j)
                if list(j["errors"]).count('Please Start or Update localtonet app!')==1:
                    print("before this tool , start the \033[92m./localtonet\033[0m command into second terminal !")
            else:
                print("check the port now")
        except Exception as e:
            print(e)
            _exit(1)
    else:
        print(f"error code : {r.status_code}\n",r.text)
        _exit(1)
def signal_handler(sig, frame):
    print("just wait for close ...")
    if START==False:
        sys.exit(0)
    else:
        try:
            if STOP==True:
                sys.exit(0)
            StopTunnel()
            STOP=True
        except:
            sys.exit(0)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
GetToken()
GetTunnels()
yy=["start","stop","exit"]
y="zaprago"
while y.lower() not in yy:
    y=input("do you  \033[92mstart\033[0m the port or  \033[92mstop\033[0m or  \033[92mexit\033[0m : "+
    "\ntype  \033[92mstart\033[0m or  \033[92mstop\033[0m or  \033[92mexit\033[0m : ")
if y.lower()=="exit":
    _exit(1)
elif y.lower()=="stop":
    StopTunnel()
else:
    StartTunnel()
    START=True
_exit(1)