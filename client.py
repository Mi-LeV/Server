import socket
import pygame

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
! + espace + objet +espace + action + espace + x,y ou x
notation objet :
    2 lettres en maj
    1e lettre: type d'objet player,ia,icone...
    P:player
    I:IA
    F:Fond
    I:Icone
    2e lettre: friendly ou ennemy:
            F ou E
    
ex : "! FP blit x,y"
"""
while True:
    msg_rec = connexion_avec_serveur.recv(1024)
    msg_rec = msg_rec.decode()
    msg = msg_rec.split(" ")
    msg = msg[-1]
    coo_tuple = tuple(map(int,msg.split(",")))
    rect = image.get_rect(center = coo_tuple)

    fenetre.blit(image_fond,(0,0))
    fenetre.blit(image,rect)
    pygame.display.flip()




print("disconnected")
connexion_avec_serveur.close()