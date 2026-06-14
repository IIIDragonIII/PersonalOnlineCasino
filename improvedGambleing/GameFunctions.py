import os
import random

class Jetons:
    #Währungssystem
    if not os.path.exists("jetons.txt"):
        with open("jetons.txt", "w") as f:
            f.write("10000")
    
    def Einsatz(self):
        with open("jetons.txt", "r") as f:
            jetons = int(f.read())
        while True:
            try:
                einsatz = int(input("Wie viele Jetons möchten Sie setzen? "))
                if einsatz > jetons:
                    print("Sie haben nicht genug Jetons. Bitte setzen Sie einen niedrigeren Betrag.")
                elif einsatz <= 0:
                    print("Bitte setzen Sie einen positiven Betrag.")
                else:
                    print(f"Sie haben {einsatz} Jetons gesetzt.")
                    with open("jetons.txt", "w") as f:
                        f.write(str(jetons - einsatz))
                    return einsatz
            except ValueError:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")

class Deck:
    #Kartendeck und Kartenfunktionen erstellen
    karten = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    symbole = ["♠", "♥", "♦", "♣"]
    kartenstapel = []

    def createDeck(self):
        for symbol in self.symbole:
            for karte in self.karten:
                self.kartenstapel.append((karte, symbol))
    def mischen(self):
        random.shuffle(self.kartenstapel)
    def ziehen(self):
        if len(self.kartenstapel) > 0:
            gezogen = self.kartenstapel.pop()
            print(f"Sie haben {gezogen[0]}{gezogen[1]} gezogen.")
            return gezogen
        else:
            print("Der Kartenstapel ist leer.")
            return None