import parser
import classes
from BurteForce import BruteForce

inputList= ['','input/net4.txt','input/net12_1.txt','input/net12_2.txt']




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
            demandList = parser.createDemands(inputList[int(choice)])
            linkList = parser.createNetwork(inputList[int(choice)])
            bf = BruteForce(demandList,linkList)
            bf.run(demandList)
        elif alghoritmType == "2":
            pass
        else:
            print("Podano nie poprawną wartość")
            break
        print(choice,alghoritmType)
        break
        
if __name__ == "__main__":
    main()