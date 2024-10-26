import copy
from practica import config
from practica.joc import Laberint, Accions


class EstatMinimax:

    def __init__(self, parets: set, desti: tuple[int, int], posicio: tuple[int, int], cami=None, jugador=True):
        if cami is None:
            cami = []
        self.__parets = parets
        self.__desti = desti
        self.__posicio = posicio

        # cami --> lista(Moure|Botar, direcció)
        self.cami = cami
        self.jugador = jugador # True si es el turno del jugador, False si es el turno del enemigo

    def __hash__(self):
        return hash((self.__desti, self.__posicio, self.jugador))

    # Metodo que comprueba si dos estados son iguales
    def __eq__(self, other):
        return self.__posicio == other.__posicio and self.jugador == other.jugador

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

                # Añadimos la acción actual a `cami`
                nuevo_cami = nou_estat.cami + [(accio, direccio)]
                nou_estat.cami = nuevo_cami

                # Calculamos la nueva posición y cambiamos el turno
                nou_estat.__posicio = self.__obte_pos(nou_estat.__posicio, self.__accio_get_value(accio), direccio)
                nou_estat.jugador = not self.jugador

                # Si el nuevo estado es legal, lo añadimos a los estados generados
                if nou_estat._legal():
                    estats_generats.append(nou_estat)

        return estats_generats

    def calc_heuristica(self):
        # Heurística basada en la distancia Manhattan
        heuristica = abs(self.__posicio[0] - self.__desti[0]) + abs(self.__posicio[1] - self.__desti[1])

        return heuristica

    def __accio_get_value(self, accio: Accions):
        if accio == Accions.MOURE:
            return 1
        elif accio == Accions.BOTAR:
            return 2

    # Metodo que devuelve un string con la información del estado
    def __str__(self):
        return f"Posicio: {self.__posicio}, Desti: {self.__desti}, Parets: {self.__parets}, Cami: {self.cami}"

    def __obte_pos(self, pos_original: tuple[int, int], multiplicador: int, direccio: str):
        return (
            Laberint.MOVS[direccio][0] * multiplicador + pos_original[0],
            Laberint.MOVS[direccio][1] * multiplicador + pos_original[1],
        )