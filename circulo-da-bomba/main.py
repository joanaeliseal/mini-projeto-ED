from Jogo import Jogo, JogoException

while True:
    try:
        print('\nVamos jogar o círculo da bomba!')
        numeroDeParticipantes = int(input("\nDigite o número de participantes: "))
        numeroDeVencedores = int(input(f"Digite o número de vencedores: "))
    
        circulo = Jogo(numeroDeVencedores, numeroDeParticipantes)

        lerArquivo = input('\nDeseja ler os nomes dos participantes de um arquivo texto?: (S)im/(N)ão: ').upper()
        while lerArquivo not in 'SN':
            lerArquivo = input('\n>>>Opção inválida. Deseja ler os nomes dos participantes de um arquivo texto? (S)im/(N)ão: ').upper()
        if lerArquivo == 'S':
            arquivo = input("\nDigite o nome do arquivo (ou o caminho do arquivo se ele não estiver nesta pasta): ")
            circulo.lerArquivoDosParticipantes(arquivo, numeroDeParticipantes)
        else:
            circulo.receberParticipantes()
        
        circulo.iniciarJogo()

        if not circulo.jogarDeNovo():
            print("Obrigado por jogar!")
            break

    except JogoException as je:
        print(je)
    except ValueError as e:
        print(f">>>Erro: {e}. Por favor, insira valores válidos.")