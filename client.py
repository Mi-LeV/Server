import socket
import pygame
from pygame.locals import *
import cl_classes as cl
import cl_var as var

hote = 'localhost'
port = 8001
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Famille d'adresses, type du socket et de protocole
connexion_avec_serveur.connect((hote, port)) #Permet d'attendre des connexions de clients en utilisant le tuple (nom_hote, port)
print("Connecte")
pygame.init()
fenetre = pygame.display.set_mode((800, 800))
image_fond = pygame.image.load('images/img_fond.png').convert_alpha()
loop = True
"""
Les messages recus sont tjrs de cette forme:
! + espace + objet + nom_objet +espace + action + espace + x,y ou x
type objet :
    2 lettres en maj
    1e lettre: type d'objet player,ia,icone...
        P:player
        I:IA
        M:Missile
    
    2e lettre: friendly ou ennemy:
        F ou E

nom de l'objet:
    un nom unique, propre à l'objet en question

action:
    chose que l'on veut faire avec cet objet: blit : bl, delete : del

options:
    champ optionnel, utilisé par blit pour les coordonnées et l'angle,etc...

les champs du message non utilisés NE DOIVENT PAS ETRE VIDES, ils sont remplacés par des ?

ex : "!PE nom_obj blit x,y,angle."
ex : "!? nom_obj delete ?."
CHAQUE MESSAGE DOIT FAIRE 24 CARACTERES (pour éviter perte de données): SI LE MESSAGE EST TROP PETIT,
 RAJOUTER DES ? DANS LES OPTIONS
"""

while loop:
    for event in cl.pygame.event.get():    #On parcours la liste de tous les événements reçus
            if event.type == MOUSEBUTTONDOWN and event.button == 1:##clic gauche
                msg = "!" + "? " + "? " + "sho " + "?" + "."
                msg = msg.encode()
                connexion_avec_serveur.send(msg)
            if event.type == KEYDOWN and event.key == K_SPACE:#on crée un nouv player et on le met dans playerlist
                msg = "!" + "? " + "? " + "res " + "?" + "."
                msg = msg.encode()
                connexion_avec_serveur.send(msg)
            if event.type == KEYDOWN and event.key == K_n:#on crée un nouv player et on le met dans playerlist
                msg = "!" + "IE " + "? " + "spa " + "5" + "."
                msg = msg.encode()
                connexion_avec_serveur.send(msg)
            if event.type == KEYDOWN and event.key == K_b:#on crée un nouv player et on le met dans playerlist
                msg = "!" + "IF " + "? " + "spa " + "5" + "."
                msg = msg.encode()
                connexion_avec_serveur.send(msg)
            
    var.blitList = []
    msg_rec = connexion_avec_serveur.recv(2600)
    msg_rec = msg_rec.decode()
    list_msg = msg_rec.split("!")
    for msg in list_msg[1:]:

        if "." in msg:#si le message est entier
            list_command = msg[:-1].split("!")
            command = list_command[-1].split(" ")
            type_objet = command[0]
            name_object = command[1]
            action = command[2]
            options = command[3]
            options = options.replace("?","")

            if action == "bl":
                found = False
                coo = options.split(",")
                x,y = tuple(map(int,coo[:2]))#on fait un tuple avec x,y
                for objet in var.objectList:
                    if objet.name == name_object:
                        found = True
                        var.blitList.append(objet)
                        objet.move((x,y))
                        objet.turn(float(coo[2]))
                if not found:
                    if type_objet == 'PE':
                        new_obj = cl.PE(name_object,(x,y))
                    elif type_objet == 'PF':
                        new_obj = cl.PF(name_object,(x,y))
                    elif type_objet == 'IE':
                        new_obj = cl.IE(name_object,(x,y))
                    elif type_objet == 'IF':
                        new_obj = cl.IF(name_object,(x,y))
                    var.objectList.append(new_obj)
                    var.blitList.append(new_obj)
            
            if action == "del":
                for objet in var.objectList:
                    if objet.name == name_object:
                        objet.delete()
            
            if action == "nam":
                client_name = name_object
        
        fenetre.blit(image_fond,(0,0))

        for objet in var.blitList:
            fenetre.blit(objet.image,objet.rect)
        
        pygame.display.flip()

        if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):#si on appuie sur la croix de la fenetre 
                msg = "!" + "? " + "? " + "clo " + "?" + "."
                msg = msg.encode()
                connexion_avec_serveur.send(msg)
                loop = False



print("disconnected")
connexion_avec_serveur.close()