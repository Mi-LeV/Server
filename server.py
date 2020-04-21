import socket 
import select
from random import randrange


hote = ''
port = 8001

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Famille d'adresses, type du socket et de protocole
connexion_principale.bind((hote, port)) #Permet d'attendre des connexions de clients en utilisant le tuple (nom_hote, port)
connexion_principale.listen(5)

serveur_lance = True
clients_connectes = []

while serveur_lance:
    connexion_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05) #select renvoie la liste des clients qui ont un message à réceptionner

    for connexion in connexion_demandees:
        connexion_avec_client, infos_connexion = connexion_principale.accept()
        clients_connectes.append(connexion_avec_client)
    
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05) #wlist est la liste des sockets en attente d'etre écrits, xlist est la liste des sockets en attente d'une erreur
    except select.error:
        pass
    else:
        for client in clients_a_lire:
            pass
        for client in clients_connectes:
            x = randrange(0,800)
            y = randrange(0,800)
            coo = "!" + str(x) + "," + str(y)
            coo = coo.encode()
            client.send(coo)


print("disconnected")
for client in clients_connectes:
    client.close()

connexion_principale.close()