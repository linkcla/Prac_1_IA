from practica import joc, agent_profunditat, agent_estrella, agent_minimax, config

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
        agent_minimax.ViatgerMinimax("Agent 1", mida_taulell=mida),
        agent_minimax.ViatgerMinimax("Agent 2", mida_taulell=mida)]

    lab = joc.Laberint(agents, mida_taulell=mida)
    lab.comencar()

if __name__ == "__main__":
    main_minimax()
