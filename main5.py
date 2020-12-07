# TP Simulation
import random
import numpy
import statistics
import matplotlib.pyplot as plt

tempsSimulation = 240
nbReplications = 20
m = 200
w = 30

class Evenement:

    def __init__(self, pNomEvenement, pDate):
        # Evenement
        self.nomEvenement = pNomEvenement
        # Date
        self.dateEvenement = pDate


class CentreDeMaintenance:
    NbBus = 0
    NbBusControle = 0
    NbBusRep = 0
    AireQc, AireQr, AireBr = 0.0, 0.0, 0.0
    Qc, Qr, Bc, Br = 0, 0, 0, 0
    echeancier = []

    tempsAttenteMoyenC = 0.0
    tempsAttenteMoyenR = 0.0
    TauxUtilsiationCR = 0.0

    tailleMoyenneFileC = 0.0
    tailleMoyenneFileR = 0.0

    tempsAttenteMaxFileC = 0.0
    tempsAttenteMaxFileR = 0.0

    def __init__(self, pDate):
        # Date simualtion en heures
        self.dateSimulation = pDate

    def insertEvenement(self, evenement):
        notInserted = True
        i = 0
        while (notInserted and i < len(self.echeancier)):
            if (self.echeancier[i].dateEvenement >= evenement.dateEvenement):
                self.echeancier.insert(i, evenement)
                notInserted = False
            i += 1
        if (i == len(self.echeancier) and notInserted):
            self.echeancier.append(evenement)

    def debutSimulation(self):
        print("Debut Simulation")
        evenement = Evenement("arriveeBus", self.dateSimulation + numpy.random.exponential(2))
        self.insertEvenement(evenement)
        evenement = Evenement("finSimulation", tempsSimulation)
        self.insertEvenement(evenement)

    def finSimulation(self):
        print("Fin Simualtion")
        self.echeancier.clear()

        if (self.NbBus == 0):
            self.tempsAttenteMoyenC = 0  # on ne tiendra pas compte de cette valeur
        else:
            self.tempsAttenteMoyenC = self.AireQc / self.NbBus

        if (self.NbBusRep == 0):
            self.tempsAttenteMoyenR = 0  # on ne tiendra pas compte de cette valeur
        else:
            self.tempsAttenteMoyenR = self.AireQr / self.NbBusRep

        if (self.NbBusRep == 0):
            self.TauxUtilsiationCR = 0
        else:
            self.TauxUtilsiationCR = self.AireBr / (2 * tempsSimulation)

        self.tailleMoyenneFileC = self.AireQc / tempsSimulation
        self.tailleMoyenneFileR = self.AireQr / tempsSimulation

    def arriveeBus(self):
        # print("arrivee Bus")
        evenement = Evenement("arriveeBus", self.dateSimulation + numpy.random.exponential(2))
        self.insertEvenement(evenement)
        self.NbBus += 1
        evenement = Evenement("arriveeFileC", self.dateSimulation)
        self.insertEvenement(evenement)

    def arriveeFileC(self):
        # print("Arrivé file controle")
        self.Qc += 1
        if (self.Bc == 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.insertEvenement(evenement)

    def accesControle(self):
        # print("Acces controle")
        self.Qc -= 1
        self.Bc = 1
        self.NbBusControle += 1
        evenement = Evenement("departControle", self.dateSimulation + random.uniform(0.25, 1.0833))
        self.insertEvenement(evenement)

    def departControle(self):
        # print("Depart Controle")
        self.Bc = 0
        if (self.Qc > 0):
            evenement = Evenement("accesControle", self.dateSimulation)
            self.insertEvenement(evenement)
        if (random.random() < 0.3):
            evenement = Evenement("arriveeFileR", self.dateSimulation)
            self.insertEvenement(evenement)

    def arriveeFileR(self):
        # print("Arrivee file reparation")
        self.Qr += 1
        self.NbBusRep += 1
        if (self.Br < 2):
            evenement = Evenement("accesReparation", self.dateSimulation)
            self.insertEvenement(evenement)

    def accesReparation(self):
        # print("Arrivé reparation")
        self.Qr -= 1
        self.Br += 1
        evenement = Evenement("departReparation", self.dateSimulation + random.uniform(2.1, 4.5))
        self.insertEvenement(evenement)

    def departReparation(self):
        # print("Depart reparation")
        self.Br -= 1
        if (self.Qr > 0):
            evenement = Evenement("accesReparation", self.dateSimulation)
            self.insertEvenement(evenement)

    def mise_A_Jour_Aires(self, D1, D2):
        self.AireQc += (D2 - D1) * self.Qc
        self.AireQr += (D2 - D1) * self.Qr
        self.AireBr += (D2 - D1) * self.Br
        self.calcultempsAttenteMaxFileC((D2 - D1) * self.Qc)
        self.calcultempsAttenteMaxFileR((D2 - D1) * self.Qr)

    def calcultempsAttenteMaxFileC(self, param):
        if param > self.tempsAttenteMaxFileC:
            self.tempsAttenteMaxFileC = param

    def calcultempsAttenteMaxFileR(self, param):
        if param > self.tempsAttenteMaxFileC:
            self.tempsAttenteMaxFileR = param


def moyennesMobiles(listeMoyennes,w):
    mB = len(listeMoyennes)
    listeRetour = []
    moyenneBuffer = 0
    for i in range(1,mB+1):
        if(i<=w):
            for u in range(2*i):
                moyenneBuffer+=listeMoyennes[u]
            moyenneBuffer/=2*i-1
            listeRetour.append(moyenneBuffer)
        elif(i>w and i <(mB-w)):
            for u in range(w):
                moyenneBuffer+=listeMoyennes[u+i]
            moyenneBuffer/=2*w+1
            listeRetour.append(moyenneBuffer)
        moyenneBuffer=0
    return listeRetour



if __name__ == '__main__':

    listeMoyenneSelonM = []
    for k in range(m+w):
        for i in range(nbReplications):

            listTempsAttenteMoyenC = []
            listTempsAttenteMoyenR = []
            listTauxUtilsiationCR = []

            listTempsAttenteMaxFileC = []
            listTempsAttenteMaxFileR = []

            listTailleMoyenneFileC = []
            listTailleMoyenneFileR = []

            print("\n \nreplication : " + str(i))

            DateSimulation = 0
            centreMaintenance = CentreDeMaintenance(DateSimulation)
            evenement = Evenement("debutSimulation", centreMaintenance.dateSimulation)
            centreMaintenance.echeancier.append(evenement)

            while (centreMaintenance.echeancier):

                if m != -1:
                    if centreMaintenance.NbBusControle >= m:
                        break

                evt = centreMaintenance.echeancier.pop(0)
                centreMaintenance.mise_A_Jour_Aires(centreMaintenance.dateSimulation, evt.dateEvenement)
                centreMaintenance.dateSimulation = evt.dateEvenement

                if (evt.nomEvenement == "debutSimulation"):
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

            listTempsAttenteMoyenC.append(centreMaintenance.tempsAttenteMoyenC)

            listTempsAttenteMoyenR.append(centreMaintenance.tempsAttenteMoyenR)

            listTauxUtilsiationCR.append(centreMaintenance.TauxUtilsiationCR)

            listTailleMoyenneFileC.append(centreMaintenance.tailleMoyenneFileC)

            listTailleMoyenneFileR.append(centreMaintenance.tailleMoyenneFileR)

            listTempsAttenteMaxFileC.append(centreMaintenance.tempsAttenteMaxFileC)
            listTempsAttenteMaxFileR.append(centreMaintenance.tempsAttenteMaxFileR)

        moyenneTpsAttMoyAvtCtrl = statistics.mean(listTempsAttenteMoyenC)
        moyenneTpsAttMoyAvtRep = statistics.mean(listTempsAttenteMoyenR)
        moyenneTauxUtilisationCentreRep = statistics.mean(listTauxUtilsiationCR)
        moyenneTailleMoyenneFileC = statistics.mean(listTailleMoyenneFileC)
        moyenneTailleMoyenneFileR = statistics.mean(listTailleMoyenneFileR)


        listeMoyenneSelonM.append(moyenneTpsAttMoyAvtCtrl)

    resultatWelch = moyennesMobiles(listeMoyenneSelonM, w)
    print("Moyennes mobiles = " + str(resultatWelch))
    # création de données
    arr = numpy.array(resultatWelch)
    x = numpy.linspace(0, m, m-1)
    y = arr

    plt.plot(x, y)
    plt.show()  # affiche le graphique (optionnel dans Jupyter)


