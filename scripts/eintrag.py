from __future__ import annotations
from classen import Kunde, Konto, Bank, Sparkonto, Girokonto


def eintrag_konto_daten() -> dict:
    konto_art = input("G - Girokonto | S - Sparkonto: ")
    anfangsguthaben = float(input("Anfangsguthaben: "))
    konto_daten = {
        "konto_art": konto_art,
        "anfangsguthaben": anfangsguthaben
    }

    if konto_art == "G":
        ueberziehungslimit = float(input("Überziehungslimit: "))
        konto_daten["ueberziehungslimit"] = ueberziehungslimit

    elif konto_art == "S":
        zinssatz = float(input("Zinssatz: "))
        konto_daten["zinssatz"] = zinssatz

    return konto_daten


class Eintrag:
    @staticmethod
    def kunde_hinzufuegen(bank: Bank) -> None:
        name = input("Kundenname: ")
        konto_daten = eintrag_konto_daten()

        kunde = bank.kunde_hinzufuegen(name, **konto_daten)

        print("Kunde wurde erfolgreich hinzugefügt")
        kunde.info()
        

    @staticmethod
    def kunde_info(bank: Bank) -> None:
        kunde_id = int(input("Kunde ID: "))
        kunde = bank.kunde_bekommen(kunde_id)
        if kunde:
            kunde.info()
        else:
            print(f"Kunde unter ID '{kunde_id}' konnte nicht gefunden werden.")


    @staticmethod
    def kunde_entfernen(bank: Bank) -> None:
        kunde_id = int(input("Kunde ID: "))
        try:
            bank.kunde_entfernen(kunde_id)
        except ValueError:
            print(f"Kunde unter ID '{kunde_id}' konnte nicht gefunden werden.")
        else:
            print(f"Kunde unter ID '{kunde_id}' wurde erfolgreich gelöscht.")


    @staticmethod
    def konto_hinzufuegen(bank: Bank) -> None:
        kunde_id = int(input("Kunde ID: "))
        kunde = bank.kunde_bekommen(kunde_id)
        if kunde:
            konto_daten = eintrag_konto_daten()
            konto = bank.konto_oeffnen(kunde, **konto_daten)
            print("Konto wurde erfolgreich hinzugefügt")
            konto.info()
        else:
            print(f"Kunde unter ID '{kunde_id}' konnte nicht gefunden werden.")


    @staticmethod
    def konto_info(bank: Bank) -> None:
        kontonummer = int(input("Kontonummer: "))
        konto = bank.konto_bekommen(kontonummer)
        if konto:
            konto.info()
        else:
            print(f"Konto unter der Nummer '{kontonummer}' konnte nicht gefunden werden.")


    @staticmethod
    def konto_entfernen(bank: Bank) -> None:
        kontonummer = int(input("Kontonummer: "))
        try:
            bank.konto_entfernen(kontonummer)
        except ValueError:
            print(f"Konto unter der Nummer '{kontonummer}' konnte nicht gefunden werden.")
        else:
            print(f"Konto unter der Nummer '{kontonummer}' wurde erfolgreich gelöscht.")
