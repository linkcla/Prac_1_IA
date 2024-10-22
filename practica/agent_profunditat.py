from practica import joc
from practica.estat import Estat
from practica.joc import Accions


class ViatgerProfunditat(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(ViatgerProfunditat, self).__init__(*args, **kwargs)
        self.__per_visitar = None
        self.__visitats = None
        self.__cami_exit = None

    def pinta(self, display):
        pass

    def cerca(self, estat_inicial: Estat) -> bool:
        self.__per_visitar = []
        self.__visitats = set()
        exit = False

        self.__per_visitar.append(estat_inicial)
        while self.__per_visitar:
            estat_actual = self.__per_visitar.pop(-1)

            if estat_actual in self.__visitats:
                continue

            if estat_actual.es_meta():
                break
            
            print("Estat actual:", estat_actual)
            for f in estat_actual.generar_fill():
                self.__per_visitar.append(f)
            
            self.__visitats.add(estat_actual)
        
        if estat_actual.es_meta():
            self.__cami_exit = estat_actual.cami
            exit = True

        return exit


    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__cami_exit is None:
            estat_inicial = Estat(
                parets = percepcio["PARETS"],
                desti = percepcio["DESTI"],
                # Para seleccionar la posicion del unico agente del diccionario
                posicio = next(iter(percepcio["AGENTS"].values()))
            )
            self.cerca(estat_inicial)
        
        # Si hay un camino de salida
        if self.__cami_exit:
            accio, direccio = self.__cami_exit.pop(-1)

            print("Accio:", accio, "Direccio:", direccio)
            return accio, direccio
        else:
            return Accions.ESPERAR
