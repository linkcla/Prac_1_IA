from practica import joc, config
from practica.estat_minimax import EstatMinimax
from practica.joc import Accions

class ViatgerMinimax(joc.Viatger):
    PODA = True

    def __init__(self, *args, **kwargs):
        super(ViatgerMinimax, self).__init__(*args, **kwargs)
        #self.__per_visitar = None
        self.__visitats = None
        self.__cami_exit = None

    def cerca(self, estat: EstatMinimax, alpha, beta, torn_max=True, profunditat=config.limite_profundidad):
        if estat.es_meta() or profunditat == 0:
            return estat, estat.calc_heuristica()

        puntuacio_fills = []

        for fill in estat.generar_fill():
            if fill not in self.__visitats:
                punt_fill = self.cerca(fill, alpha, beta, not torn_max, profunditat - 1)

                # Poda alfa-beta
                if ViatgerMinimax.PODA:
                    if torn_max:
                        alpha = max(alpha, punt_fill[1])
                    else:
                        beta = min(beta, punt_fill[1])
                    if alpha >= beta:
                        break

                self.__visitats[fill] = punt_fill
            puntuacio_fills.append(self.__visitats[fill])

        if not puntuacio_fills:
            return estat, estat.calc_heuristica()

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            return puntuacio_fills[0]
        else:
            return puntuacio_fills[-1]

    def pinta(self, display):
        pass

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        self.__visitats = dict()
        estat_inicial = EstatMinimax(
            parets = percepcio["PARETS"],
            desti = percepcio["DESTI"],
            # Para seleccionar la posicion del unico agente del diccionario
            posicio = next(iter(percepcio["AGENTS"].values()))
        )

        print("Estat inicial: ", estat_inicial)
        res = self.cerca(estat_inicial, alpha =- float("inf"), beta = float("inf"))

        if isinstance(res, tuple) and res[0].cami is not None and len(res[0].cami) > 0:
            accio, direccio = res[0].cami[0]

            print("Accion: ", accio, "Direccion: ", direccio)
            return accio, direccio
        else:
            return Accions.ESPERAR


