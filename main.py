# TP Simulation
import random

class Evenement:

    def __init__(self,pEvenement,pDate):
        #Evenement
        self.evenement = pEvenement
        #Date
        self.dateEvenement = pDate


class CentreDeMaintenance :

    NbBus = 0
    NbBusRep = 0
    AireQc,AireQr,AireBr=0,0,0
    Qc,Qr,Bc,Br=0,0,0,0
    echeancier = []

    def __init__(self,pDate):

        #Date simualtion en heures
        self.dateSimulation = pDate

    def debutSimulation(self):
        print("DebutSimulation")
        evenement = Evenement("arriveeBus",self.dateSimulation+0.5)
        self.echeancier.append(evenement)
        evenement = Evenement("finSimulation", 160)
        self.echeancier.append(evenement)

    def finSimulation(self):
        print("Fin Simualtion")
        self.echeancier = []
        tempsAttenteMoyenC = self.AireQc / self.NbBus
        tempsAttenteMoyenR = self.AireQr / self.NbBusRep
        TauxUtilsiationCR = self.AireBr /(2*160)


    def arriveeBus(self):
        print("arriveeBus")
        evenement = Evenement("arriveeBus", self.dateSimulation + 0.5)
        self.echeancier.append(evenement)
        self.NbBus += 1
        evenement = Evenement("arriveeFileC", self.dateSimulation)
        self.echeancier.append(evenement)

    def arriveeFileC(self):
        print("Arrivé file controle")
        self.Qc += 1
        if(self.Bc == 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.echeancier.append(evenement)

    def accesControle(self):
        print("Acces controle")
        self.Qc -= 1
        self.Bc = 1
        evenement = Evenement("departControle", self.dateSimulation+0.25)
        self.echeancier.append(evenement)

    def departControle(self):
        print("Depart controle")
        self.Bc = 0
        if (self.Qc > 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.echeancier.append(evenement)
        x = random()
        if(x<0.3):
            evenement = Evenement("arriveeFileR", self.dateSimulation)
            self.echeancier.append(evenement)

    def arriveeFileR(self):
        print("Arrivé file reparation")
        self.Qr += 1
        self.NbBusRep += 1
        if (self.Br < 2):
            evenement = Evenement("accesReparation", self.dateSimulation)
            self.echeancier.append(evenement)

    def accesReparation(self):
        print("Arrivé reparation")
        self.Qr -= 1
        self.Br += 1
        evenement = Evenement("departReparation", self.dateSimulation + 2.1)
        self.echeancier.append(evenement)

    def departReparation(self):
        print("Depart reparation")
        self.Br -= 1
        if(self.Qr>0):
            evenement = Evenement("debutSimulation", self.dateSimulation)
            self.echeancier.append(evenement)


    def mise_A_Jour_Aires(self,D1,D2):
        self.AireQc += (D2-D1)*self.Qc
        self.AireQr += (D2 - D1) * self.Qr
        self.AireBr += (D2 - D1) * self.Br

if __name__ == '__main__':

    DateSimulation = 00
    centreMaintenance = CentreDeMaintenance(DateSimulation)
    evenement = Evenement("debutSimulation", centreMaintenance.dateSimulation)
    centreMaintenance.echeancier.append(evenement)

    while(centreMaintenance.echeancier):
        evt = centreMaintenance.echeancier.pop(0)
        centreMaintenance.mise_A_Jour_Aires(centreMaintenance.dateSimulation,evt.dateEvenement)
        centreMaintenance.dateSimulation = evt.dateEvenement

        if(evt.evenement == "debutSimulation"):
            centreMaintenance.debutSimulation()
        elif (evt.evenement == "finSimulation"):
            centreMaintenance.finSimulation()
        elif (evt.evenement == "arriveeBus"):
            centreMaintenance.arriveeBus()
        elif (evt.evenement == "arriveeFileC"):
            centreMaintenance.arriveeFileC()
        elif (evt.evenement == "accesControle"):
            centreMaintenance.accesControle()
        elif (evt.evenement == "departControle"):
            centreMaintenance.departControle()
        elif (evt.evenement == "arriveeFileR"):
            centreMaintenance.arriveeFileR()
        elif (evt.evenement == "accesReparation"):
            centreMaintenance.accesReparation()
        elif (evt.evenement == "departReparation"):
            centreMaintenance.departReparation()
        else:
            print("evenement inconnu")