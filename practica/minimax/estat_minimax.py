import copy
from practica import config
from practica.joc import Laberint, Accions


class EstatMinimax:

    def __init__(self, pos_max: tuple[int, int], pos_min: tuple[int, int], desti: tuple[int, int],parets: set, turno=True, cami=None):
        if cami is None:
            cami = []
        self.__pos_max = pos_max
        self.__pos_min = pos_min
        self.__desti = desti
        self.__parets = parets
        self.__turno = turno
        self.__cami = cami
        #self.__cost_max = 0
        #self.__cost_min = 0

    def __hash__(self):
        return hash((self.__pos_max, self.__pos_min))

    # Metodo que comprueba si dos estados son iguales
    def __eq__(self, other):
        return (self.__pos_max == other.__pos_min and \
                self.__pos_min == other.__pos_min and \
                self.__parets == other.__parets)

    # Metodo que comprueba si la posición es legal (no hay pared) y está dentro del tablero
    def _legal(self) -> bool:
        return ((not self.__pos_max in self.__parets) and \
                0 <= self.__pos_max[0] < config.mida[0] and \
                0 <= self.__pos_max[1] < config.mida[1]) and \
                ((not self.__pos_min in self.__parets) and \
                0 <= self.__pos_min[0] < config.mida[0] and \
                0 <= self.__pos_min[1] < config.mida[1])

    # Metodo que comprueba si la posición es el destino
    def es_meta(self) -> bool:
        return  self.__pos_max == self.__desti or self.__pos_min == self.__desti

    def generar_fill(self) -> list:
        estats_generats = []

        for accio in (Accions.MOURE, Accions.BOTAR):
            for direccio in Laberint.MOVS:
                ## !!!!!!!!!! POSIBLE OPTIMIZACIÓN !!!!!!!!!!
                nou_estat = copy.deepcopy(self)

                nou_estat.__cami.append([accio, direccio])
                if self.__turno:
                    nou_estat.__pos_max = self.__obte_pos(nou_estat.__pos_max, self.__accio_get_value(accio), direccio)
                    #nou_estat.__cost_max = nou_estat.__cost_max + self.__accio_get_value(accio)
                else:
                    nou_estat.__pos_min = self.__obte_pos(nou_estat.__pos_min, self.__accio_get_value(accio), direccio)
                    #nou_estat.__cost_min = nou_estat.__cost_min + self.__accio_get_value(accio)

                nou_estat.__turno = not nou_estat.__turno

                if nou_estat._legal():
                    estats_generats.append(nou_estat)

        return estats_generats

    def calc_heuristica(self):
        # Heuristica: diferecia de distancias Manhattan
        x0, y0 = self.__desti
        #         ----------- MANHATTAN MIN ---------------------              ----------- MANHATTAN MAX ---------------------
        return (abs(x0 - self.__pos_min[0]) + abs(y0 - self.__pos_min[1])) - (abs(x0 - self.__pos_max[0]) + abs(y0 - self.__pos_max[1]))
        #return (abs(x0 - self.__pos_min[0]) + abs(y0 - self.__pos_min[1])) - (abs(x0 - self.__pos_max[0]) + abs(y0 - self.__pos_max[1])) + self.__cost_min - self.__cost_max
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
        return f"Posicio MAX: {self.__pos_max}, Posicio MIN: {self.__pos_min}, Desti: {self.__desti}, Parets: {self.__parets}, Cami: {self.cami}"

    def __obte_pos(self, pos_original: tuple[int, int], multiplicador: int, direccio: str):
        return (
            Laberint.MOVS[direccio][0] * multiplicador + pos_original[0],
            Laberint.MOVS[direccio][1] * multiplicador + pos_original[1],
        )

    def get_cami(self):
        return self.__cami