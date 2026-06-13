import pygame
import random
import os
import GameFunctions 
from GameFunctions import Deck, Jetons

deck = Deck()
jetons = Jetons()
start = False

print("Willkommen zum Blackjack-Spiel!")

#Einsatz abfragen
einsatz = jetons.Einsatz()
while not start:
    if einsatz:
        start = True
    else:
        print("Fehler beim Setzen der Jetons.")
        start = False
#Deck erstellen und mischen
deck.createDeck()
deck.mischen()

#Karten für Spieler ziehen
print("1. Karte:", deck.ziehen())
print("2. Karte:", deck.ziehen())
