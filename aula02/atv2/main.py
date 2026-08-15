alunos = [] 
disciplinas = set() 
turma = ("DSM3", 2026)

opcao = 0

while opcao != 8:
    
    print("Sistema de Cadastro de Alunos")
    print("1 - Cadastrar Aluno\n2 - Listar Alunos\n3 - Registrar Notas\n4 - Calcular a Média\n5 - Cadastrar Disciplinas\n6 - Listar Disciplinas\n7 - Informar dados da turma\n8 - Sair")


    opcao = int(input("Escolha uma opção: "))
    print("")
     
    if opcao == 1:
        nome = input("Digite o nome do aluno: ")

        if any(aluno["nome"].lower() == nome.lower() for aluno in alunos):
            print("Já existe um aluno cadastrado com esse nome!\n")
        else:
            idade = input("Digite a idade do aluno: ")
            cidade = input("Digite a cidade do aluno: ")

        aluno = {
            "nome": nome,
            "idade": idade,
            "cidade": cidade,
            "notas": []
        }

        alunos.append(aluno)
        print("Aluno cadastrado com sucesso!\n")

    elif opcao == 2:
        if len(alunos) == 0:
            print("Nenhum aluno cadastrado.\n")
        else:
            print("Lista de Alunos:")
            for aluno in alunos:
                print("Nome:", aluno["nome"])
                print("Idade:", aluno["idade"])
                print("Cidade:", aluno["cidade"])

                if len(aluno["notas"]) > 0:
                    print("Notas:", aluno["notas"],"\n")
                else:
                    print("Notas: Nenhuma registrada\n")

    elif opcao == 3:
        nome = input("Digite o nome do aluno: ")

        for aluno in alunos:
            if aluno["nome"].lower() == nome.lower():

                quantidade = int(input("Quantas notas deseja cadastrar? "))

                aluno["notas"] = []

                for i in range(quantidade):
                    nota = float(input(f"Digite a nota {i+1}: "))
                    aluno["notas"].append(nota)

                print("Notas registradas com sucesso!\n")
                break
        else:
            print("Aluno não encontrado.\n")

    elif opcao == 4:
        nome = input("Digite o nome do aluno: ")

        for aluno in alunos:
            if aluno["nome"].lower() == nome.lower():

                if len(aluno["notas"]) > 0:
                    media = sum(aluno["notas"]) / len(aluno["notas"])

                    print(f"Média de {aluno['nome']}: {media:.2f}")

                    if media >= 6:
                        print("Situação: Aprovado\n")
                    else:
                        print("Situação: Reprovado\n")

                else:
                    print("Este aluno não possui notas cadastradas.\n")

                break
        else:
            print("Aluno não encontrado.\n")

    elif opcao == 5:
        disciplina = input("Digite o nome da disciplina: ")

        if disciplina in disciplinas:
                print("Essa disciplina já está cadastrada!\n")
        else:
            disciplinas.add(disciplina)
            print("Disciplina cadastrada com sucesso!\n")

    elif opcao == 6:
        if len(disciplinas) > 0:
            print("\nDisciplinas cadastradas:")
            for disciplina in disciplinas:
                print("-", disciplina)
            print("")
        else:
            print("Nenhuma disciplina cadastrada.\n")

    elif opcao == 7:
        print("Dados da Turma")
        print("Curso:", turma[0])
        print("Ano:", turma[1])
        print("Quantidade de alunos:", len(alunos))

        if len(disciplinas) > 0:
            print("Disciplinas:")
            for disciplina in disciplinas:
                print(" - ", disciplina)
            print()
        else:
            print("Nenhuma disciplina cadastrada.\n")

    elif opcao == 8:
        print("Encerrando o programa...")

    else:
        print("Opção inválida. Tente novamente.\n")