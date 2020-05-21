import twint_scraper
import sentiment_analyzer
import wordcloud_analyzer
import images_analyzer

if __name__ == '__main__':

	search = twint_scraper.twint_scraper()

	images_analyzer.images_analyzer()

	tweets_df = sentiment_analyzer.textblob_sentiment_analyzer()

	# Realizamos la nube de palabras sobre los tweets limpios pero no traducidos: tweet_clean (opción de menú de idioma-inglés: translation)
	# El parámetro search es para eliminar las palabras utilizadas en la búsqueda
	wordcloud_analyzer.word_cloud_analyzer(tweets_df['tweet_cloud'], search)