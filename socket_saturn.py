import socket
import time
import json

# Constantes
BUFFER_SIZE = 1024  # Taille du tampon pour les données reçues
DEFAULT_PORT = 3000  # Port par défaut
DISCOVERY_MESSAGE = b"M99999"  # Message de découverte à envoyer


TIMEOUT = 1  # Délai d'attente en secondes
BROADCAST_IP = "172.16.16.146"  # Adresse IP cible pour le broadcast


def discover_printer(ip_address, port):
    """
    Fonction pour découvrir une imprimante via UDP.

    :param ip_address: Adresse IP de broadcast.
    :param port: Port à utiliser pour l'envoi/réception.
    :return: Tuple contenant l'adresse de l'émetteur et les données reçues, ou None si timeout.
    """
    # Création du socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)  # Définition du délai d'attente
        try:
            # Envoi du message de découverte
            sock.sendto(DISCOVERY_MESSAGE, (ip_address, port))

            # Attente de la réponse
            start_time = time.time()
            while True:
                if time.time() - start_time > TIMEOUT:
                    print("Délai d'attente écoulé, aucune réponse reçue.")
                    return None
                try:
                    # Lecture des données reçues
                    data, addr = sock.recvfrom(BUFFER_SIZE)
                    return addr, data
                except socket.timeout:
                    print("Timeout lors de l'écoute des réponses.")
                    return None
        except socket.error as e:
            print(f"Erreur de socket : {e}")
            return None


if __name__ == "__main__":
    # Appel de la fonction pour découvrir les imprimantes
    result = discover_printer(BROADCAST_IP, DEFAULT_PORT)
    if result:
        addr, data = result
        print(f"Imprimante trouvée à {addr} avec les données : {data}")
    else:
        print("Aucune imprimante détectée.")


# Reponse attendu : Imprimante trouvée à ('172.16.16.*', 3000) avec les données : b'{"Id":"dddf25273b12b094c5a8b9513a30ca60049","Data":{"Attributes":{"Name":"Saturn3Ultra","MachineName":"ELEGOO Saturn 3 Ultra","ProtocolVersion":"V1.0.0","FirmwareVersion":"V1.5.4","Resolution":"11520x5120","MainboardIP":"172.16.16.146","MainboardID":"5b7e314f2ed00100","SDCPStatus":0,"LocalSDCPAddress":"","SDCPAddress":"","Capabilities":["FILE_TRANSFER","PRINT_CONTROL"]},"Status":{"CurrentStatus":0,"PreviousStatus":0,"PrintInfo":{"Status":0,"CurrentLayer":0,"TotalLayer":0,"CurrentTicks":0,"TotalTicks":0,"ErrorNumber":0,"Filename":""},"FileTransferInfo":{"Status":0,"DownloadOffset":0,"CheckOffset":0,"FileTotalSize":0,"Filename":""}}}}'
