import math
from random import randrange
import json
import serv_var as var


class utility:
    @staticmethod
    def plafonne(nombre,plafond,plafondMax):
        if plafondMax:
            if nombre > plafond:
                return plafond
        else:
            if nombre < plafond:
                return plafond
        return nombre
    
    @staticmethod
    def getBearing(pointA,pointB):
        # if (a1 = b1 and a2 = b2) throw an error 
        theta = math.atan2(pointB[0] - pointA[0], pointA[1] - pointB[1])
        if (theta < 0):
            theta += 2*math.pi
        angle = 360-math.degrees(theta)
        angle %= 360
        return angle
    
    @staticmethod

    def getCoords(angleDegree):
        angle = math.radians(angleDegree)
        x = math.cos(angle)
        y = math.sin(angle)
        return x,y
    
    @staticmethod
    def getDistance(objet,objet2):
        diffX = objet2.x - objet.x
        diffY = objet2.y - objet.y
        distance = math.sqrt(diffX**2+diffY**2)
        return distance
        
    @staticmethod
    def spawnGroup(x,y,friendly,number):
        for i in range(number):
            IaPlane(x+randrange(-100,100,30),y+randrange(-100,100,30),friendly,"ia"+str(var.nom_iterator))
            var.nom_iterator += 1
    
    @staticmethod
    def getObjType(obj):
        if type(obj) == PlayerPlane:
            classe = "P"
        elif type(obj) == IaPlane:
            classe = "I"
        elif type(obj) == Missile:
            classe = "M"
        if obj.friendly == True:
            return classe + "F"
        elif obj.friendly == False:
            return classe + "E"
        else:
            return classe + "N"


class Plane:
    def __init__(self,x,y,name,angle = 90,timeAlive = 0):
        self.MAXSPEED = 3
        self.timeAlive = timeAlive
        self.xVector=0
        self.yVector=0
        self.xDest = x
        self.yDest = y
        self.x = x
        self.y = y
        self.name = name
        self.angle = angle
        self.missileList = []
        var.refreshList.append(self)


    def delete(self):
        if self in var.hitList:
            var.hitList.remove(self)
        if self in var.refreshList:
            var.refreshList.remove(self)
        if self in var.playerList:
            var.playerList.remove(self)
        del self

    def vectorTo(self,vector,distanceToDest):

        if distanceToDest > 0:
            distanceToDest = utility.plafonne(distanceToDest,2,True)
        else:
            distanceToDest = utility.plafonne(distanceToDest,-2,False)
        
        if (vector + distanceToDest)*abs((distanceToDest/1.5)) > 0:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),self.MAXSPEED,True)
        else:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),-self.MAXSPEED,False)
        
        return vector
    
    def goTo(self,xDistanceToDest,yDistanceToDest):

        self.xVector = self.vectorTo(self.xVector,xDistanceToDest)
        self.yVector = self.vectorTo(self.yVector,yDistanceToDest)
        
        self.x += self.xVector
        self.y += self.yVector

        xDistanceToDest -= self.xVector
        yDistanceToDest -= self.yVector

    def testOutOfMap(self):# la map doit etre un carre
        if self.x < 0 or self.x > var.MAP_LIMITS:
            return True
        if self.y < 0 or self.y > var.MAP_LIMITS:
            return True
        return False



    def tick(self):
        self.timeAlive += 1
        if not self.xDest or not self.yDest:# si la dest n'est pas définie, rien faire
            return
        xDistanceToDest=self.xDest-self.x
        yDistanceToDest=self.yDest-self.y
        if not((3 > xDistanceToDest > -3) and (3 > yDistanceToDest > -3)):
            self.goTo(xDistanceToDest,yDistanceToDest)
        else:# s'arrete
            
            self.xVector = 0
            self.yVector = 0
            return True

    def turn(self):
        self.angle = (utility.getBearing((self.x,self.y),(self.xDest,self.yDest))+90)%360
    
    def shoot(self):
        self.missileList.append(Missile(0,0,"mis{}".format(var.nom_iterator),0,0,self))
    

class PlayerPlane(Plane):
    def __init__(self,x,y,friend,name,angle = 90,timeAlive = 0):
        super().__init__(x,y,name,angle,timeAlive)
        self.MAXMISSILE = 3
        var.playerList.append(self)
        
        self.friendly = friend
        self.notifList = []
        self.notifOutList =[]
        self.mouse = (400,400)
    
    def shoot(self):
        if len(self.missileList) < self.MAXMISSILE:
            super().shoot()

    def tick(self):
        if self.testOutOfMap() and (not self.notifList):
            NotifOut('Hors des limites de la map, mort dans ',60,self)
        if (not self.testOutOfMap()) and self.notifList:
            for notif in self.notifOutList:
                notif.delete()
        for notif in self.notifList:
            if notif.timeAlive > 60:
                self.delete()
        self.timeAlive += 1
        self.goTo()
    
    def goTo(self):
        self.xVector = self.vectorToX(self.xVector,self.mouse[0])
        self.yVector = self.vectorToY(self.yVector,self.mouse[1])
        
        self.x += self.xVector
        self.y += self.yVector

    def vectorToX(self,vector,mouse):
        distanceToDest = mouse - 400
        if (vector + distanceToDest)*abs((distanceToDest/1.5)) > 0:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),self.MAXSPEED,True)
        else:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),-self.MAXSPEED,False)
        return vector
    
    def vectorToY(self,vector,mouse):
        distanceToDest = mouse - 400
        if (vector + distanceToDest)*abs((distanceToDest/1.5)) > 0:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),self.MAXSPEED,True)
        else:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),-self.MAXSPEED,False)
        return vector
    

class IaPlane(Plane):
    def __init__(self,x,y,friend,name,active = True,angle = 90,timeAlive = 0):
        super().__init__(x,y,name,angle,timeAlive)
        self.MAXSPEED = 1.5
        self.RELOADTIME = 30
        self.MAXMISSILE = 3
        self.agro = None
        self.active = active
        self.friendly = friend
    
    def tick(self):
        if self.active:
            if self.searchAgro():#cherche agro et renvoie true si trouve
                if utility.getDistance(self,self.agro) < 150 and len(self.missileList)<self.MAXMISSILE and self.timeAlive%self.RELOADTIME==0 and self.timeAlive != 0:
                    #si à moins de 150, et qu'il a moins de 3 missiles en vie et que son tmps de vie est divisible
                    #  par RELOADTIME(pour ajouter délai)
                    self.shoot()
                
            objectNear = self.testObjectNear()
            if objectNear:
                self.xDest = self.x-(objectNear.x-self.x)
                self.yDest = self.y-(objectNear.y-self.y)
            else:
                if not self.goAgro():#renvoie True si elle va à l'agro
                    self.xDest = self.x #sinon on immobilise
                    self.yDest = self.y

            super().tick()
            

    def testObjectNear(self):
        minima = 99999999 #valeur très haute, toujours supérieur à distance
        temp = 99999999 #valeur très haute, toujours supérieur à temp
        minObj = None
        for objet in var.refreshList:#test de la distance minimlale
            if objet != self:#si l'objet le plus proche n'est pas lui meme
                temp = utility.getDistance(self,objet)#calcul distance
            if temp < minima:
                minima = temp
                minObj = objet#on a l'objet le plus proche
        if minima < 75:#si l'objet est à moins de 50
            return minObj
        else:
            return None
        
    def goAgro(self):
        if not self.agro:# si la dest n'est pas définie, rien faire
            return False
        self.xDest = self.agro.x
        self.yDest = self.agro.y
        return True

    def searchAgro(self):
        ennemyList = []
        for objet in var.refreshList:
            if type(objet)!= Missile and objet.friendly != self.friendly:#test si objet non missile et si il est pas de son camp
                ennemyList.append(objet)

        if ennemyList:#si la liste n'est pas vide
            minima = 99999999 #valeur très haute, toujours supérieur à distance
            minObj = None
            for objet in ennemyList:#test de la distance minimlale
                temp = utility.getDistance(self,objet)#calcul distance
                if temp < minima:
                    minima = temp
                    minObj = objet
            self.agro = minObj
            return True
        else:
            self.agro = None
            return False

class Missile():
    def __init__(self,x, y , name , angle ,timeAlive,creator = None):

        self.creator = creator
        if self.creator: #si il a un créateur
            angle = self.creator.angle
            xVector = self.creator.xVector
            yVector = self.creator.yVector
            x = self.creator.x
            y = self.creator.y
            timeAlive = 0
        else:#si il est créé artificiellement (lors d'un load)
            angle = angle
            xVector = 0
            yVector = 0
            x = x
            y = y
            timeAlive = timeAlive
        self.friendly = None

        xAngle,yAngle = utility.getCoords(angle)
        self.xVector=utility.plafonne(xVector*2 + xAngle*30,40,True)
        self.xVector=utility.plafonne(xVector*2 + xAngle*30,-40,False)
        self.yVector=utility.plafonne(yVector*2 + yAngle*30,40,True)
        self.yVector=utility.plafonne(yVector*2 + yAngle*30,-40,False)
        self.x = x
        self.y = y
        self.speed = 0
        self.timeAlive = timeAlive
        self.name = name
        self.angle = angle#l'angle natif de l'image
        var.refreshList.append(self)
    
    def vectorTo(self,vector):#décélération proressive du missile
        return vector/((self.timeAlive/20)+1)
    
    def goTo(self):

        self.xVector = self.vectorTo(self.xVector)
        self.yVector = self.vectorTo(self.yVector)
        
        self.x += self.xVector
        self.y -= self.yVector #c'est un moins car l'origine des y n'est pas en bas mais en haut
    
    def tick(self):
        self.timeAlive += 1
        #si vecteurs pas trop faibles, et timeAlive pas trop grand, bouger sinon s'arrete
        if not(((-1.5<self.xVector < 1.5) and (-1.5<self.yVector < 1.5))or ( self.timeAlive > 500)):
            self.goTo()
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            self.delete()
    
    def turn(self):
        return

    def delete(self):
        if self.creator:
            if self in self.creator.missileList:
                self.creator.missileList.remove(self)
        if self in var.hitList:
            var.hitList.remove(self)
        if self in var.refreshList:
            var.refreshList.remove(self)
        if self in var.playerList:
            var.playerList.remove(self)
        del self
    
    def testOutOfMap(self):
        if self.x < 0 or self.x > var.MAP_LIMITS:
            return True
        if self.y < 0 or self.y > var.MAP_LIMITS:
            return True
        return False
