import pyrebase
import time
import threading

config = {
  "apiKey": "AIzaSyCueeUC-97AiWzhERKmGCNa2qWSqkjiq7g",
  "authDomain": "shesh-besh.firebaseapp.com",
  "databaseURL": "https://shesh-besh.firebaseio.com",
  "storageBucket": "shesh-besh.appspot.com",
  "serviceAccount": "C://Users//lidor//PycharmProjects//untitled//shesh-besh-firebase-adminsdk-ujskc-b2a6f1e811.json"
}
invitelistener=0
lock = threading.Lock()
firebase = pyrebase.initialize_app(config)
global db
haveagame=threading.Lock()
startplay=False
db= firebase.database()
ingame = 2
def createuser():
    data = {"state": "waiting", "mymsg":""}
    numofplayer = db.child("users").push(data)
    return numofplayer['name']
global myid
def findapartner(numofplayer):
    global haveagame
    global lock
    global ingame
    myid=numofplayer
    users_by_key = db.child('users').order_by_child('state').equal_to("waiting").get()
    print(users_by_key.val())
    for user in users_by_key.each():
        if user.key() < numofplayer:
            with lock:
                db.child("users").child(user.key()).update({'mymsg': "invite" + numofplayer, 'state': "invited"})
                my_stream = db.child("users").child(user.key()).stream(waitingforrespond)
                time.sleep(12)
                if db.child("users").child(user.key()).child('state').get().val() == "invite" + numofplayer:
                    ingame = 0
                my_stream.close()
                if ingame==3:
                    return
                if ingame == 0:
                    deleteAuser(user.key())
                elif ingame == 1:
                    db.child("users").child(myid).update({'mymsg': "OK" + numofplayer})
                    startgame(numofplayer,user.key())
                    ingame=3
mygamenum=0
def listentogame(msg):
    global mygamenum
    global startplay
    if msg['data'] == None or not 'state' in msg['data'].keys() or msg['data']["state"] == 'waiting' or msg['data']["state"] == 'invited':
        return
    mygamenum = msg['data']['state']
    startplay = True

def waitingforrespond(msg):
    global lock
    global ingame
    if ingame == 1 or ingame==3:
         return
    if msg["data"] == None:
        return
    if "mymsg" in msg["data"].keys() and msg["data"]["mymsg"]=="OK"+myid:
        ingame=1
    if "mymsg" in msg["data"].keys() and msg["data"]["mymsg"][0:2] == "OK" and msg["data"]["mymsg"] != "OK"+myid:
        ingame=2

def reacttoinvite(msg):
    global ingame
    global lock
    global myid
    with lock:
        if msg["data"] == None:
            return
        if ingame == 1 or ingame==3:
            return
        if msg["data"]["mymsg"][0:6] == "invite":
            db.child("users").child(myid).update({'mymsg': "OK" + msg["data"]["mymsg"][6:]})
           # if myid>msg["data"]["mymsg"][6:]:
            #    startgame(myid,msg["data"]["mymsg"][6:])
            ingame=3


def startgame(player1,player2):
    data={"player1": player1, "player2": player2}
    numofgame= db.child("games").push(data)
    db.child("games").child(numofgame).child('qubes').set({})
    db.child("users").child(player2).update({"state": numofgame['name']})
    db.child("users").child(player1).update({"state": numofgame['name']})
    return numofgame

def endgame(numofgame):
    users = db.child("users").get()
    game=db.child("games").child(numofgame).get()
    for user in users.each():
        if game["player1"]==user or game["player1"]==user:
            db.child("users").child(user.key()).update({"state": "waiting"})

def deleteAuser(numofuser):
    db.child("users").child(numofuser).remove()

def getmydir():
    mygame= db.child('games').child(mygamenum).get()
    if mygame.val()['player1'] > myid or mygame.val()['player2'] > myid:
        return 0
    return 1


def updatequbes(left, right, num_of_drop):
    db.child("games").child(mygamenum).child('qubes').update({"left": left, "right": right, "num_of_drop": num_of_drop})


approval_move = False
lock_approval_move = threading.Lock()
def update_game_move(origin, target, num_of_movement):
    global approval_move, lock_approval_move
    with lock_approval_move:
        approval_move = False
        db.child("games").child(mygamenum).child('accept').set({})
        db.child("games").child(mygamenum).child('movement').update({"origin": origin, "target": target, "num_of_movement": num_of_movement})
        accept_move_listener = db.child("games").child(mygamenum).child('accept').stream(move_accepted)
        while not approval_move:
            time.sleep(0.25)
        accept_move_listener.close()
        print("end doing move")

def zero_movement():
    with lock_approval_move:
      db.child("games").child(mygamenum).child('movement').update({"origin": 0, "target": 0})


def move_accepted(msg):
    global approval_move
    print("accept: ",   msg)
    if approval_move:
        return
    approval_move = not msg['data'] is None and msg['path'] == '/' and 'is_accepted' in msg['data'].keys()

def accept_move():
    db.child("games").child(mygamenum).child('accept').update({"is_accepted": "yes"})

def change_player():
    whoplay = db.child("games").child(mygamenum).child('side').get()
    db.child("games").child(mygamenum).child('side').update({'whoplay': (whoplay.val()['whoplay']+1)%2})







