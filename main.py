# TP Simulation
import random
import numpy

class Evenement:

    def __init__(self,pNomEvenement,pDate):
        #Evenement
        self.nomEvenement = pNomEvenement
        #Date
        self.dateEvenement = pDate


class CentreDeMaintenance :

    NbBus = 0
    NbBusRep = 0
    AireQc,AireQr,AireBr=0,0,0
    Qc,Qr,Bc,Br=0,0,0,0
    echeancier = []

    def insertEvenement(self, evenement):
        notInserted = True
        i = 0
        while (notInserted and i < len(self.echeancier)):
            if (self.echeancier[i].dateEvenement >= evenement.dateEvenement):
                self.echeancier.insert(i, evenement)
                notInserted = False
            i += 1
        if (i == len(self.echeancier)):
            self.echeancier.append(evenement)

    def __init__(self,pDate):

        #Date simualtion en heures
        self.dateSimulation = pDate

    def debutSimulation(self):
        print("DebutSimulation")
        evenement = Evenement("arriveeBus",self.dateSimulation + numpy.random.exponential(2))
        self.insertEvenement(evenement)
        evenement = Evenement("finSimulation", 160)
        self.insertEvenement(evenement)

    def finSimulation(self):
        print("Fin Simualtion")
        self.echeancier = []
        tempsAttenteMoyenC = self.AireQc / self.NbBus
        tempsAttenteMoyenR = self.AireQr / self.NbBusRep
        TauxUtilsiationCR = self.AireBr /(2*160)


    def arriveeBus(self):
        print("arriveeBus")
        evenement = Evenement("arriveeBus", self.dateSimulation + numpy.random.exponential(2))
        self.insertEvenement(evenement)
        self.NbBus += 1
        evenement = Evenement("arriveeFileC", self.dateSimulation)
        self.insertEvenement(evenement)

    def arriveeFileC(self):
        print("Arrivé file controle")
        self.Qc += 1
        if(self.Bc == 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.insertEvenement(evenement)

    def accesControle(self):
        print("Acces controle")
        self.Qc -= 1
        self.Bc = 1
        evenement = Evenement("departControle", self.dateSimulation + random.uniform(0.25, 1.0833))
        self.insertEvenement(evenement)

    def departControle(self):
        print("Depart controle")
        self.Bc = 0
        if (self.Qc > 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.insertEvenement(evenement)
        if(random.random() < 0.33):
            evenement = Evenement("arriveeFileR", self.dateSimulation)
            self.insertEvenement(evenement)

    def arriveeFileR(self):
        print("Arrivé file reparation")
        self.Qr += 1
        self.NbBusRep += 1
        if (self.Br < 2):
            evenement = Evenement("accesReparation", self.dateSimulation)
            self.insertEvenement(evenement)

    def accesReparation(self):
        print("Arrivé reparation")
        self.Qr -= 1
        self.Br += 1
        evenement = Evenement("departReparation", self.dateSimulation + random.uniform(2.1, 4.5))
        self.insertEvenement(evenement)

    def departReparation(self):
        print("Depart reparation")
        self.Br -= 1
        if(self.Qr>0):
            evenement = Evenement("debutSimulation", self.dateSimulation)
            self.insertEvenement(evenement)


    def mise_A_Jour_Aires(self,D1,D2):
        self.AireQc += (D2-D1)*self.Qc
        self.AireQr += (D2 - D1) * self.Qr
        self.AireBr += (D2 - D1) * self.Br

if __name__ == '__main__':

    DateSimulation = 0
    centreMaintenance = CentreDeMaintenance(DateSimulation)
    evenement = Evenement("debutSimulation", centreMaintenance.dateSimulation)
    centreMaintenance.echeancier.append(evenement)

    while(centreMaintenance.echeancier):
        evt = centreMaintenance.echeancier.pop(0)
        centreMaintenance.mise_A_Jour_Aires(centreMaintenance.dateSimulation,evt.dateEvenement)
        centreMaintenance.dateSimulation = evt.dateEvenement

        if(evt.nomEvenement == "debutSimulation"):
            centreMaintenance.debutSimulation()
        elif (evt.nomEvenement == "finSimulation"):
            centreMaintenance.finSimulation()
        elif (evt.nomEvenement == "arriveeBus"):
            centreMaintenance.arriveeBus()
        elif (evt.nomEvenement == "arriveeFileC"):
            centreMaintenance.arriveeFileC()
        elif (evt.nomEvenement == "accesControle"):
            centreMaintenance.accesControle()
        elif (evt.nomEvenement == "departControle"):
            centreMaintenance.departControle()
        elif (evt.nomEvenement == "arriveeFileR"):
            centreMaintenance.arriveeFileR()
        elif (evt.nomEvenement == "accesReparation"):
            centreMaintenance.accesReparation()
        elif (evt.nomEvenement == "departReparation"):
            centreMaintenance.departReparation()
        else:
            print("evenement inconnu")