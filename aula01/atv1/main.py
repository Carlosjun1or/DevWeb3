from random import randint

# Cores
VERMELHO = "\033[31m"
VERDE = "\033[32m"
AMARELO = "\033[33m"
AZUL = "\033[34m"
CIANO = "\033[36m"
RESET = "\033[0m"

opcoes = ["Pedra", "Papel", "Tesoura"]
contador_vitorias_jogador = 0
contador_vitorias_pc = 0
print(f"\n{CIANO}Vamos jogar {VERMELHO}Jo{AMARELO}ken{VERDE}pô!{CIANO} O primeiro a vencer {VERDE}3 rodadas{RESET}{CIANO} ganha o jogo!{RESET}")

while contador_vitorias_jogador < 3 and contador_vitorias_pc < 3:
    pc = randint(0,2) #gera um número aleatório entre 0 e 2
    jogador = int(input("Escolha:\n0- Pedra, 1- Papel, 2- Tesoura:"))
    if jogador < 0 or jogador > 2:
        print(f"{VERMELHO}Escolheu o número errado! Tente novamente.{RESET}\n")
        continue        
    print(f"\nJogador: {VERDE}{opcoes[jogador]}{RESET} X {VERMELHO}{opcoes[pc]}{RESET} :Computador\n")

    
    if jogador == pc:
        print(f"{AMARELO}Empate!{RESET}")
    elif (jogador == 0 and pc == 2) or (jogador == 1 and pc == 0) or (jogador == 2 and pc == 1):
        print(f"{VERDE}Jogador venceu essa rodada!{RESET}")
        contador_vitorias_jogador += 1
    else:
        print(f"{VERMELHO}Computador venceu essa rodada!{RESET}")
        contador_vitorias_pc += 1

    if contador_vitorias_jogador == 3:
        print(f"\n{CIANO}Fim do jogo!{RESET}")
        print(f"{VERDE}JOGADOR VENCEU O JOGO{RESET}, com {VERDE}{contador_vitorias_jogador}{RESET} X {VERMELHO}{contador_vitorias_pc}{RESET} do Computador!")
        break
    elif contador_vitorias_pc == 3:
        print(f"\n{CIANO}Fim do jogo!{RESET}")
        print(f"{VERMELHO}COMPUTADOR VENCEU O JOGO{RESET}, com {VERMELHO}{contador_vitorias_pc}{RESET} X {VERDE}{contador_vitorias_jogador}{RESET} do Jogador!")
        break
    else:
        print(f"\n{CIANO}O jogo continua! \nPlacar:{RESET} Jogador: {VERDE}{contador_vitorias_jogador}{RESET} - Computador: {VERMELHO}{contador_vitorias_pc}{RESET}\n")