import copy
from practica import config
from practica.joc import Laberint, Accions


class EstatEstrella:

    def __init__(self, parets: set, desti: tuple[int, int], posicio: tuple[int, int], cami=None, coste = 0):
        if cami is None:
            cami = []
        self.__parets = parets
        self.__desti = desti
        self.__posicio = posicio

        # cami --> lista(Moure|Botar, direcció)
        self.cami = cami
        self.coste = coste # Costo acumulado g(n)

    def __hash__(self):
        return hash((self.__desti, self.__posicio))

    # Metodo que comprueba si dos estados son iguales
    def __eq__(self, other):
        return self.__posicio == other.__posicio

    # Metodo que comprueba si la posición es legal (no hay pared) y está dentro del tablero
    def _legal(self) -> bool:
        return (not self.__posicio in self.__parets) and (
                    0 <= self.__posicio[0] < config.mida[0] and 0 <= self.__posicio[1] < config.mida[1])

    # Metodo que comprueba si la posición es el destino
    def es_meta(self) -> bool:
        return self.__posicio == self.__desti

    def generar_fill(self) -> list:
        estats_generats = []

        for accio in {Accions.MOURE, Accions.BOTAR}:
            for direccio in Laberint.MOVS:
                ## !!!!!!!!!! POSIBLE OPTIMIZACIÓN !!!!!!!!!!
                nou_estat = copy.deepcopy(self)

                nou_estat.cami.append([accio, direccio])
                nou_estat.__posicio = self.__obte_pos(nou_estat.__posicio, self.__accio_get_value(accio), direccio)
                nou_estat.coste = self.coste + self.__accio_get_value(accio) # coste + accion

                if nou_estat._legal():
                    estats_generats.append(nou_estat)
        return estats_generats

    def calc_heuristica(self):
        # Heuristica: distancia Manhattan
        # posible modificación: sumar 1 por cada pared doble que tenga en una dirección
        heuristica = abs(self.__posicio[0] - self.__desti[0]) + abs(self.__posicio[1] - self.__desti[1])
        print ("Heuristica: ", heuristica, "Coste: ", self.coste)
        return heuristica + self.coste


    def __accio_get_value(self, accio: Accions):
        if accio == Accions.MOURE:
            return 1
        elif accio == Accions.BOTAR:
            return 2

    # Metodo que compara dos estados por su heuristica
    def __lt__(self, other):
        # Devolvemos el estado con menor heuristica
        return self.calc_heuristica() < other.calc_heuristica()

    # Metodo que devuelve un string con la información del estado
    def __str__(self):
        return f"Posicio: {self.__posicio}, Desti: {self.__desti}, Parets: {self.__parets}, Cami: {self.cami}, Coste: {self.coste}"

    def __obte_pos(self, pos_original: tuple[int, int], multiplicador: int, direccio: str):
        return (
            Laberint.MOVS[direccio][0] * multiplicador + pos_original[0],
            Laberint.MOVS[direccio][1] * multiplicador + pos_original[1],
        )