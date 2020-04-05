# Music-Player

<p>Music Player é um reprodutor de musica leve e facil de usar! <br>Ele funciona totalmente pelo terminal com uma interface muito amigavel</p>

## Como Usar?

<p>Primeiro vamos instalar as dependências</p>

```bash
pip install npyscreen
pip install pydub
pip install pyaudio
pip install PyFiFinder
```

<p>Verifique se as bibliotecas do portaudio estão instaladas corretamente.</p>

<p>Lembre-se de alterar o caminho para a sua home no arquivo reprodutor.py</p>

```python
self.buscador = PyFinder('caminho/para/home', ['mp3', 'wav', 'wave'])
```

<b>Depois é só executar o arquivo main do projeto</b>

```bash
	python main.py
```

Author: Marcelo Almeida (M4rk)
Lincense: MIT

