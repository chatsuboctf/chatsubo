# Chatsubo
## Requirements

Install them via :

```
sudo apt install mariadb libmariadbclient-dev
```

Setup MySQL :

```
sudo mysql_secure_installation
CREATE USER 'chatsubo'@'localhost' IDENTIFIED BY 'chatsubo';
GRANT ALL PRIVILEGES ON localhost.localhost TO 'chatsubo'@'localhost';
```

Setup PVE API :
+ Création d'un user PVE "API"
    + Catégorie "Users"
+ Création d'un token "api"
    + Set name peu importe, uuidv4 OK
    + Catégorie "API Tokens"
+ Création d'un rôle API
    + Perms :
        + VM.Audit
        + VM.PowerMgmt
        + VM.Monitor
        + VM.Snapshot
        + VM.Snapshot.Rollback
    + Catégorie "Roles"
+ Ajout des paths 
    + Top catégorie "Permissions"
    + Ajout des paths /nodes/pve et /vms :
        + À l'utilisateur API
            + User permission
        + ET au token "api"
            + API Token permission

Setup Docker :
+ Créer un certificat serveur et client via le script bin/docker_cert.sh
+ Sur la machine du front :
    + Placer les fichiers ca.pem, cert.pem, key.pem dans config/providers/docker/<nom du docker précisé dans la config>/
+ Sur la machine hôte des conteneurs :
    + Placer les fichiers ca.pem, server-cert.pem, server-key.pem dans le dossier /etc/docker/tls
    + Copier la configuration suivante dans le fichier /etc/docker/daemon.json
    ```json
    {
        "tls": true,
        "tlscacert": "/etc/docker/tls/ca.pem",
        "tlscert": "/etc/docker/tls/server-cert.pem",
        "tlskey": "/etc/docker/tls/server-key.pem",
        "tlsverify": true,
        "hosts": ["fd://", "unix:///var/run/docker.sock","tcp://0.0.0.0:2376"]
    }
    ```
    + Créer le network docker auquel appartient le conteneur du VPN et auquel tous les containers seront ratachés :
        + `docker network create chatsubo-gate --subnet 10.10.30.0/24`

