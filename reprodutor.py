from pydub import AudioSegment
from pydub.playback import play
from PyFiFinder import PyFinder
from threading import Thread
import sched
import time
import pyaudio


class Reprodutor():
	'''
	Este é um reprodutor de musica simples feito em python.
	'''

	def __init__(self):
		
		# Cria um objeto do tipo PyAudio que vai servir para reproduzir as musicas.
		self.p = pyaudio.PyAudio()
		# Guarda o momento em quê a musica esta.
		self.reproducao_atual = 0
		# Cria um objeto pyfinder para procurar por musicas no diretorio do usuario
		self.buscador = PyFinder('/home/user/', ['mp3', 'wav', 'wave'])
		# Diz se o fluxo do pyaudio esta ativo ou não
		self.fluxo = False

	def selecionar_arquivo(self, arquivo, formato):
		# Cria um seguimento de audio
		self.arquivo = AudioSegment.from_file(arquivo, format=formato)

	def reproduzir(self, continuar_reproducao=False):
		
		# Diz se tem alguma musica reproduzindo agora
		self.reproduzindo = True
		
		# Diz se o usuario quer continua a reprodução de onde a outra parou
		if not continuar_reproducao:

			self.reproducao_atual = 0
		
		# verifica se ja tem um objeto do tipo fluxo criado
		if self.fluxo:
			# Para o fluxo
			self.fluxo.stop_stream()
			# Fecha o fluxo atual
			self.fluxo.close()

		# Cria um novo fluxo
		self.fluxo = self.p.open(
			format=self.p.get_format_from_width(self.arquivo.sample_width), # Pega o formato do arquivo pelo seu tamanho
			channels=self.arquivo.channels, # Pega os canais disponiveis
			rate=self.arquivo.frame_rate, # Frame rate
			output=True,
		)

		try:
			
			# Cada 1000 pedaços de um AudioSegment é igual a 1s, então dividimos cada pedaços em 5s para ficar agradavel
			for frame in self.arquivo[self.reproducao_atual::5000]:
				# Verifica se é para continuar reproduzindo
				if self.reproduzindo:
					# Começa a reproduzir
					self.fluxo.write(frame.raw_data)
					# Guarda a quantidade que ja foi reproduzido
					self.reproducao_atual += 5000

				else:

					break
			# Para o fluxo
			self.fluxo.stop_stream()
			# Fecha o fluxo
			self.fluxo.close()

		except KeyboardInterrupt:

			self.fluxo.stop_stream()
			self.fluxo.close()
			self.p.terminate()
	
	def buscar_musicas(self):
		
		# Inicia a busca por musicas
		self.buscador.start()

	def fechar(self):
		'''
		Esta função encerra o reprodutor.
		'''

		if self.fluxo:

			if self.fluxo.is_active():
				
				self.reproduzindo = False

		self.p.terminate()

