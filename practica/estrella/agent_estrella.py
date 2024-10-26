from queue import PriorityQueue

from practica import joc
from practica.estrella.estat_estrella import EstatEstrella
from practica.joc import Accions


class ViatgerA(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(ViatgerA, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__cami_exit = None
        

    def pinta(self, display):
        pass

    def cerca(self, estat_inicial: EstatEstrella):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial))
        
        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.generar_fill()
            
            for fill in estats_fills:
                self.__oberts.put((fill.calc_heuristica(), fill))

            self.__tancats.add(actual)

        if actual.es_meta():
            self.__cami_exit = actual.cami
    
    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__cami_exit is None:    
            estat_inicial = EstatEstrella(
                parets = percepcio["PARETS"],
                desti = percepcio["DESTI"],
                # Para seleccionar la posicion del unico agente del diccionario
                posicio = next(iter(percepcio["AGENTS"].values()))
            )

            self.cerca(estat_inicial)
        
        if self.__cami_exit:
            accio, direccio = self.__cami_exit.pop(0)

            print("Accio:", accio, "Direccio:", direccio)
            return accio, direccio
        else:
            return Accions.ESPERAR
        
