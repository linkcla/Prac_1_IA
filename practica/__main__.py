from practica import joc, config
from practica.profundidad import agent_profunditat
from practica.minimax import agent_minimax
from practica.estrella import agent_estrella


def main_profunditat():
    mida = config.mida
    agents = [
        agent_profunditat.ViatgerProfunditat("Agent 1", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()

def main_estrella():
    mida = config.mida
    agents = [
        agent_estrella.ViatgerA("Agent 1", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()

def main_minimax():
    mida = config.mida
    agents = [
        agent_minimax.ViatgerMinimax("MAX", mida_taulell=mida),
        agent_minimax.ViatgerMinimax("MIN", mida_taulell=mida)]

    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()

if __name__ == "__main__":
    main_minimax()
