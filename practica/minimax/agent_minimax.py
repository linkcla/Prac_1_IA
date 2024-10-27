from practica import joc, config
from practica.minimax.estat_minimax import EstatMinimax
from practica.joc import Accions

class ViatgerMinimax(joc.Viatger):
    PODA = False

    def __init__(self, *args, **kwargs):
        super(ViatgerMinimax, self).__init__(*args, **kwargs)
        self.__per_visitar = set()
        self.__visitats = {}
        self.__cami_exit = None

    def cerca(self, estat: EstatMinimax, alpha, beta, torn_max=True, profunditat=config.limite_profundidad):

        if estat in self.__per_visitar: return estat, estat.calc_heuristica()

        self.__per_visitar.add(estat)

        if estat.es_meta():
            return estat, float("inf") if torn_max else -float("inf")

        if profunditat == 0: return estat, estat.calc_heuristica() if estat.jugador else -estat.calc_heuristica()

        puntuacio_fills = []

        aux = estat.generar_fill()
        for fill in aux:
            if fill not in self.__visitats:
                punt_fill = self.cerca(fill, alpha, beta, not torn_max, profunditat - 1)

                # Poda alfa-beta
                if ViatgerMinimax.PODA:
                    if torn_max:
                        alpha = max(alpha, punt_fill[1])
                    else:
                        beta = min(beta, punt_fill[1])
                    if alpha >= beta:
                        print(f"Poda aplicada: alpha={alpha}, beta={beta}")
                        break

                self.__visitats[fill] = punt_fill
            puntuacio_fills.append(self.__visitats[fill])

        self.__per_visitar.remove(estat)

        if not puntuacio_fills:
            return estat, estat.calc_heuristica()

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            #print(f"Mejor movimiento para MAX: {puntuacio_fills[0]}")
            return puntuacio_fills[0]
        else:
            #print(f"Mejor movimiento para MIN: {puntuacio_fills[0]}")
            return puntuacio_fills[-1]

    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        self.__visitats = dict()
        estat_inicial = EstatMinimax(
            parets = percepcio["PARETS"],
            desti = percepcio["DESTI"],
            # Para seleccionar la posicion del unico agente del diccionario
            agents = percepcio["AGENTS"]
        )

        print("Estat inicial: ", estat_inicial)
        res = self.cerca(estat_inicial, alpha =- float("inf"), beta = float("inf"))

        if isinstance(res, tuple) and res[0].cami is not None and len(res[0].cami) > 0:
            accio, direccio = res[0].cami[0]

            print("Accion: ", accio, "Direccion: ", direccio)
            return accio, direccio
        else:
            return Accions.ESPERAR


