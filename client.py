import socket
import pygame
import cl_client as cl

hote = 'localhost'
port = 8001
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Famille d'adresses, type du socket et de protocole
connexion_avec_serveur.connect((hote, port)) #Permet d'attendre des connexions de clients en utilisant le tuple (nom_hote, port)
print("Connecte")
pygame.init()
fenetre = pygame.display.set_mode((800, 800))
image = pygame.image.load('img_sprite_plane_red_player.png').convert_alpha()
image_fond = pygame.image.load('img_fond.png').convert_alpha()
rect = image.get_rect()
"""
Les messages recus sont tjrs de cette forme:
! + espace + objet + nom_objet +espace + action + espace + x,y ou x
notation objet :
    2 lettres en maj
    1e lettre: type d'objet player,ia,icone...
        P:player
        I:IA
        F:Fond
        I:Icone
    2e lettre: friendly ou ennemy:
        F ou E
    
ex : "!PE nom_obj blit x,y"
"""
objectList = []

while True:
    blitList = []
    msg_rec = connexion_avec_serveur.recv(1024)
    msg_rec = msg_rec.decode()
    list_msg = msg_rec.split("!")
    msg = list_msg[-1]
    if "." in msg:
        list_command = msg[:-1].split("!")
        command = list_command[-1].split(" ")
        type_objet = command[0]
        name_object = command[1]
        action = command[2]
        options = command[3]

        if action == "blit":
            found = False
            coo = options.split(",")
            coo = tuple(map(int,coo))
            for objet in objectList:
                if objet.name == name_object:
                    found = True
                    blitList.append(objet)
                    objet.move(coo)
            if not found:
                x = cl.PE(name_object,coo)
                objectList.append(x)
                blitList.append(x)
        
        fenetre.blit(image_fond,(0,0))
        for objet in blitList:
            fenetre.blit(objet.image,objet.rect)
        
        pygame.display.flip()
    else:
        try:
            msg = list_msg[-2]
            if "." in msg:
                list_command = msg[:-1].split("!")
                command = list_command[-1].split(" ")
                type_objet = command[0]
                name_object = command[1]
                action = command[2]
                options = command[3]

                if action == "blit":
                    found = False
                    coo = options.split(",")
                    coo = tuple(map(int,coo))
                    for objet in objectList:
                        if objet.name == name_object:
                            found = True
                            blitList.append(objet)
                            objet.move(coo)
                    if not found:
                        x = cl.PE(name_object,coo)
                        objectList.append(x)
                        blitList.append(x)
                
                fenetre.blit(image_fond,(0,0))
                for objet in blitList:
                    fenetre.blit(objet.image,objet.rect)
                
                pygame.display.flip()
        except:pass




print("disconnected")
connexion_avec_serveur.close()