from __future__ import annotations
from num_generator import generator_id, generator_kontonummer


class Kunde:
    def __init__(self, name: str, kunde_id: int, bank: Bank) -> None:
        self.name = name
        self.kunde_id = kunde_id
        self.kontos = []

    def info(self) -> None:
        print(
            f"----------------------- \
            \nName: {self.name} \
            \nID: {self.kunde_id} \
            \n--- Kontos ---")
        for konto in self.kontos:
            print(f"Kontonummer: {konto.nummer}     Guthaben: {konto.guthaben}")


class Konto:
    def __init__(
        self,
        nummer: int,
        inhaber: Kunde,
        anfangsguthaben: float,
    ) -> None:

        self.nummer = nummer
        self.inhaber = inhaber
        self.guthaben = anfangsguthaben


    def info(self) -> None:
        print(
            f"----------------------- \
            \n{self.__class__.__name__} \
            \nKontonummer: {self.nummer} \
            \nInhaber: {self.inhaber.name} \
            \nGuthaben: {self.guthaben}")


    def einzahlung(self, betrag: float) -> None:
        self.guthaben += betrag
        print(f"Betrag von {betrag} Euro wurde erfolgreich eingezahlt.")


    def kontostandabfragen(self):
        pass


class Bank:
    def __init__(self, name: str) -> None:
        self.name = name
        self.kunden = []
        self.gen_id = generator_id()
        self.gen_kn = generator_kontonummer()


    def kunde_bekommen(self, kunde_id: int) -> Kunde | None:
        for kunde in self.kunden:
            if kunde.kunde_id == kunde_id:
                return kunde
    

    def kunde_hinzufuegen(
        self,
        kundenname: str,
        konto_art: str,
        anfangsguthaben: float = 0,
        zinssatz: float = 0,
        ueberziehungslimit: float = 0
    ) -> Kunde | None:

        kunde_id = next(self.gen_id)
        
        kunde = Kunde(kundenname, kunde_id, self)
        self.kunden.append(kunde)

        self.konto_oeffnen(kunde, konto_art, anfangsguthaben, zinssatz, ueberziehungslimit)

        return kunde


    def kunde_entfernen(self, kunde_id: int) -> None:
        kunde = self.kunde_bekommen(kunde_id)

        if not kunde:
            raise ValueError(f"Kunde unter ID '{kunde_id}' konnte nicht gefunden werden.")

        self.kunden.remove(kunde)

    @property
    def kontos(self) -> list[Konto]:
        return [konto for kunde in self.kunden for konto in kunde.kontos]


    # def kunde_kontos_bekommen(self, kunde_id: int) -> list[Konto] | None:
    #     kunde = self.kunde_bekommen(kunde_id)
    #     if kunde:
    #         return [konto for konto in kunde.kontos]


    def konto_bekommen(self, kontonummer: int) -> Konto | None:
        for konto in self.kontos:
            if konto.nummer == kontonummer:
                return konto


    def konto_oeffnen(
        self,
        kunde: Kunde,
        konto_art: str,
        anfangsguthaben: float,
        zinssatz: float = 0,
        ueberziehungslimit: float = 0
    ) -> Konto:

        kontonummer = next(self.gen_kn)

        if konto_art == "G":
            konto = Girokonto(kontonummer, kunde, anfangsguthaben, ueberziehungslimit)
        elif konto_art == "S":
            konto = Sparkonto(kontonummer, kunde, anfangsguthaben, zinssatz)

        kunde.kontos.append(konto)

        return konto


    def konto_schliessen(self, kontonummer: int) -> None:
        konto = self.konto_bekommen(kontonummer)

        if not konto:
            raise ValueError(f"Konto unter der Nummer '{kontonummer}' konnte nicht gefunden werden.")

        konto.kunde.kontos.remove(konto)


class Sparkonto(Konto):
    def __init__(self,
                nummer: int,
                inhaber: Kunde,
                anfangsguthaben: float,
                zinssatz: float) -> None:

        super().__init__(nummer, inhaber, anfangsguthaben)
        self.zinssatz = zinssatz


    def abhebung(self, betrag: float) -> bool:
        if self.guthaben < betrag:
            return False

        self.guthaben -= betrag
        return True


    def zinsberechnung(self) -> float:
        self.guthaben += self.guthaben * 0.01 * self.zinssatz
        return self.guthaben


    def info(self) -> None:
        super().info()
        print(f"Zinssatz: {self.zinssatz}")


class Girokonto(Konto):
    def __init__(self,
                nummer: int,
                inhaber: Kunde,
                anfangsguthaben: float,
                ueberziehungslimit: float) -> None:

        super().__init__(nummer, inhaber, anfangsguthaben)
        self.ueberziehungslimit = ueberziehungslimit


    def abhebung(self, betrag: float) -> None:
        if (self.guthaben + self.ueberziehungslimit) < betrag:
            return False

        self.guthaben -= betrag
        return True


    def info(self) -> None:
        super().info()
        print(f"Überziehungslimit: {self.ueberziehungslimit}")
