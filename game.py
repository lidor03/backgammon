from graphics import *
from PIL import Image
import win32api
import random
from win32api import GetSystemMetrics
from graphics import *
from time import sleep
import firebase
import threading

boardlocker=threading.Lock()





numofplayer=0
class player(object):
    def __init__(self, color, stack,point):
        self.color = color
        self.inhouse = False
        self.stack = stack
        self.dir = 1
        if color == "white":
            self.dir = -1
            self.house = 24
        else:
            self.dir = 1
            self.house = -1
        self.point=Circle(point,3)
        self.point.setFill("red")

    def setinhouse(self, bool):
        self.inhouse = bool


class qube(object):
    def __init__(self,p1,p2,p3,p4,win):
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.p4=p4
        self.win=win
        middlex=(p1.getX()+p2.getX())/2
        middley=(p1.getY()+p3.getY())/2
        middlepoint=Point(middlex,middley)
        thirdx=(-p1.getX()+p2.getX())/4
        thirdy=((-p1.getY()+p3.getY())/4)
        leftup=Point(p1.getX()+thirdx,p1.getY()+thirdy)
        rightup=Point(p1.getX()+3*thirdx,p1.getY()+thirdy)
        middleright=Point(p1.getX()+thirdx,p1.getY()+2*thirdy)
        middleleft=Point(p1.getX()+3*thirdx,p1.getY()+2*thirdy)
        rightdown=Point(p1.getX()+thirdx,p1.getY()+3*thirdy)
        leftdown=Point(p1.getX()+3*thirdx,p1.getY()+3*thirdy)
        self.num=[[0],[6,2],[0,6,2],[5,6,1,2],[0,5,6,1,2],[4,5,1,2,3,6]]
        self.point=[Circle(middlepoint,3),Circle(leftup,3),Circle(rightup,3),Circle(middleleft,3),Circle(middleright,3),Circle(leftdown,3),Circle(rightdown,3)]
        self.val=1
        self.cube = Polygon([self.p1, self.p2, self.p3, self.p4])
    def create(self,val):
        self.val=val
        self.cube.setFill("white")
        self.cube.draw(self.win)
        for i in range(len(self.num[val-1])):
            self.point[self.num[val-1][i]].setFill("black")
            self.point[self.num[val-1][i]].draw(self.win)
    def gray(self):
        self.cube.undraw()
        for i in range(len(self.num[self.val-1])):
            self.point[self.num[self.val-1][i]].undraw()
            self.point[self.num[self.val - 1][i]].setFill("gray")
        self.cube.setOutline("gray")
        self.cube.draw(self.win)
        for i in range(len(self.num[self.val-1])):
            self.point[self.num[self.val-1][i]].draw(self.win)
    def remove(self):
        self.cube.undraw()
        for i in range(len(self.num[self.val-1])):
            self.point[self.num[self.val-1][i]].undraw()



class triangle(object):
    def __init__(self, corner1, corner2, corner3, color, numofplayers, radius, win):
        self.numofplayers = numofplayers
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.players = {}
        self.color = color
        self.radius = radius
        self.win = win
        self.up = [radius, 3 * radius, 5 * radius, 7 * radius, 9 * radius, radius + 5, 3 * radius + 5, 5 * radius + 5,
                   7 * radius + 5, 9 * radius + 5, radius + 10, 3 * radius + 10, 5 * radius + 10, 7 * radius + 10,
                   9 * radius + 10, radius + 6, 3 * radius + 6, 5 * radius + 6, 7 * radius + 6, 9 * radius + 6,
                   radius + 8, 3 * radius + 8, 5 * radius + 8, 7 * radius + 8, 9 * radius + 8, radius, 3 * radius,
                   5 * radius, 7 * radius, 9 * radius]
        if self.corner3.getY() > self.corner1.getY():
            self.sign = Circle(Point(corner3.getX(), corner3.getY() + 3), 3)
        else:
            self.sign = Circle(Point(corner3.getX(), corner3.getY() - 3), 3)
        self.sign.setFill("red")

    def create(self):
        vertices = [self.corner1, self.corner2, self.corner3]
        tri = Polygon(vertices)
        tri.setFill('SaddleBrown')
        tri.setWidth(0)  # width of boundary line
        tri.draw(self.win)
        self.locateplayers()

    def locateplayers(self):
        i = 0
        self.middle = ((self.corner1).getX() + (self.corner2).getX()) / 2
        if (self.corner1).getY() < (self.corner3).getY():
            locy = (self.corner1).getY() + self.radius
            while i < self.numofplayers:
                locy = 50 + self.up[i]
                cir = Circle(Point(self.middle, locy), self.radius)
                cir.setFill(self.color)
                self.players[i] = cir
                (self.players[i]).draw(self.win)
                i = i + 1
        else:
            while i < self.numofplayers:
                locy = (self.corner1).getY() - self.up[i]
                cir = Circle(Point(self.middle, locy), self.radius)
                cir.setFill(self.color)
                self.players[i] = cir
                (self.players[i]).draw(self.win)
                i = i + 1

    def isup(self):
        return self.corner1.getY() < self.corner3.getY()

    def remove(self):
        if self.numofplayers == 1:
            self.color = "no"
        self.numofplayers = self.numofplayers - 1
        cir = self.players[self.numofplayers]
        self.players.popitem()
        return cir

    def add(self, cir, color):
        print("try to add")
        self.players[self.numofplayers] = cir
        if self.isup():
            dy = (self.corner1.getY() + self.up[self.numofplayers]) - cir.getCenter().getY()
        else:
            dy = (self.corner1.getY() - self.up[self.numofplayers]) - cir.getCenter().getY()
        self.players[self.numofplayers].move(self.middle - cir.getCenter().getX(), dy)
        self.numofplayers = self.numofplayers + 1
        if (self.color == "no"):
            print(self.color)
            self.color = color
        self.players[self.numofplayers - 1].undraw()
        sleep(0.5)
        print(self.players)
        self.players[self.numofplayers - 1].draw(self.win)

class stack(object):
    def __init__(self, startpoint, upordown, radius, win):
        self.startpoint = startpoint
        self.upordown = upordown
        self.radius = radius
        self.win = win
        self.up = [radius, 3 * radius, 5 * radius, 7 * radius, 9 * radius, radius + 5, 3 * radius + 5, 5 * radius + 5,
                   7 * radius + 5, 9 * radius + 5, radius + 10, 3 * radius + 10, 5 * radius + 10, 7 * radius + 10,
                   9 * radius + 10, radius + 6, 3 * radius + 6, 5 * radius + 6, 7 * radius + 6, 9 * radius + 6,
                   radius + 8, 3 * radius + 8, 5 * radius + 8, 7 * radius + 8, 9 * radius + 8, radius, 3 * radius,
                   5 * radius, 7 * radius, 9 * radius]
        self.players = {}
        self.numofplayers = 0

    def add(self, cir):
        self.players[self.numofplayers] = cir
        dy = self.startpoint.getY() + self.upordown * self.up[self.numofplayers] - cir.getCenter().getY()
        dx = self.startpoint.getX() - cir.getCenter().getX()
        self.players[self.numofplayers].move(dx, dy)
        self.numofplayers = self.numofplayers + 1
        self.players[self.numofplayers - 1].undraw()
        self.players[self.numofplayers - 1].draw(self.win)

    def remove(self):
        self.numofplayers -= 1
        cir = self.players[self.numofplayers]
        self.players.popitem()
        return cir

    def isempty(self):
        return self.numofplayers == 0


#    def remove(self):

class board(object):
    def __init__(self):
        arr = [2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 5, 5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 2]
        colors = ["Peru", "no", "no", "no", "no", "white", "no", "white", "no", "no", "no", "Peru", "white", "no", "no",
                  "no", "Peru", "no", "Peru", "no", "no", "no", "no", "white"]
        Width = GetSystemMetrics(0)
        Height = GetSystemMetrics(1)
        self.win = GraphWin('שש בש', Width, Height)
        self.white = stack(Point(Width / 2, 50), 1, 25, self.win)
        self.black = stack(Point(Width / 2, Height - 50), -1, 25, self.win)
        pointblack=Point(25,Height-53)
        pointwhite=Point(25,53)
        self.players = [player("white", self.white,pointwhite), player("Peru", self.black,pointblack)]
        # win = GraphWin('שש בש', 1400, 850) # give title and dimensions # make right side up coordinates!
        self.win.setBackground("Sienna")
        # the centeralplace
        vertices = [Point(50, 50), Point(Width - 50, 50), Point(Width - 50, Height - 50), Point(50, Height - 50)]
        square = Polygon(vertices)
        square.setFill('GoldenRod')
        square.setWidth(0)  # width of boundary line
        square.draw(self.win)
        i = 0
        k = (Width - 200) / 12
        self.up = {}
        up = {}
        while i < 6:
            p1 = Point(50 + i * k, 50)
            p2 = Point(50 + (i + 1) * k, 50)
            middle = ((50 + (i + 1) * k) + (50 + i * k)) / 2
            p3 = Point(middle, 350)
            self.up[i] = triangle(p1, p2, p3, colors[i], arr[i], 25, self.win)
            self.up[i].create()
            p1 = Point(50 + i * k, Height - 50)
            p2 = Point(50 + (i + 1) * k, Height - 50)
            p3 = Point(middle, Height - 350)
            self.up[23 - i] = triangle(p1, p2, p3, colors[23 - i], arr[23 - i], 25, self.win)
            self.up[23 - i].create()
            i = i + 1
        j = 0
        while j < 6:
            left = Width / 2 + 50 + j * k
            right = Width / 2 + 50 + (j + 1) * k
            p1 = Point(left, 50)
            p2 = Point(right, 50)
            middle = (left + right) / 2
            p3 = Point(middle, 350)
            self.up[j + 6] = triangle(p1, p2, p3, colors[j + 6], arr[j + 6], 25, self.win)
            self.up[j + 6].create()
            p1 = Point(left, Height - 50)
            p2 = Point(right, Height - 50)
            p3 = Point(middle, Height - 350)
            self.up[17 - j] = triangle(p1, p2, p3, colors[17 - j], arr[17 - j], 25, self.win)
            self.up[17 - j].create()
            j = j + 1
        # the middle wood
        vertices = [Point((Width / 2) - 50, 50), Point((Width / 2) - 50, Height - 50),
                    Point((Width / 2) + 50, Height - 50), Point((Width / 2) + 50, 50)]
        square = Polygon(vertices)
        square.setFill('Sienna')
        square.setWidth(0)  # width of boundary line
        square.draw(self.win)
        line = Line(Point(Width / 2, 50), Point(Width / 2, Height - 50))
        line.setWidth(1)
        line.setFill('black')
        line.draw(self.win)
        whitecube1=qube(Point(Width/4-25,Height/2-25),Point(Width/4+25,Height/2-25),Point(Width/4+25,Height/2+25),Point(Width/4-25,Height/2+25),self.win)
        whitecube2 = qube(Point(Width / 4 - 25+60, Height / 2 - 25), Point(Width / 4 + 25+60, Height / 2 - 25),Point(Width / 4 + 25+60, Height / 2 + 25), Point(Width / 4 - 25+60, Height / 2 + 25), self.win)
        blackcube1 = qube(Point(3*Width / 4 - 25, Height / 2 - 25), Point(3*Width / 4 + 25, Height / 2 - 25),Point(3*Width / 4 + 25, Height / 2 + 25), Point(3*Width / 4 - 25, Height / 2 + 25), self.win)
        blackcube2 = qube(Point(3*Width / 4 - 25 + 60, Height / 2 - 25), Point(3*Width / 4 + 25 + 60, Height / 2 - 25),Point(3*Width / 4 + 25 + 60, Height / 2 + 25), Point(3*Width / 4 - 25 + 60, Height / 2 + 25), self.win)
        self.cubes=[whitecube1,whitecube2,blackcube1,blackcube2]
        self.val=[]
        global  numofplayer
        # Use Polygon object to draw the triangl
        gamelistener = firebase.db.child('users').child(numofplayer).stream(firebase.listentogame)
        waitingmsg = Text(Point(3 * Width /4  - 25 + 60, Height / 2 - 25), 'waiting for partner...')
        waitingmsg.setSize(25)
        while not firebase.startplay:
            sleep(1)
            waitingmsg.draw(self.win)
            sleep(2)
            waitingmsg.undraw()
        gamelistener.close()
        self.whoami = firebase.getmydir()
        self.whoplay = -1
        self.side_stream = None
        self.num_of_drop = 0
        if self.whoami == 0:
            firebase.db.child("games").child(firebase.mygamenum).child('side').update({'whoplay': random.randint(0,1)})
        self.myside = threading.Condition()
        self.listen_to_qube = firebase.db.child('games').child(firebase.mygamenum).child('qubes').stream(self.qubeslistener)
        t2=threading.Thread(target=self.makingamove)
        t2.start()
        self.win.mainloop(0)
        #self.makingamove()

    def side_listener(self,msg):
        print("side_lis:   ", msg)
        if msg['data'] is None or not 'whoplay' in msg['data'].keys():
            return
        with self.myside:
            self.whoplay = int(msg['data']['whoplay'])
            self.myside.notify_all()

    def qubeslistener(self,msg):
        global boardlocker
        print("qubeeee  ", msg)
        if msg['data'] is None or not msg['path'] == '/' or not('left' in msg['data'].keys() and 'right' in msg['data'].keys()) or self.whoami == self.whoplay:
            return
        with boardlocker:
            if self.num_of_drop >= int(msg['data']['num_of_drop']):
                return
            self.num_of_drop = int(msg['data']['num_of_drop'])
            self.makeacube(int(msg['data']['left']), int(msg['data']['right']))
            firebase.db.child('games').child(firebase.mygamenum).child('qubes').remove()

    def movement_listener(self,msg):
        global boardlocker
        if self.is_update or self.ismine() or msg['data'] is None or not msg['path'] == '/' or not('origin' in msg['data'].keys() and 'target' in msg['data'].keys()):
            return
        with boardlocker:
            print("movement:   ", msg)
            src = int(msg['data']['origin'])
            dst = int(msg['data']['target'])
            num = int(msg['data']['num_of_movement'])
            if num in self.moves:
                return
            if src == 0 and dst == 0:
                with self.myside:
                    self.myside.notify_all()
                return
            self.moves.append(num)
            if src == self.players[self.whoplay].house:
                self.step_from_stack_web(src, dst)
            else:
                self.make_a_move_by_web(src, dst)
            firebase.db.child("games").child(firebase.mygamenum).child('movement').remove()
            firebase.accept_move()
            self.is_update = True
        with self.myside:
            self.myside.notify_all()


    def ismine(self):
        return self.whoami == self.whoplay

    def makingamove(self):
        self.num_of_move = 0
        while not self.isover():
            if self.win.isClosed():
                print("leave meeee")
            with self.myside:
                self.moves = []
                self.listen_to_qube.start()
                self.side_stream = firebase.db.child('games').child(firebase.mygamenum).child('side').stream(self.side_listener)
                if not self.ismine():
                    self.move_lis = firebase.db.child("games").child(firebase.mygamenum).child("movement").stream(self.movement_listener)
                while not self.ismine():
                    self.is_update = False
                    print("not makin a move")
                    self.myside.wait()
            self.side_stream.close()
            print("making a move")
            self.win.getMouse()
            self.rollthecubes()
            while self.canmove():
                if (not self.players[self.whoplay].stack.isempty()):
                    src = self.players[self.whoplay].house
                    self.makestepfromstack(src)
                else:
                    l = self.win.getMouse()
                    src = self.findtriangle(l)
                    self.makeastep(src)
            self.num_of_move = 0
            with firebase.lock_approval_move:
                self.whoplay = self.changeplayer()
        print("stoping")

        self.win.close()
    def makestepfromstack(self,src):
        if self.ischosable(src):
            a = self.allsteps(src)
            for i in range(len(a)):
                self.up[a[i]].sign.undraw()
                self.up[a[i]].sign.draw(self.win)
            l = self.win.getMouse()
            dst = self.findtriangle(l)
            if self.find(a, dst):
                self.step_from_stack_web(src,dst)
                self.val.remove(abs(src - dst))
                self.numoftryes -= 1
                self.num_of_move += 1
                update_move_thread = threading.Thread(target=firebase.update_game_move(src, dst, self.num_of_move))
                update_move_thread.start()
            for i in range(len(a)):
                self.up[a[i]].sign.undraw()

    def step_from_stack_web(self, src, dst):
        color = self.players[self.whoplay].color
        m = self.players[self.whoplay].stack.remove()
        if self.up[dst].color != self.players[self.whoplay].color and self.up[dst].numofplayers == 1:
            self.eat(self.up[dst])
        self.up[dst].add(m, color)


    def makeastep(self, src):
        if self.ischosable(src):
            a = self.allsteps(src)
            for i in range(len(a)):
                if a[i]==24:
                    self.players[self.whoplay].point.undraw()
                    self.players[self.whoplay].point.draw(self.win)
                else:
                    self.up[a[i]].sign.undraw()
                    self.up[a[i]].sign.draw(self.win)
            try:
                l = self.win.getMouse()
            except GraphicsError:
                print("yulkelulu")
            dst = self.findtriangle(l)
            while ((dst == None) and not (24 in a and self.isallinhome() and 0<=l.getX()<=50)):
                l = self.win.getMouse()
                dst = self.findtriangle(l)
            if dst == None:
                dst == -7
            self.make_a_move_for_user(src,dst,a,l)
            self.num_of_move += 1
            update_move_thread = threading.Thread(target=firebase.update_game_move(src, dst, self.num_of_move))
            update_move_thread.start()

    def make_a_move_for_user(self, src, dst, a, l):
        if dst is None:
            m = self.remforever(src, a)
        if self.find(a, dst):
            color = self.players[self.whoplay].color
            m = self.up[src].remove()
            if self.up[dst].color != self.players[self.whoplay].color and self.up[dst].numofplayers == 1:
                self.eat(self.up[dst])
            self.up[dst].add(m, color)
            self.val.remove(abs(src - dst))
            self.numoftryes -= 1
        for i in range(len(a)):
            if a[i]==24:
                self.players[self.whoplay].point.undraw()
            else:
                self.up[a[i]].sign.undraw()

    def make_a_move_by_web(self, src, dst):
        color = self.players[self.whoplay].color
        m = self.up[src].remove()
        if dst==-7:
            m = self.remove_forever_web(src)
            return
        if self.up[dst].color != self.players[self.whoplay].color and self.up[dst].numofplayers == 1:
            self.eat(self.up[dst])
        self.up[dst].add(m, color)


    def remove_forever_web(self, src):
        k = self.up[src].remove()
        k.undraw()


    def isallinhome(self):
        startpoint=(self.players[self.whoplay].dir)+self.players[self.whoplay].house
        for i in range(18):
            if self.up[startpoint+self.players[self.whoplay].dir*i].color==self.players[self.whoplay].color:
                return False
        return True
    def remforever(self, src,a):
        k=self.up[src].remove()
        k.undraw()
        for i in range(len(a)):
            if not a[i]==24:
                for j in range(len(self.val)):
                    if not (0<=src+self.players[self.whoplay].dir*self.val[j]<=23):
                        self.val.remove(self.val[j])
                        self.numoftryes -= 1
                        return
        self.numoftryes -= 1
    def rollthecubes(self):
        for i in range(len(self.cubes)):
            self.cubes[i].remove()
        val1=random.randint(1,6)
        val2 = random.randint(1, 6)
        if(val1==val2):
            self.numoftryes=4
            self.val=[val1,val1,val1,val1]
        else:
            self.numoftryes = 2
            self.val = [val1, val2]
        self.num_of_drop += 1
        firebase.updatequbes(val1,val2,self.num_of_drop)
        self.cubes[self.whoplay*2].create(val1)
        self.cubes[self.whoplay*2+1].create(val2)

    def eat(self, src):
        if src.color == "white":
            cir = src.remove()
            self.white.add(cir)
        else:
            cir = src.remove()
            self.black.add(cir)
    def find(self,a,item):
        for i in range(len(a)):
            if item==a[i]:
                return True
        return False
    def canmove(self):
        if len(self.val) == 0 or self.numoftryes <= 0 or self.isover():
            return False
        for i in range(len(self.val)):
            val1=self.val[i]
            if self.players[self.whoplay].stack.isempty():
                for i in range(23):
                    loc1 = i + self.players[self.whoplay].dir * val1
                    if loc1 >= 0 and loc1 <= 23:
                        if self.up[loc1].color == self.players[self.whoplay].color or self.up[loc1].color == "no":
                            return True
                        elif self.up[loc1].color != self.players[self.whoplay].color and self.up[loc1].numofplayers == 1:
                            return True
                    elif self.isallinhome() and not 0<=loc1<=23:
                        return True
            else:
                if self.up[self.players[self.whoplay].house + self.players[self.whoplay].dir * val1].color == self.players[self.whoplay].color or self.up[self.players[self.whoplay].house + self.players[self.whoplay].dir * val1].color == "no":
                    return True
                elif self.up[self.players[self.whoplay].house + self.players[self.whoplay].dir * val1].color != self.players[self.whoplay].color and self.up[self.players[self.whoplay].house + self.players[self.whoplay].dir * val1].numofplayers == 1:
                    return True
        return False
    def makeacube(self, left,right):
        for i in range(len(self.cubes)):
            self.cubes[i].remove()
        self.cubes[self.whoplay * 2].create(left)
        self.cubes[self.whoplay * 2 + 1].create(right)


    def ischosable(self, src):
        if src==None:
            return False
        for i in range(len(self.val)):
            val1=self.val[i]
            if self.isallinhome() and not (0 <= src + self.players[self.whoplay].dir * val1 <= 23):
                return True
            if src == self.players[self.whoplay].house or self.players[self.whoplay].color == self.up[src].color:
                if (src + self.players[self.whoplay].dir * val1 >= 0 and src + self.players[self.whoplay].dir * val1 <= 23):
                    if self.up[src + self.players[self.whoplay].dir * val1].color == self.players[self.whoplay].color or \
                            self.up[src + self.players[self.whoplay].dir * val1].color == "no" or self.up[
                        src + self.players[self.whoplay].dir * val1].numofplayers == 1:
                        return True
        return False

    def allsteps(self, src):
        steps = []
        for i in range(len(self.val)):
            val1=self.val[i]
            if src + self.players[self.whoplay].dir * val1 >= 0 and src + self.players[self.whoplay].dir * val1 <= 23:
                if self.up[src + self.players[self.whoplay].dir * val1].color == self.players[self.whoplay].color or \
                        self.up[src + self.players[self.whoplay].dir * val1].color == "no" or self.up[
                    src + self.players[self.whoplay].dir * val1].numofplayers == 1:
                    steps.append(src + self.players[self.whoplay].dir * val1)
            elif self.isallinhome() and not 0<=src + self.players[self.whoplay].dir * val1<=23:
                steps.append(24)
        return steps

    def findtriangle(self, point):
        y = point.getY()
        x = point.getX()
        for i in range(24):
            if self.up[i].corner1.getX() <= x and self.up[i].corner2.getX() >= x and self.up[i].corner1.getY() <= y and \
                    self.up[i].corner3.getY() >= y:
                return i
            if self.up[i].corner1.getX() <= x and self.up[i].corner2.getX() >= x and self.up[i].corner1.getY() >= y and \
                    self.up[i].corner3.getY() <= y:
                return i
        return None

    def isover(self):
        iswhiteover = True
        isblackover = True
        for i in range(24):
            if self.up[i].color == "white":
                iswhiteover = False
            if self.up[i].color == "Peru":
                isblackover = False
        if self.black.numofplayers > 0:
            isblackover = False
        if self.white.numofplayers > 0:
            iswhiteover = False
        return iswhiteover or isblackover

    def changeplayer(self):
        self.val.clear()
        firebase.change_player()
        if self.whoplay == 0:
            return 1
        return 0


def searching():
    global numofplayer
    global ingame
    ingame = 0
    firebase.myid = numofplayer
    firebase.invitelistener = firebase.db.child("users").child(numofplayer).stream(firebase.reacttoinvite)
    stam = firebase.findapartner(numofplayer)

def main():
    global numofplayer
    numofplayer = firebase.createuser()
    t = threading.Thread(target=searching,daemon=True)
    t.start()
    try:
        b = board()
    except GraphicsError as e:
        print("OK, GOODBYE")
        sys.exit()


main()
