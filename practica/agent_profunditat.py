import random

from practica import joc
from practica.joc import Accions

class ViatgerProfunditat(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(ViatgerProfunditat, self).__init__(*args, **kwargs)
        self.__proves = [
            (Accions.MOURE, "E"),
            (Accions.MOURE, "S"),
            (Accions.MOURE, "N"),
            (Accions.MOURE, "O"),
            (Accions.BOTAR, "S"),
            (Accions.BOTAR, "N"),
            (Accions.BOTAR, "E"),
            (Accions.BOTAR, "O"),
            (Accions.POSAR_PARET, "S"),
            (Accions.POSAR_PARET, "N"),
            (Accions.POSAR_PARET, "E"),
            (Accions.POSAR_PARET, "O"),
        ]
        self.__per_visitar = None
        self.__visitats = None
        self.__cami_exit = None
                

    def pinta(self, display):
        pass

    def cerca(self, percepcio : dict) -> bool:
        self.__per_visitar = []
        self.__visitats = set()
        exit = False
        
        tablero = percepcio["TAULELL"]
        destino = percepcio["DESTI"]
        pos_actual = self.posicio
        

        #                          pos actual, camino
        self.__per_visitar.append((pos_actual, [])) 

        # Mientras haya casillas por visitar
        while self.__per_visitar:
            (posicion, camino) = self.__per_visitar.pop(-1)
            
            if posicion in self.__visitats or not 

        return exit

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__proves:
            acc = random.choice(self.__proves)
            return acc
        return Accions.ESPERAR
