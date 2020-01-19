import npyscreen
from reprodutor import Reprodutor
import threading

# Cria um objeto do tipo Reprodutor
rep = Reprodutor()
rep.buscar_musicas()

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

	def create(self):
		'''
		Esta função é chamada quando o formulario é criado
		ela servirar para construir todos os widgets filhos
		'''

		global rep
		
		# Variavel que vai armazenar uma Thread
		self.t = False

		# Adiciona dois widgets para mensagens
		self.add_widget(npyscreen.TitleText, name='Mensagem: ', value='Boas vindas', editable=False)
		self.add_widget(npyscreen.TitleText, name='Sobre: ', value='Este é um simples reprodutor de musica feito em python', editable=False)
		
		# Guarda as musicas encontradas pelo reprodutor
		self.selecao = []

		for key, value in rep.buscador.data['archives'].items():
			
			for musica in value:

				self.selecao.append(musica)
		# Este é um widget que é tipo uma caixa em quê o usuario vai selecionar a musica desejada
		self.musica = self.add_widget(npyscreen.TitleMultiLine, name='Musicas: ', values=self.selecao, max_height=20)
		# Um botão usado para reproduzir a musica selecionada
		self.confirmar = self.add_widget(npyscreen.ButtonPress, name='Reproduzir')
		# Armazena a função que vai ser chamada quando o usuario pressionar o botão
		self.confirmar.whenPressed = self.reproduzir

	def reproduzir(self):
		
		global rep
		
		# Pega o valor que o usuario selecionou
		self.musica_selecionada = self.selecao[self.musica.value]
		# Passa o arquivo e o formato do arquivo para o reprodutor
		rep.selecionar_arquivo(arquivo=self.musica_selecionada, formato=self.musica_selecionada.split('.')[len(self.musica_selecionada.split('.')) - 1])
		# Diz pro reprodutor para a execução de qualquer musica no momento
		rep.reproduzindo = False
		
		# Verifica se ha alguma Thread ativa
		if self.t:
			# Espera o termino da Thread
			self.t.join()
		# Inicia uma nova Thread para reproduzir a musica
		self.t = threading.Thread(target=rep.reproduzir)
		self.t.start()


	def afterEditing(self):
		
		global rep
		
		# Usado para fecha o reprodutor quando fecha o App
		rep.reproduzir = False
		self.parentApp.setNextForm(None)


if __name__ == '__main__':

	app = App()
	app.run()

