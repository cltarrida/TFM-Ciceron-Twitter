import re
import wget
import pandas as pd
import os

try:
	from PIL import Image
except:
	import Image
import pytesseract

def images_analyzer():
	try:
		tweets_df = pd.read_csv("tweets_csv.csv")

		# Modificamos el formato del campo de fecha
		tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'], unit = 'ms')
		# Extraemos las imágenes y el texto en ellas de cada tweet
		tweets_df['photos_text'] = tweets_df['photos'].apply(extract_images)

		# Volcamos sólo aquellos datos que nos interesan
		header = ["id", "created_at", "username", "tweet", "photos", "photos_text"]
		tweets_df.to_csv('tweets_images.csv', mode = 'w', header = True, index = False, columns = header)

	except Exception as e:
		print(e)


def extract_images(images):
	try:
		# Si no se consigue extraer ningún dato se devolverá una cadena que indica que había una imagen
		image_text_cleaned = " "
		image_text = " "
		# Eliminamos los caracteres inncesarios que actúan como separadores de las URLs
		images = re.sub(r'[\[\]\'\,]', '', images)
		# Extraemos las direcciones URLs y las almacenamos en una lista
		images_list = re.findall('https?:\/\/\S+', images)

		# Sólo entramos en la descarga de imágenes si hay algo que descargar
		if images_list:
			# Creamos un directorio para almacenar las imágenes (sólo en el caso de que no exista)
			directory = os.getcwd() + '/Images/'
			try:
				os.stat(directory)
			except:
				os.mkdir(directory)

			# Descargamos las imágenes de cada una de las direcciones URLs extraídas
			for image in images_list:
				# Eliminamos el espacio que se introduce al final para poder descargar correctamente las imágenes
				image = re.sub('[\s]', '', image)
				print(image)

				# Extraemos el texto de la imagen
				image_text += pytesseract.image_to_string(Image.open(wget.download(image, out = directory)))

				image_text_cleaned = clean_image_text(image_text)
				print(image_text_cleaned)

		else:
			print("No hay imágenes para descargar.")

		return image_text_cleaned
	except Exception as e:
		print("Se ha producido un error en el análisis de las imágenes:")
		print(e)

def clean_image_text(text_to_clean):
	# Eliminamos el carácter que empleamos como separador del csv: |, para que no haya errores de parseo
	text_cleaned = re.sub('[\|]', '', text_to_clean)
	# Limpiamos todos los \n y todas las comillas, también para evitar errores de parseo
	text_cleaned = re.sub('[\n\t\r]', ' ', text_cleaned)
	text_cleaned = re.sub('[\"-]', '', text_cleaned)

	return text_cleaned