import pygame
import random
import os
import GameFunctions
from GameFunctions import Blackjack, Jetons

bj = Blackjack()
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
bj.DeckErstellen()
bj.Mischen()

#Karten für Spieler ziehen
erste_karte, erster_wert = bj.Ziehen()
zweite_karte, zweiter_wert = bj.Ziehen()
gesamt_wert = erster_wert + zweiter_wert
print("1. Karte:", erste_karte, "2. Karte:", zweite_karte, "Gesamt:", gesamt_wert)

#Karten für Dealer ziehen
dealer_erste_karte, dealer_erster_wert = bj.Ziehen()
dealer_zweite_karte, dealer_zweiter_wert = bj.Ziehen()
dealer_gesamt_wert = dealer_erster_wert + dealer_zweiter_wert
print(f"Dealer: {dealer_erste_karte} [_] Gesamt: {dealer_erster_wert}",end="/r", flush=True)

bj.KartenBlackjack(gesamt_wert, dealer_gesamt_wert)
if bj.spieler_blackjack == True:
    print(f"Dealer: {dealer_erste_karte} [_] Gesamt: {dealer_erster_wert}")
    print("Spieler hat Blackjack!")
    
elif bj.dealer_blackjack == True:
    print(f"Dealer: {dealer_erste_karte} {dealer_zweite_karte} Gesamt: {dealer_gesamt_wert}")
    print("Dealer hat Blackjack!")
    
if not bj.no_comparison:
    bj.ÜberEinundzwanzig(gesamt_wert, dealer_gesamt_wert)