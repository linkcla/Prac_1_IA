from practica import joc, agent_profunditat, config


def main():
    mida = config.mida
    agents = [
        agent_profunditat.ViatgerProfunditat("Agent 1", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
