#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys
import logging
import getpass
import signal
import os
import time

from optparse import OptionParser

import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


# Definition des fonctions appliquant les actions sur le jabber
def CallVienoiserieOK(signum, stack):
    xmpp.signal_vienoiserieOK(signum);

def CallVienoiserieKO(signum, stack):
    xmpp.signal_vienoiserieKO(signum);

def CallDeconnexion(signum, stack):
    xmpp.signal_deconnexion(signum);

# Classe Connection
class Connection(sleekxmpp.ClientXMPP):

    def signal_vienoiserieOK(self, signum):
        print 'Received:', signum
        self.send_presence(pstatus="Vienoiserie OK !")

    def signal_vienoiserieKO(self, signum):
        print 'Received:', signum
        self.send_presence(pstatus="Vienoiserie KO !!!")

    def signal_deconnexion(self, signum):
        print 'Received:', signum
        self.disconnect(wait=True)

    # Fonction permettant d'écrire dans le fichier saltServer.pid le pid du processus courant 
    def writePidFile():
        pid = str(os.getpid())
        f = open('saltServer.pid', 'w')
        f.write(pid)
        f.close()

    # Initialisation de la connexion en envoyant la présence et en désactivant la mise à jours automatique
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.send_presence()
        self.auto_reconnect = False

    # Appel des différentes fonctions à la détection du signal
    signal.signal(signal.SIGUSR1, CallVienoiserieOK)
    signal.signal(signal.SIGINFO, CallVienoiserieKO)
    signal.signal(signal.SIGUSR2, CallDeconnexion)

    # Appel de la fonction d'écriture du pid
    writePidFile()

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options (outils de debug).
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options (définition de nouveaux parametres login et password).
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    # Définition des logins
    # opts.jid = "compteJabber"
    # opts.password = "motdepasse"
    

    # Si aucun login n'est entré, on les demande dans la console (utilisé pour le debug)
    # if opts.jid is None:
    #    opts.jid = raw_input("Username: ")
    # if opts.password is None:
    #    opts.password = getpass.getpass("Password: ")

    # Création de la connexion xmpp en instanciant la classe
    xmpp = Connection(opts.jid, opts.password)

    # Si la connexion est bonne (au serveur jabber), alors on lance le processus.
    if xmpp.connect(('jabber.etu.univ-nantes.fr', 5222)): 
        print 'My PID is:', os.getpid()

        xmpp.process(block=True)
        print("Done")

    else:
        print("Unable to connect.")