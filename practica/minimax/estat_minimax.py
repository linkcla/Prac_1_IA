import copy
from practica import config
from practica.joc import Laberint, Accions


class EstatMinimax:

    def __init__(self, parets: set, desti: tuple[int, int], agents: dict, cami=None, jugador=True):
        if cami is None:
            cami = []
        self.__parets = parets
        self.__desti = desti
        self.__posicio = agents["MAX"] if jugador else agents["MIN"]
        self.__agents = agents

        # cami --> lista(Moure|Botar, direcció)
        self.cami = cami
        self.jugador = jugador # True si es el turno del jugador, False si es el turno del enemigo

    def __hash__(self):
        return hash((self.__posicio, self.jugador, tuple(self.__parets)))

    # Metodo que comprueba si dos estados son iguales
    def __eq__(self, other):
        return self.__posicio == other.__posicio and self.jugador == other.jugador and self.__parets == other.__parets

    # Metodo que comprueba si la posición es legal (no hay pared) y está dentro del tablero
    def _legal(self) -> bool:
        return (not self.__posicio in self.__parets) and \
            (0 <= self.__posicio[0] < config.mida[0] and 0 <= self.__posicio[1] < config.mida[1]) and \
            self.__posicio != self.__obte_pos_adversari()

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
                nou_estat.cami.append((accio, direccio))

                # Calculamos la nueva posición y cambiamos el turno
                nou_estat.__posicio = self.__obte_pos(nou_estat.__posicio, self.__accio_get_value(accio), direccio)
                nou_estat.jugador = not self.jugador

                # Si el nuevo estado es legal, lo añadimos a los estados generados
                if nou_estat._legal():
                    estats_generats.append(nou_estat)
                    print(f"Generado nuevo estado: {nou_estat}")

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
        else:
            return 0

    # Metodo que devuelve un string con la información del estado
    def __str__(self):
        return f"Posición: {self.__posicio}, Destino: {self.__desti}, Jugador: {self.jugador}"

    def __obte_pos(self, pos_original: tuple[int, int], multiplicador: int, direccio: str):
        return (
            Laberint.MOVS[direccio][0] * multiplicador + pos_original[0],
            Laberint.MOVS[direccio][1] * multiplicador + pos_original[1],
        )

    def __obte_pos_adversari(self):
        if self.jugador:
            return self.__agents["MIN"]
        else:
            return self.__agents["MAX"]