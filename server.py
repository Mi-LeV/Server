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


while serveur_lance:
    connexion_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05) #select renvoie la liste des clients qui ont un message à réceptionner

    for connexion in connexion_demandees:
        connexion_avec_client, infos_connexion = connexion_principale.accept()
        clients_connectes.append(connexion_avec_client)
        noms_clients[connexion_avec_client] = "pl{}".format(var.nom_iterator)
        msg = "!" + "? " + noms_clients[connexion_avec_client]+ " " + "nam " + "?????????" + "."
        connexion_avec_client.send(msg.encode())
        var.nom_iterator += 1
        cl.PlayerPlane(0,0,True,noms_clients[connexion_avec_client])
        
    
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
            for msg in list_msg[1:]:
                if "." in msg:
                    list_command = msg[:-1].split("!")
                    command = list_command[-1].split(" ")
                    type_objet = command[0]
                    name_object = command[1]
                    action = command[2]
                    options = command[3]

                    if action == "clo":
                        client.close()
                        noms_clients.pop(client)
                        clients_connectes.remove(client)
                    
                    if action == "spa":
                        cl.utility.spawnGroup(500,500,type_objet[1] == "F",int(options))

                    if action == "res":
                        pass

                    if action == "sho":
                        pass
    
    for objet in var.refreshList:
        objet.turn()
        objet.tick()

    var.hitList = []#reset de la liste des objets touchés

    for objet in var.refreshList:#pour chaque objet physique(avion, missile)
        for objet2 in var.refreshList:#boucle de test hitbox
            if (- 5 <objet.x - objet2.x < 5 or - 5 <objet.y - objet2.y < 5) and objet != objet2:
                if not(type(objet)==cl.Missile and objet.creator == objet2 and objet.timeAlive < 5) and not(type(objet2)==cl.Missile and objet2.creator == objet and objet2.timeAlive < 5):
                    #si 1 et 2 sont pas des missiles dans la phase d'invincibilité, ou si ils touchent leur créateur
                    var.hitList.append(objet) #on ajoute l'objet 1 à la hitList
        
    for objet in var.hitList[::-1]:#boucle delete(on déréférence les objets de toute liste pour pouvoir les supprimer)
        objet.delete()

    for client in clients_connectes:
        allMsg = ""
        for objet in var.refreshList:
            msg = "!" + cl.utility.getObjType(objet) + " "+ objet.name + " " + "bl "\
                + str(round(objet.x))+","+str(round(objet.y))+","+str(round(objet.angle))
            while len(msg) < 25:
                msg += "?"
            msg += "."
            allMsg += msg
        totalsent = 0
        while totalsent < len(allMsg):
            sent = client.send(allMsg[totalsent:].encode())
            totalsent = totalsent + sent


print("disconnected")
for client in clients_connectes:
    client.close()

connexion_principale.close()