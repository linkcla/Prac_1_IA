from practica import joc, agent_profunditat


def main():
    mida = (12, 12)

    agents = [
        agent_profunditat.ViatgerProfunditat("Agent 1", mida_taulell=mida)
    ]   

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
