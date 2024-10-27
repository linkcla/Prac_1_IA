import copy

from mpl_toolkits.mplot3d.art3d import juggle_axes

from practica import config
from practica.joc import Laberint, Accions


class EstatMinimax:

    def __init__(self, parets: set, desti: tuple[int, int], agents: dict, cami=None, jugador=True):
        if cami is None:
            cami = []

        self.__parets = parets
        self.__desti = desti
        #self.__posicio = agents["MAX"] if jugador else agents["MIN"]
        self.__agents = agents

        # cami --> lista(Moure|Botar, direcció)
        self.cami = cami
        self.jugador = jugador # True si es el turno de MAX, False si es el turno de MIN

    def __hash__(self):
        return hash((self.__agents["MAX"], self.__agents["MIN"], self.jugador, tuple(self.__parets)))

    # Metodo que comprueba si dos estados son iguales
    def __eq__(self, other):
        #return self.__posicio == other.__posicio and self.jugador == other.jugador and self.__parets == other.__parets
        return self.__agents == other.__agents and self.__parets == other.__parets

    # Metodo que comprueba si la posición es legal (no hay pared) y está dentro del tablero
    def _legal(self) -> bool:
        pos_aux = self.__agents["MAX"] if not self.jugador else self.__agents["MIN"]

        return (not pos_aux in self.__parets) and \
            (0 <= pos_aux[0] < config.mida[0] and 0 <= pos_aux[1] < config.mida[1]) and \
            self.__agents["MAX"] != self.__agents["MIN"]

    # Metodo que comprueba si la posición es el destino
    def es_meta(self) -> bool:
        pos_aux = self.__agents["MAX"] if self.jugador else self.__agents["MIN"]
        return pos_aux == self.__desti

    def generar_fill(self) -> list:
        pos_aux = self.__agents["MAX"] if self.jugador else self.__agents["MIN"]
        estats_generats = []

        for accio in (Accions.MOURE, Accions.BOTAR):
            for direccio in Laberint.MOVS:
                ## !!!!!!!!!! POSIBLE OPTIMIZACIÓN !!!!!!!!!!
                nou_estat = copy.deepcopy(self)

                # Añadimos la acción actual a `cami`
                nou_estat.cami.append((accio, direccio))

                # Calculamos la nueva posición y cambiamos el turno
                nom = "MAX" if self.jugador else "MIN"
                nou_estat.__agents[nom] =  self.__obte_pos(nou_estat.__agents[nom], self.__accio_get_value(accio), direccio)

                nou_estat.jugador = not self.jugador

                # Si el nuevo estado es legal, lo añadimos a los estados generados
                if nou_estat._legal():
                    estats_generats.append(nou_estat)
                    #print(f"Generado nuevo estado: {nou_estat}")

        return estats_generats

    def calc_heuristica(self):
        # Heurística basada en la distancia Manhattan
        nom = "MAX" if self.jugador else "MIN"
        heuristica = abs(self.__agents[nom][0] - self.__desti[0]) + abs(self.__agents[nom][1] - self.__desti[1])

        return heuristica

    def __accio_get_value(self, accio: Accions):
        if accio == Accions.MOURE:
            return 1
        elif accio == Accions.BOTAR:
            return 2
        else:
            return 0

    # Metodo que devuelve un string con la información del estado
    def __str__(self):
        return f"Posición MAX: {self.__agents["MAX"]},Posición MIN: {self.__agents["MIN"]}, Destino: {self.__desti}, Jugador: {self.jugador}"

    def __obte_pos(self, pos_original: tuple[int, int], multiplicador: int, direccio: str):
        aux = (
            Laberint.MOVS[direccio][0] * multiplicador + pos_original[0],
            Laberint.MOVS[direccio][1] * multiplicador + pos_original[1],
        )
        return aux