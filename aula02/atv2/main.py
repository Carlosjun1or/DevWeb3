alunos = []
disciplinas = set()
opcao = 0

print("Sistema de Cadastro de Alunos")

while opcao != 8:
    print("1 - Cadastrar Aluno")
    print("2 - Listar Alunos")
    print("3 - Registrar Notas")
    print("4 - Calcular a Média")
    print("5 - Cadastrar Disciplinas")
    print("6 - Listar Disciplinas")
    print("7 - Informar dados da turma")
    print("8 - Sair")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        nome = input("Digite o nome do aluno: ")
        idade = input("Digite a idade do aluno: ")
        altura = input("Digite a altura do aluno: ")

        aluno = {
            "nome": nome,
            "idade": idade,
            "altura": altura
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
                print("Altura:", aluno["altura"])
                print("--------------------")

    elif opcao == 3:
        nome = input("Digite o nome do aluno para registrar as notas: ")

        for aluno in alunos:
            if aluno["nome"] == nome:
                nota1 = float(input("Digite a primeira nota: "))
                nota2 = float(input("Digite a segunda nota: "))
                aluno["notas"] = [nota1, nota2]
                print("Notas registradas com sucesso!\n")
                break
        else:
            print("Aluno não encontrado.\n")

    elif opcao == 4:
        nome = input("Digite o nome do aluno para calcular a média: ")

        for aluno in alunos:
            if aluno["nome"] == nome:
                if "notas" in aluno:
                    media = sum(aluno["notas"]) / len(aluno["notas"])
                    print("Média do aluno", nome, ":", media)
                else:
                    print("Notas não registradas para este aluno.")
                break
        else:
            print("Aluno não encontrado.\n")

    elif opcao == 5:
        disciplina = input("Digite o nome da disciplina: ")
        disciplinas.add(disciplina)
        print("Disciplina cadastrada com sucesso!\n")

    elif opcao == 6:
        if len(disciplinas) > 0:
            print("Lista de Disciplinas:")
            for disciplina in disciplinas:
                print(disciplina)
        else:
            print("Nenhuma disciplina cadastrada.\n")

    elif opcao == 7:
        print("Informações da Turma:")
        print("Quantidade de Alunos:", len(alunos))

        if len(disciplinas) > 0:
            print("Disciplinas Cadastradas:")
            for disciplina in disciplinas:
                print(disciplina)
        else:
            print("Nenhuma disciplina cadastrada.")

    elif opcao == 8:
        print("Saindo do sistema...")

    else:
        print("Opção inválida. Tente novamente.\n")