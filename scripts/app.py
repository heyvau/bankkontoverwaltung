from classen import Kunde, Konto, Bank, Sparkonto, Girokonto
from eintrag import Eintrag


if __name__ == "__main__":
    sparbank = Bank("Sparbank")

    print(f"Willkommen in {sparbank.name}!")

    while True:

        print("\n")
        print("********** Auswahlliste **********")
        print("\n")
        print("0 - Schließen")
        print("1 - Kunde hinzufügen")
        print("2 - Kunde Info")
        print("3 - Kunde entfernen")
        print("4 - Konto hinzufügen")
        print("5 - Konto Info")
        print("6 - Konto entfernen")

        print("\n")
        
        ui = int(input(">> "))

        match ui:
            case 0:
                exit()
            case 1:
                Eintrag.kunde_hinzufuegen(sparbank)
            case 2:
                Eintrag.kunde_info(sparbank)
            case 3:
                Eintrag.kunde_entfernen(sparbank)
            case 4:
                Eintrag.konto_hinzufuegen(sparbank)
            case 5:
                Eintrag.konto_info(sparbank)
            case 6:
                Eintrag.konto_entfernen(sparbank)

        input("ENTER um fortzufahren...")
