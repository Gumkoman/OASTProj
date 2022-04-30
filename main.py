import myparser
import classes
from BurteForce import BruteForce
import Evolutionary
inputList= ['','input/net4.txt','input/net12_1.txt','input/net12_2.txt']



def simulationEvolution():
    pass


def main():
    while(1):
        choice = input("Wybierz plik tekstowy z listy:\n1.net4.txt\n2.net12_1.txt\n3.net12_2.txt\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        else:
            print("Podano nie poprawną nazwę pliku tekstowego")
            break
        alghoritmType = input("Wybierz rodzaj algorytmu:\n1.BruteForce\n2.Algorytm Ewolucyjny\n")
        if alghoritmType =="1":
            demandList = myparser.createDemands(inputList[int(choice)])
            linkList = myparser.createNetwork(inputList[int(choice)])
            bf = BruteForce(demandList,linkList)
            bf.run(demandList)
        elif alghoritmType == "2":
            seed = int(input("Podaj wartość seed\n"))
            deafultPopulationSize = int(input("Podaj rozmiar populacji\n"))
            crossoverProbabilityMul = int(input("Podaj corossover probability\n"))
            stopAlgorithm = input("Podaj Kryterium zatrzymania algorytmu\n1.Liczba sekund\n2.Liczba generacji\n3.Liczba mutacji\n4.Brak poprawy przez N populacji\n")
            secondsNumber=0
            generationNumber=0
            mutationNumber=0
            noImproveNumber=0
            if stopAlgorithm == '1':
                secondsNumber = int(input("Podaj liczbę sekund działania algorytmu\n"))
            elif stopAlgorithm == '2':
                generationNumber = int(input("Podaj liczbę generacji działania algorytmu\n"))
            elif stopAlgorithm == '3':
                mutationNumber = int(input("Podaj liczbę mutacji działania algorytmu\n"))
            elif stopAlgorithm == '4':
                noImproveNumber = int(input("Podaj liczbę generacji bez poprawy działania algorytmu\n"))
            else:
                print("Podano nie poprawną wartość")
                break
            demandList = myparser.createDemands(inputList[int(choice)])
            linkList = myparser.createNetwork(inputList[int(choice)])
            ev = Evolutionary.Evelutionary(demandList,linkList,stopAlgorithm,secondsNumber,generationNumber,mutationNumber,noImproveNumber,seed,deafultPopulationSize)
            ev.evolutionarySimulation()

        else:
            print("Podano nie poprawną wartość")
            break
        print(choice,alghoritmType)
        break
        
if __name__ == "__main__":
    main()