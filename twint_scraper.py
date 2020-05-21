import twint


def twint_scraper():
	try:
		c = twint.Config()
		# Para descargar tweets según términos de búsqueda
		search = c.Search = "cambio AND climático"
		# Para permitir el almacenamiento en fichero .csv
		c.Store_csv = True
		# Establecer el nombre del fichero de salida
		c.Output = "tweets_csv.csv"
		# Número de tweets máximos a almacenar
		c.Limit = 150

		twint.run.Search(c)
		
		return search

	except Exception as e:
		print(e)