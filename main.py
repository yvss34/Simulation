# TP Simulation
import random

class Evenement:

    def __init__(self,pEvenement,pDate):
        #Evenement
        self.evenement = pEvenement
        #Date
        self.dateEevenement = pDate


class CentreDeMaintenance :

    NbBus = 0
    NbBusRep = 0
    AireQc,AireQr,AireBr=0
    Qc,Qr,Bc,Br=0
    echeancier = ()

    def __init__(self,pDate):

        #Date simualtion en heures
        self.dateSimulation = pDate

    def debutSimulation(self):
        print("DebutSimulation")
        evenement = Evenement("arriveeBus",self.dateSimulation+0.5)
        self.echeancier.add(evenement)
        evenement = Evenement("finSimulation", 160)
        self.echeancier.add(evenement)

    def finSimulation(self):
        print("Fin Simualtion")
        self.echeancier = ()
        tempsAttenteMoyenC = self.AireQc / self.NbBus
        tempsAttenteMoyenR = self.AireQr / self.NbBusRep
        TauxUtilsiationCR = self.AireBr /(2*160)


    def arriveeBus(self):
        print("arriveeBus")
        evenement = Evenement("arriveeBus", self.dateSimulation + 0.5)
        self.echeancier.add(evenement)
        self.NbBus += 1
        evenement = Evenement("arriveeFileC", self.dateSimulation)
        self.echeancier.add(evenement)

    def arriveeFileC(self):
        print("Arrivé file controle")
        self.Qc += 1
        if(self.Bc == 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.echeancier.add(evenement)

    def accesControle(self):
        print("Acces controle")
        self.Qc -= 1
        self.Bc = 1
        evenement = Evenement("departControle", self.dateSimulation+0.25)
        self.echeancier.add(evenement)

    def departControle(self):
        print("Depart controle")
        self.Bc = 0
        if (self.Qc > 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.echeancier.add(evenement)
        x = random()
        if(x<0.3):
            evenement = Evenement("arriveeFileR", self.dateSimulation)
            self.echeancier.add(evenement)

    def arriveeFileR(self):
        print("Arrivé file reparation")
        self.Qr += 1
        self.NbBusRep += 1
        if (self.Br < 2):
            evenement = Evenement("accesReparation", self.dateSimulation)
            self.echeancier.add(evenement)

    def accesReparation(self):
        print("Arrivé reparation")
        self.Qr -= 1
        self.Br += 1
        evenement = Evenement("departReparation", self.dateSimulation + 2.1)
        self.echeancier.add(evenement)

    def departReparation(self):
        print("Depart reparation")
        self.Br -= 1
        if(self.Qr>0):
            evenement = Evenement("debutSimulation", self.dateSimulation)
            self.echeancier.add(evenement)


    def mise_A_Jour_Aires(self,D1,D2):
        self.AireQc += (D2-D1)*self.Qc
        self.AireQr += (D2 - D1) * self.Qr
        self.AireBr += (D2 - D1) * self.Br

if __name__ == '__main__':

    DateSimualtion = 00
    centreMaintenance = CentreDeMaintenance(DateSimualtion)
    evenement = Evenement("accesReparation", centreMaintenance.dateSimulation)
    centreMaintenance.echeancier.add(evenement)

    while(centreMaintenance.echancier != ()):
        evt = centreMaintenance.echeancier.__getitem__()
        centreMaintenance.mise_A_Jour_Aires(centreMaintenance.dateSimulation,(Evenement)evt.dateEvenement)
        centreMaintenance.dateSimulation = (Evenement)evt.dateEvenement

        if((Evenement)evt.evenement == "debutSimulation"):
            centreMaintenance.debutSimulation()
        elif ((Evenement)evt.evenement == "finSimulation"):
            centreMaintenance.finSimulation()
        elif ((Evenement)evt.evenement == "arriveeBus"):
            centreMaintenance.arriveeBus()
        elif ((Evenement)evt.evenement == "arriveeFileC"):
            centreMaintenance.arriveeFileC()
        elif ((Evenement)evt.evenement == "accesControle"):
            centreMaintenance.accesControle()
        elif ((Evenement)evt.evenement == "departControle"):
            centreMaintenance.departControle()
        elif ((Evenement)evt.evenement == "arriveeFileR"):
            centreMaintenance.arriveeFileR()
        elif ((Evenement)evt.evenement == "accesReparation"):
            centreMaintenance.accesReparation()
        elif ((Evenement)evt.evenement == "departReparation"):
            centreMaintenance.departReparation()
        else:
            print("evenement inconnu")


