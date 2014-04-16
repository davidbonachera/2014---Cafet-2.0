 <i class="icon-refresh"></i> Cafet 2.0 
========================================

Afin de connecter la **cafetéria** et de permettre aux utilisateurs de **connaitre l'état** de celle-ci en temps réel, nous avons mis en place un système utilisant différentes technologies qui automatise cette tache et **detecte l'ouverture** ou **la fermeture** d'un volet roulant.

----------
Introduction
------------

Dans un premier temps, nous attendons encore la livraison du raspberry et du capteur commandés par la cafet pour pouvoir implémenter l'application grâce au travail du groupe de *Thomas JOEISSEINT* et *Vladimir BAGAZOV*.

Effectivement nous pourrons ainsi fournir une page WEB avec l'état actualisé remonté par nos capteurs. 

Actuellement, nous avons mis en place une page web de test en simulant le changement d'état du capteur par des boutons lancant des actions asynchrones.


> <i class="icon-file"></i> **Technologies utilisées:**
> 
> - Librairie **Python** [<i class="icon-link"></i> SleekXMPP][1] : Permet d'établir une connexion XMPP sur le serveur jabber et d'intéragir avec celui-ci.
> - Serveur **Apache/PHP** : Permet de simuler le rideau en créant des boutons imitant la fermeture ou l'ouverture du rideau.
> - Signaux **Système** : Permet d'intéragir avec le processus de l'application de facon asynchrone et de lancer dynamiquement des changements d'état sur le serveur Jabber.
> - Librairie **C** [<i class="icon-link"></i> wiringPI][4] : Permet d'acceder a la lecture des pins du GPIO. <!--- Non implémenté (attente livraison raspberry + capteur) -->

> <i class="icon-hdd"></i> **Matériels utilisés:**
>
> - Un raspberry.
> - Un [<i class="icon-link"></i> capteur I052601][2] à effet de hall.
> - Des [<i class="icon-link"></i> aimants Rare-Earth][3] 8mm x 1mm.


Utilisation
-------------------------

Dans un premier temps nous allons voir comment executer l'application puis par la suite comment intéragir avec elle.

###Execution
Pour faire fonctionner le script, il existe plusieurs façon. Soit de définir l'utilisateur et le mot de passe dans le fichier `connexion.py`, soit de les specifier en paramètre lors du lancement du script.

**Méthode 1 : Modifier le fichier connexion.py**

Pour ce faire il suffit de décommenter les lignes 108 et 109 *(ci-dessous)* puis remplacer les informations par celles d'un compte présent sur le serveur `jabber.etu.univ-nantes.fr`

```
    # Définition des logins
    opts.jid = "compteJabber"
    opts.password = "motDePasse"
```

De ce fait nous pouvons lancer le script par cette ligne de commande `python connexion.py` et voir l'état du compte passer à ***Online***.

> Pour effectuer les tests, nous pouvons utiliser le service presence du jabber de l'université accesible via cette url :
> [<i class="icon-link"></i> http://services-jabber.univ-nantes.fr/presence/?jid=PRENOM.NOM@etu.univ-nantes.fr&type=js][5]

<!--- Ne pas oublier de remplacer PRENOM.NOM par le compte connecté -->

----------

**Méthode 2 : Définir les paramètres lors de l'éxécution du script**

Il suffit lors de l'execution du script de rajouter -j et -p qui feront correspondre les valeurs entrées aux variables correspondantes.

Ex : `python connexion.py -j compteJabber@etu.univ-nantes.fr -p MotDePasse`

###Intéraction
Nous avons decidé de passer par l'utilisation des signaux systèmes pour faciliter l'execution du script et d'avoir une relation asynchrone avec celui-ci.

Avec trois signaux nous pouvons couvrir les différents cas d'utilisations du projet qui sont :

 - Connexion sur le serveur jabber à l'ouverture du rideau (automatique a l'execution du script)
 - Modification du status à l'arrivée des viennoiseries (2eme signal)
 - Déconnexion du serveur à la fermeture (1er signal)
 - Modification du status lors de penurie de viennoiseries (3eme signal)

De ce fait nous utilisons les signaux USR1, USR2 et INFO. Un signal est envoyé par l'éxecution d'une commande `kill`

Par exemple, pour dire au processus en cours de déconnecter l'utilisateur du serveur puis de fermer le proccesus, nous utilisons la commande suivante :
```
kill -USR2 $pid
```

`$pid` est une variable qui a pour valeur le dernier Process IDentifier lancé par le script python et qui est stocké dans un fichier (saltServer.pid). Grâce à cela, nous pouvons toujours identifier le dernier processus lancé.


Intégration
-----------

Pour la suite du projet, comme dit précédement, nous attendons toujours la livraison du matériel mais nous avons déjà le schéma *(fichier <i class="icon-picture"></i> schema.png)* pour brancher notre capteur sur le GPIO ainsi que la librairie a utiliser pour detecter le changement d'état du capteur au passage de l'aimant.


  [1]: http://sleekxmpp.com/ "SleekXMPP"
  [2]: http://www.dx.com/p/diy-hall-switch-hall-sensor-module-for-smart-car-blue-141648
  [3]: http://www.amazon.fr/dp/B00AAWGWPA/ref=pe_386181_37038081_TE_3p_dp_1
  [4]: http://wiringpi.com/
  [5]: http://services-jabber.univ-nantes.fr/presence/?jid=david.bonachera@etu.univ-nantes.fr&type=js