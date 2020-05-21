import emoji
from textblob import TextBlob
from googletrans import Translator
import pandas as pd
import re
import os

SMILEYS = {":-)": "smiley", ";-)": "smiley", ":)": "smiley", ":D": "smiley", ":o)": "smiley", ":]": "smiley", ":3": "smiley", ":c)": "smiley", ":>": "smiley", "=]": "smiley", "8)": "smiley",
">:[": "sad", ":-(": "sad", ":(": "sad", ":-c": "sad", ":c": "sad", ":-<": "sad", ":っC": "sad", ":<": "sad", ":-[": "sad", ":[": "sad", ":{": "sad",
">:\\": "neutral", "\>:\/": "neutral", ":-/": "neutral",  ":-.": "neutral", ":/": "neutral", ":\\": "neutral", "=/": "neutral", "=\\": "neutral", ":L": "neutral", "=L": "neutral", ":S": "neutral", ">.<": "neutral"}

# (tweets_df)
def textblob_sentiment_analyzer():
	try:
		# Unimos las columnas de fehca y hora para tenerlo disponible para kibana
		tweets_df = pd.read_csv("tweets_csv.csv")

		# Eliminamos el fichero csv de memoria después de utilizarlo
		os.remove("tweets_csv.csv")
		
		# Fusionamos los campos dedicados a la fecha y la hora
		tweets_df['date_time'] = pd.to_datetime(tweets_df['date'] + ' ' + tweets_df['time'])

		# Limpieza para evitar errores de parseo
		tweets_df['tweet'] = tweets_df['tweet'].apply(avoid_parse_error)
		# Sustituimos emojis por palabras
		# Demoji: es necesario sustuir los emoticonos por palabras antes de traducir
		tweets_df['tweet_clean'] = tweets_df['tweet'].apply(lambda tweets_df: emoji.demojize(str(tweets_df)))
		# Sustituimos emoticonos por palabras
		tweets_df['tweet_clean'] = tweets_df['tweet_clean'].apply(convert_emoticons)
		# Limpiamos los caracteres sobrantes para la nube de palabras
		tweets_df['tweet_cloud'] = tweets_df['tweet_clean'].apply(clean_tweets, flag_cloud = True)
		# Limpiamos los caracteres sobrantes antes de traducir
		tweets_df['tweet_clean'] = tweets_df['tweet_cloud'].apply(clean_tweets, flag_cloud = False)
		
		# Bloque para traducir
		translator = Translator()
		# Traducimos los tweets con detección automática del idioma de entrada a inglés
		tweets_df['translation'] = tweets_df['tweet_clean'].apply(lambda tweets_df: translator.translate(tweets_df, dest = 'en').text)

		# Análisis de sentimiento con traducción. Trabajamos por cada fila de la columna del objeto pandas (lambda). Sin traducción, cambiar 'translation' por 'tweet'
		tweets_df['polarity'] = tweets_df['translation'].apply(lambda tweets_df: TextBlob(tweets_df).sentiment.polarity)
		tweets_df['subjectivity'] = tweets_df['translation'].apply(lambda tweets_df: TextBlob(tweets_df).sentiment.subjectivity)
		# Computamos la polaridad del sentimiento
		tweets_df['analysis'] = tweets_df['polarity'].apply(compute_sentiment_polarity)
			
		# Sobreescribe el archivo csv existente - en caso contrario, utilizar 'a' (append)
		# Se ha modificado el delimitador para que pueda utilizarse el ; en el texto del tweet
		tweets_df.to_csv('tweets_df.csv', mode = 'w', sep ="|", header = True, index = False)

		return tweets_df
			
	except Exception as e:
		print("Se ha producido un error en el análisis del sentimiento:")
		print(e)


def avoid_parse_error(tweet):
	# Limpiamos todos los \n y todas las comillas y el separador |
	tweet= re.sub('[\|]', '', tweet)
	tweet = re.sub('[\n\t\r]', ' ', tweet)
	tweet = re.sub('[\"-]', '', tweet)
	return tweet

# Función para limpiar los tweets de caracteres usuales de Twitter
def clean_tweets(tweet, flag_cloud):
	if(flag_cloud == True):
		# Limpiar los RT (creo que sólo el símbolo), \s: un espacio
		tweet = re.sub('RT[\s]', '', tweet)
		# Limpiar los hipervínculos completos, \S: cualquier cosa menos un espacio
		tweet = re.sub('https?:\/\/\S+', '', tweet)
		# Limpiar las referencias a imágenes completas, +: uno o más caracteres
		tweet = re.sub('pic.twitter.com\S+', '', tweet)
		# Limpiamos todos los \n y todas las comillas (repetimos el proceso por si se han introducido nuevos caracteres de escape)
		# Eliminamos el carácter que empleamos como separador del csv: |, para que no haya errores de parseo
		tweet= re.sub('[\|]', '', tweet)
		tweet = re.sub('[\n\t\r]', ' ', tweet)
		tweet = re.sub('[\"-]', '', tweet)
	else:
		# No necesitamos menciones ni hashtags para el análisis de sentimiento
		#Limpiar las menciones completas, +: uno o más caracteres (no las quitamos para la nube de palabras, nos interesa)
		tweet = re.sub('@[A-Za-z0-9]+', '', tweet)
		# Limpiar los hashtags completos (no los quitamos para la nube de palabras, nos interesa)
		tweet = re.sub('#[A-Za-z0-9]+', '', tweet)

	return tweet

def convert_emoticons(tweet):
	words = tweet.split()
	reformed = [SMILEYS[word] if word in SMILEYS else word for word in words]
	tweet = " ".join(reformed)
	return tweet

# Función para computar la polaridad del sentimiento
def compute_sentiment_polarity(polarity):
	# Una vez que se implemente el menú, el retorno será en español o en inglés
	if polarity < 0:
		return 'Negativo'
	elif polarity == 0:
		return 'Neutral'
	else:
		return 'Positivo'