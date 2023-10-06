from random import randint
from PilhaSequencial import *
from ListaEncadeadaCircular import *

class JogoException(Exception):
    """Classe de exceção lançada quando uma violação no acesso aos elementos
       do jogo, indicado pelo usuário, é identificada.
    """
    def __init__(self,msg):
        """ Construtor padrão da classe, que recebe uma mensagem que se deseja
            embutir na exceção.
        """
        super().__init__(msg)

class Jogo:
    def __init__(self, numeroVencedores:int, numeroParticipantesIniciais:int) -> None:
        """ Inicialização da classe Jogo.
        """
        try:
            assert numeroVencedores > 0, ">>>Número de vencedores deve ser maior que zero."
            assert 1 <= numeroVencedores < numeroParticipantesIniciais, ">>>Número de vencedores deve ser menor que o número de participantes iniciais."

            self.__numeroVencedores = numeroVencedores
            self.__numeroParticipantesIniciais = numeroParticipantesIniciais
            self.__participantes = Lista()
            self.__removidos = Pilha()
            self.rodada = 1
        except AssertionError as ae:
            raise JogoException(ae)
            
    def receberParticipantes(self) -> None:
        """ Permite ao usuário inserir nomes de participantes.
        """
        participantesSet = set()  # Conjunto para rastrear nomes dos participantes

        for i in range(1, self.__numeroParticipantesIniciais + 1):
            while True:
                participante = input(f"Participante {i}: ")

                # Verifica se o participante já foi inserido
                if participante in participantesSet:
                    print(">>>Erro: Este participante já foi inserido. Por favor, escolha outro nome.")
                else:
                    # Insere o participante no conjunto e na lista
                    participantesSet.add(participante)
                    self.__participantes.inserir(i, participante)
                    break

    def lerArquivoDosParticipantes(self, nomeArquivo:str, numeroDeParticipantes:int) -> None:
        """ Método para ler nomes de participantes de um arquivo de texto 'txt'.
        """
        try:
            with open(nomeArquivo, 'r') as arquivo:
                participantes = arquivo.readlines()

            # Limpa os espaços em branco e caracteres de nova linha dos nomes lidos e divide usando vírgula
            participantes = [participante.strip().split(',') for participante in participantes]

            # Flatten a lista de listas resultante e mantenha a ordem usando uma lista
            participantesLista = [nome.strip() for sublist in participantes for nome in sublist]

            # Verifica duplicatas usando um conjunto
            participantesSet = set(participantesLista)

            # Se o número de itens no conjunto for diferente do número de itens na lista, há duplicatas
            if len(participantesSet) != len(participantesLista):
                raise JogoException(">>>Nomes duplicados encontrados no arquivo. Por favor, remova as duplicatas.")

            # Verifica se há nomes suficientes no arquivo para a quantidade de participantes especificada pelo usuário
            if len(participantesLista) < numeroDeParticipantes:
                raise JogoException(">>>Não há nomes suficientes no arquivo para a quantidade de participantes especificada.")

            # Insere apenas a quantidade de participantes especificada pelo usuário
            quantidadeParticipantesLimitada = numeroDeParticipantes

            # Insere os participantes na lista mantendo a ordem
            for i in range(quantidadeParticipantesLimitada):
                self.__participantes.inserir(i + 1, participantesLista[i])

            print("Participantes carregados do arquivo com sucesso.")

        except FileNotFoundError:
            raise JogoException(f">>>Arquivo '{nomeArquivo}' não encontrado.")
        except JogoException as je:
            print(f">>>Erro ao ler o arquivo: {je}")
        except AssertionError as ae:
            print(JogoException(ae))
        except Exception as e:
            print(f">>>Ocorreu algo inesperado: {e}")
        
    def sortearParticipanteInicial(self) -> int:
        """ Método que sorteia um participante para começar o jogo.
        """
        return randint(1, len(self.__participantes))

    def jogoContinua(self) -> bool:
        """ Método que verifica se o jogo continua com base no número de vencedores e participantes.
        """
        return len(self.__participantes) > self.__numeroVencedores

    def sortearSaltos(self) -> int:
        """ Este método sorteia a quantidade de saltos para cada rodada.
        """
        self.saltos = randint(4,15)
        return self.saltos

    def jogarDeNovo(self) -> bool:
        """ Este método permite ao usuário decidir se deseja jogar novamente.
        """
        while True:
            try:
                jogarNovamente = input("\nDeseja rodar novamente o programa? (S)im/(N)ão: ").upper()
                if jogarNovamente == 'S':
                    return True
                elif jogarNovamente == 'N':
                    return False
                else:
                    raise JogoException(">>>Entrada inválida. Por favor, insira 'S' para Sim ou 'N' para Não.")
            except JogoException as je:
                print(je)

    def iniciarJogo(self) -> None:
        """ Este método inicia o jogo e itera pelas rodadas até que o número de vencedores seja alcançado.
        """
        while self.jogoContinua():
            if self.rodada == 1:
                posicaoInicial = self.sortearParticipanteInicial()
                self.__participantes.preparaPercurso(posicaoInicial)              
            
            self.saltos = self.sortearSaltos()
            cont = 0
            print("\nParticipantes:", self.__participantes)
            print("Rodada:", self.rodada)
            print("Saltos:", self.saltos)
            while(self.__participantes.temProximo()):
                carga = self.__participantes.pedirProximo()
                if self.rodada == 1 and cont == 0:
                    print("Pointer:", carga)
                    self.saltos += 1
                cont += 1
                if (cont == self.saltos):
                    break    
            if self.rodada != 1:
                print("Pointer:", inicializador)  
            print("Removido:", carga)          
            posicao = self.__participantes.busca(carga)
            self.__removidos.empilha(carga)
            self.__participantes.remover(posicao)
            inicializador = self.__participantes.pedirProximo()
            self.rodada += 1

        print(f"\nVencedor(es) após {self.rodada-1} rodadas: ", self.__participantes)
        print("Percurso para a vitória:")
        s = ''
        for i in range(len(self.__removidos)):
            s += str(self.__removidos.desempilha()) + ' < '
        s = s.rstrip(' <' ) # remove o último ' <'
        print(s)