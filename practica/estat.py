import copy
from practica.joc import Laberint, Accions

class Estat:

    def __init__(self, parets: set, desti: tuple[int, int], posicio: tuple[int, int], cami = None):
        if cami is None:
            cami = []
        
        self.__parets = parets
        self.__desti = desti
        self.__posicio = posicio

        # cami --> lista(Moure|Botar, direcció)
        self.cami = cami
    
    def __hash__(self):
        return hash((self.__desti, self.__posicio))
    
    # Metodo que comprueba si dos estados son iguales
    def __eq__(self, other):
        return (self.__parets == other.__parets
                and self.__desti == other.__desti
                and self.__posicio == other.__posicio)
    
    # Metodo que comprueba si la posición es legal (no hay pared)
    def _legal(self) -> bool:
        return not self.__parets.__contains__(self.__posicio)
    
    # Metodo que comprueba si la posición es el destino
    def es_meta(self) -> bool:
        return self.__posicio == self.__desti
    
    def generar_fill(self) -> list:
        estats_generats = []
        
        # Por cada acción posible (MOURE, BOTAR)
        for accio in {Accions.MOURE, Accions.BOTAR}:
            # Por cada dirección posible (N, S, E, O)
            for direccio in Laberint.MOVS:
                # !!!!!!!!!! POSIBLE OPTIMIZACIÓN !!!!!!!!!!
                nou_estat = copy.deepcopy(self)
                nou_estat.pare = (self)
                #                tipo de movimiento, en que dirección
                nou_estat.cami.append([accio, direccio])
                nou_estat.__posicio = Laberint.obte_pos(nou_estat.__posicio, accio.value, direccio)
                
                if nou_estat._legal():
                    estats_generats.append(nou_estat)
                
        return estats_generats
    
    # Metodo que devuelve un string con la información del estado   
    def __str__(self):
        return f"Posicio: {self.__posicio}, Desti: {self.__desti}, Parets: {self.__parets}, Cami: {self.cami}"
                    


                