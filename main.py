import npyscreen
from reprodutor import Reprodutor
import threading


class App(npyscreen.NPSAppManaged):
	'''
	Esta é a classe que vai gerenciar toda nossa aplicação
	'''

	def onStart(self):
		'''
		Esta função é chamada quando o app começa a rodar
		'''
		# Registra um formulario
		self.registerForm('MAIN', Screen1())


class Screen1(npyscreen.Form):
	'''
	Este é um formulario que sera a tela base do nosso app
	'''

	pausado = True

	def create(self):
		'''
		Esta função é chamada quando o formulario é criado
		ela servirar para construir todos os widgets filhos
		'''
		
		# Variavel que vai armazenar uma Thread
		self.t = False

		self.rep = Reprodutor()
		self.rep.buscar_musicas()
		self.rep.metodo_customizado = self.atualizar_progresso

		# Adiciona dois widgets para mensagens
		self.add_widget(npyscreen.TitleText, name='Mensagem: ', value='Boas vindas', editable=False)
		self.add_widget(npyscreen.TitleText, name='Sobre: ', value='Este é um simples reprodutor de musica feito em python', editable=False)
		
		# Guarda as musicas encontradas pelo reprodutor
		self.selecao = []

		for key, value in self.rep.buscador.data['archives'].items():
			
			for musica in value:

				self.selecao.append(musica)
		# Este é um widget que é tipo uma caixa em quê o usuario vai selecionar a musica desejada
		self.musica = self.add_widget(npyscreen.TitleMultiLine, name='Musicas: ', values=self.selecao, max_height=20)
		# Um botão usado para reproduzir a musica selecionada
		self.confirmar = self.add_widget(npyscreen.ButtonPress, name='Reproduzir', relx=50)
		# Armazena a função que vai ser chamada quando o usuario pressionar o botão
		self.confirmar.whenPressed = self.reproduzir
		# Botão para dar pause/play na musica
		self.pausa_play = self.add_widget(npyscreen.ButtonPress, name='Pausar', relx=70, rely=-16)
		# Faz um bind para a função pausar_reproduzir
		# Este botão pausa e continua a reprodução da musica atual
		self.pausa_play.whenPressed = self.pausar_reproduzir
		# Cria um widget do tipo slider
		self.progresso = self.add_widget(npyscreen.Slider, label=False, out_of=100, lowest=0, width=80, relx=30, rely=27)
		# Função para alterar o tempo da musica.
		self.progresso.when_value_edited = self.alterar_tempo

	def reproduzir(self, continuar=False):
		''''
		O parametro continuar diz se é para reproduzir a mesma musica do local onde parou
		'''

		# Troca o estado atual da musica
		if not continuar:

			self.pausado = False
		
		# Pega o valor que o usuario selecionou
		self.musica_selecionada = self.selecao[self.musica.value]
		# Passa o arquivo e o formato do arquivo para o reprodutor
		self.rep.selecionar_arquivo(arquivo=self.musica_selecionada, formato=self.musica_selecionada.split('.')[len(self.musica_selecionada.split('.')) - 1])
		# Diz pro reprodutor para a execução de qualquer musica no momento
		self.rep.reproduzindo = False
		
		# Verifica se ha alguma Thread ativa
		if self.t:
			# Espera o termino da Thread
			self.t.join()
		# Inicia uma nova Thread para reproduzir a musica
		self.t = threading.Thread(target=self.rep.reproduzir, args=(continuar,))
		self.t.start()

	def atualizar_progresso(self, progresso):
		'''
			Esta função atualiza o tempo da barra conforme a musica passa.
		'''

		self.progresso.value = progresso
		self.progresso.display()

	def alterar_tempo(self):

		try:
			# Pega o valor do widget slide que controla o tempo da musica e transforma ele em um valor compativel com o tempo da musica
			novo_progresso = (self.progresso.value / 100) * len(self.rep.arquivo)
			# Para a reprodução
			self.rep.reproduzindo = False
			# Espera a thread terminar
			self.t.join()
			# Salva o novo progresso
			self.rep.progresso = int(novo_progresso)
			# Muda o botão de pausa/play para play
			self.pausa_play.name = 'Play'
			# Atualiza o widget
			self.pausa_play.update()
			# Diz que o estado do reprodutor é pausado
			self.pausado = True

		except:

			pass

	def pausar_reproduzir(self):
		
		# Verifica se a musica esta pausada
		if self.pausado:
			
			# Chama a função para voltar a reproduzir
			self.reproduzir(True)
			# Altera o estado da musica
			self.pausado = False
			# Alterar o name do botao de pausa/play
			self.pausa_play.name = 'Pausar'
			# Atualiza o botão
			self.pausa_play.update()

		else:
			
			# Para a reprodução
			self.rep.reproduzindo = False
			# Espera a Thread terminar
			self.t.join()
			# Altera o estado da musica
			self.pausado = True
			# Altera o nome do botão pausa/play
			self.pausa_play.name = 'Play'
			# Atualiza o botão
			self.pausa_play.update()

	def afterEditing(self):
		
		# Usado para fecha o reprodutor quando fecha o App
		self.rep.reproduzindo = False
		self.parentApp.setNextForm(None)


if __name__ == '__main__':

	app = App()
	app.run()

