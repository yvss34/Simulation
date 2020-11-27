# TP Simulation
import random
import numpy
import statistics

tempsSimulation = 160
nbReplications = 500


class Evenement:

    def __init__(self, pNomEvenement, pDate):
        # Evenement
        self.nomEvenement = pNomEvenement
        # Date
        self.dateEvenement = pDate


class Bus:

    # accesControle = 1 quand le bus accede au controle
    accesControle = 0

    dateArriveeControle = 0
    dateAccesControle = 0

    # accesReparation = 1 quand le bus accede au controle
    accesReparation = 0

    dateArriveeReparation = 0
    dateAccesReparation = 0

    def __init__(self,pIdentifiant):
        # Identifiant
        self.identifiant = pIdentifiant


class CentreDeMaintenance:
    NbBus = 0
    NbBusRep = 0
    NbBusC = 0
    NbBusR = 0
    AireQc, AireQr, AireBr = 0.0, 0.0, 0.0
    Qc, Qr, Bc, Br = 0, 0, 0, 0
    echeancier = []
    tableauBus = []

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

        bus = Bus(self.NbBus)
        bus.dateArriveeControle = self.dateSimulation
        self.tableauBus.append(bus)

        self.NbBus += 1
        evenement = Evenement("arriveeBus", self.dateSimulation + numpy.random.exponential(2))
        self.insertEvenement(evenement)
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

        for bus in self.tableauBus:
            if(bus.identifiant == self.NbBusC):
                bus.accesControle = 1
                bus.dateAccesControle = self.dateSimulation

        self.NbBusC += 1
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

        for bus in self.tableauBus:
            if(bus.identifiant == self.NbBusRep):
                bus.dateArriveeReparation = self.dateSimulation

        self.NbBusRep += 1
        if (self.Br < 2):
            evenement = Evenement("accesReparation", self.dateSimulation)
            self.insertEvenement(evenement)

    def accesReparation(self):
        # print("Arrivé reparation")
        self.Qr -= 1
        self.Br += 1

        for bus in self.tableauBus:
            if(bus.identifiant == self.NbBusR):
                bus.accesReparation = 1
                bus.dateArriveeReparation = self.dateSimulation

        self.NbBusR += 1
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


if __name__ == '__main__':

    listTempsAttenteMoyenC = []
    listTempsAttenteMoyenR = []
    listTauxUtilsiationCR = []
    listTempsAttenteMaxFileC = []
    listTempsAttenteMaxFileR = []

    listTailleMoyenneFileC = []
    listTailleMoyenneFileR = []


    for i in range(nbReplications):

        print("\n \nreplication : " + str(i))

        DateSimulation = 0
        centreMaintenance = CentreDeMaintenance(DateSimulation)
        evenement = Evenement("debutSimulation", centreMaintenance.dateSimulation)
        centreMaintenance.echeancier.append(evenement)

        while (centreMaintenance.echeancier):

            # print([centreMaintenance.echeancier[i].nomEvenement for i in range(len(centreMaintenance.echeancier))])
            evt = centreMaintenance.echeancier.pop(0)
            if(evt.nomEvenement != "arriveeFileC" or evt.nomEvenement != "arriveeFileR"):
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

    print("temps simulation : ", tempsSimulation)
    print("Moyenne TpsAttMoyAvtCtrl = " + str(statistics.mean(listTempsAttenteMoyenC)) + " sur " + str(nbReplications) + " réplications")
    print("Moyenne TpsAttMoyAvtRep = " + str(statistics.mean(listTempsAttenteMoyenR)) + " sur " + str(nbReplications) + " réplications")
    print("Moyenne TauxUtilisationCentreRep = " + str(statistics.mean(listTauxUtilsiationCR)) + " sur " + str(nbReplications) + " réplications")
    print("temps d'attente max file C = " + str(max(listTempsAttenteMaxFileC)))
    print("temps d'attente max file R = " + str(max(listTempsAttenteMaxFileR)))

    print("Moyenne TailleMoyenneFileC = " + str(statistics.mean(listTailleMoyenneFileC)) + " sur " + str(nbReplications) + " réplications")
    print("Moyenne TailleMoyenneFileR = " + str(statistics.mean(listTailleMoyenneFileR)) + " sur " + str(nbReplications) + " réplications")

    tempsAttMoyenC = 0
    tempsAttMoyenR = 0
    for bus in centreMaintenance.tableauBus:
        if(bus.accesControle == 1):
            tempsAttMoyenC += (bus.dateAccesControle - bus.dateArriveeControle)
        if (bus.accesReparation == 1):
            tempsAttMoyenR += (bus.dateAccesReparation - bus.dateArriveeReparation)

    tempsAttMoyenC = tempsAttMoyenC / centreMaintenance.NbBusC
    tempsAttMoyenR = tempsAttMoyenR / centreMaintenance.NbBusR

    print("TpsAttAvtContole = " + str(tempsAttMoyenC))
    print("TpsAttAvtReparation = " + str(tempsAttMoyenR))
