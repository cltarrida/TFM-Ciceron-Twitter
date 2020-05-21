import warnings
warnings.filterwarnings("ignore")

from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import matplotlib.pyplot as plt
import re

def word_cloud_analyzer(cloud_tweets, search):
	# En la nube de palabras están incluidas las MENCIONES y los HASHTAGS
	stop_word_sp = nltk.corpus.stopwords.words("spanish")
	stop_word_en = nltk.corpus.stopwords.words("english")

	# Detectamos palabras de la búsqueda para incluirlas en la lista de palabras prohibidas
	# Eliminamos posibles conectores de la búsqueda
	search = re.sub('OR[\s]', '', search)
	search = re.sub('AND[\s]', '', search)
	# Normalizamos a minúsculas
	search = search.lower()
	# Convertimos en lista de palabras
	search = search.split()

	# Por ahora trabajamos en conjunto (podrá elegirse el idioma de salida en un menú)
	# string.punctuation: incluye los signos de puntuación en el listado de palabras prohibidas
	# string.digits: incluye los números en klas palabras prohibidas
	# string.ascii_uppercase: incluye letras mayúsculas sueltas
	# string.ascii_lowercase: incluye letras minúsculas sueltas
	stop_word = stop_word_sp + stop_word_en
	# Incluimos en la lista de palabras prohibidas aquellas que hemos utilizado en la búsqueda
	stop_word += search
	# Incluimos sognos y otros elementos

	stop_word += list(string.punctuation) + list(string.digits) + list(string.ascii_lowercase) + list(string.ascii_uppercase) 
	stop_word += ['--', "''", "``", "..", "...", "'s", '…', '’', "'", "`", '“', '”', '«', '»', "n't", '//', '।', '—']

	# Convertimos a cadena y ponemos todo en minúscula (en mayúscula: upper). La normalización es necesaria para calcular correctamente la frecuencia de las palabras
	cloud_text = cloud_tweets.str.cat(sep = '').lower()


	# Generamos gráfico de frecuencia de aparición de palabras
	# Dividimos el texto en tokens (unidad mínima entre espacios)
	tokens = word_tokenize(cloud_text)
	word_cloud = [i for i in tokens if not i in stop_word]

	# Calvulamos la frecuencia de aparición de las palabras
	word_frequency = nltk.FreqDist(word_cloud)
	# Nos quedamos con las 25 más frecuentes
	most_common = word_frequency.most_common(25)

	# Representamos
	plt.barh(range(len(most_common)), [val[1] for val in most_common], align = 'center')
	plt.yticks(range(len(most_common)), [val[0] for val in most_common])
	# Salvamos la gráfica en un fichero
	plt.savefig('wordfrequency.png')
	plt.show()


	# Convertimos a cadena la lista de palabras tokenizada para poder representarlo en la nube de palabras y eliminar el apóstrofe final de palabra
	word_cloud = ' '.join(word_cloud)

	# Creamos un objeto WordCloud: font_path, max_words = 200, mask, stopwords = stop_word
	wc = WordCloud(width = 500, height = 300, random_state = 21, max_font_size = 110, background_color = "white")
	wc.generate(word_cloud)

	# Salvamos en png
	wc.to_file('wordcloud.png')
	# Representamos en pantalla
	plt.imshow(wc, interpolation = 'bilinear')
	plt.axis("off")
	plt.show()
