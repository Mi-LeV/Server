import socket 
import select
import serv_var as var
from random import randrange
import serv_classes as cl


hote = ''
port = 8001

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Famille d'adresses, type du socket et de protocole
connexion_principale.bind((hote, port)) #Permet d'attendre des connexions de clients en utilisant le tuple (nom_hote, port)
connexion_principale.listen(5)

serveur_lance = True
clients_connectes = []
noms_clients = {}
nb_nom = 0

while serveur_lance:
    connexion_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05) #select renvoie la liste des clients qui ont un message à réceptionner

    for connexion in connexion_demandees:
        connexion_avec_client, infos_connexion = connexion_principale.accept()
        clients_connectes.append(connexion_avec_client)
        noms_clients[connexion_avec_client] = "player{}".format(nb_nom)
        msg = "!" + "? " + noms_clients[connexion_avec_client]+ " " + "rename " + "?" + "."
        connexion_avec_client.send(msg.encode())
        nb_nom += 1
        noms_clients[connexion_avec_client] = cl.PlayerPlane(0,0,True)
        
    
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05) #wlist est la liste des sockets en attente d'etre écrits, xlist est la liste des sockets en attente d'une erreur
    except select.error:
        pass
    else:
        for client in clients_a_lire:
            msg_rec = client.recv(1024)
            msg_rec = msg_rec.decode()
            list_msg = msg_rec.split("!")
            for msg in list_msg:
                if "." in msg:
                    list_command = msg[:-1].split("!")
                    command = list_command[-1].split(" ")
                    type_objet = command[0]
                    name_object = command[1]
                    action = command[2]
                    options = command[3]

                    if action == "close":
                        client.close()

                    if action == "respawn":
                        pass

                    if action == "shoot":
                        pass



        for client in clients_connectes:
            x = randrange(0,800)
            y = randrange(0,800)
            msg = "!" + "PE " + "nom_obj " + "blit " + str(x) + "," + str(y) +","+ str(x%300)+ "."
            msg = msg.encode()
            client.send(msg)
            x = randrange(0,800)
            y = randrange(0,800)
            msg = "!" + "PF " + "nom_obj1 " + "blit " + str(x) + "," + str(y) +","+ str(x%300)+ "."
            msg = msg.encode()
            client.send(msg)


print("disconnected")
for client in clients_connectes:
    client.close()

connexion_principale.close()