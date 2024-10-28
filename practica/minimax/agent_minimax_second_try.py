import random

from joblib.externals.cloudpickle import instance
from numpy.ma.core import append
from scipy.stats import alpha

from practica import joc, config
from practica.joc import Accions
from practica.minimax.estat_minimax_second_try import EstatMinimax2


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.__cami = None
        self.__visitats = None

    def pinta(self, display):
        pass

    def cerca (self, estat : EstatMinimax2, alpha, beta, torn_max = True, profunditat = config.limite_profundidad):
        if estat.es_meta():
            # Si es el turno de max y ya se ha llegado a la meta quiere decir que el que ha hecho
            #  el úlimo movimiento ha sido el que ha ganado, entonces antes de la jugada de max el
            #  que ha movido ha sido min.
            return estat, (-float('inf') if torn_max else float('-inf'))

        if profunditat == config.limite_profundidad:
            return estat, estat.calc_heuristica() if torn_max else (-1 * estat.calc_heuristica())

        puntuacio_fills = []
        fills = estat.generar_fill()
        # Explorar primero los hijos que estén más cerca --> Poner en la parte de la izquierda del arbol los hijos
        # más proximos a la solución.
        # TODO: revisar si funciona
        fills = sorted(fills)
        for fill in fills:
            if fill not in self.__visitats:
                punt_fill = self.cerca(fill, alpha, beta, not torn_max, (profunditat - 1))

                if config.poda:
                    if torn_max:
                        max(alpha, punt_fill[1])
                    else:
                        min(beta, punt_fill[1])

                    if alpha >= beta:
                        break

                self.__visitats[fill] = punt_fill
            puntuacio_fills = append(self.__visitats[fill])

        puntuacio_fills = sorted(self.__visitats[1])
        if torn_max:
            return puntuacio_fills[0]
        else:
            return puntuacio_fills[-1]

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        self.__visitats = dict()
        estat_inicial = EstatMinimax2(
            pos_max= percepcio["AGENTS"]["MAX"],
            pos_min = percepcio["AGENTS"]["MIN"],
            desti = percepcio["DESTI"],
            parets = percepcio["PARETS"]
        )
        res = self.cerca(estat_inicial, alpha=-float("inf"), beta=float("inf"))

        if instance(res, tuple) and res[0].get_cami is not None and len(res[0].get_cami) > 0:
            accio, direccio = res[0].get_cami()[0]
            return accio, direccio
        else:
            Accions.ESPERAR
