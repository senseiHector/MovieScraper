from django.shortcuts import render
from . import models

import requests
from contextlib import closing
from bs4 import BeautifulSoup

movies = list() #Global variable for holding list of movie objects


def get_movies():
	"""Populates the list of movies and their details scraped from the silverbird Ghana page.
	This function catches a Request Exception that may occur when connecting to the silverbird url
	"""
	global movies #edit the global variable movies
	movies = list() #reinstantiate the global variable movies in case the page must be reloaded 
	page = None #Variable to hold the html script retreived from the url
	count = 1 #Variable to keep count of movies in the list
	url = "https://silverbirdcinemas.com/cinema/accra/"

	try:
		with closing(requests.get(url, stream=True)) as response: #Get request for the data linked to url
			content_type = response.headers['Content-Type'].lower()
			if (response.status_code == 200 
			and content_type is not None 
			and content_type.find('html') > -1): #If request is succesful store content in page variable
				page = response.content

	except requests.RequestException as e: #Handle exception created by unsuccesful get request
			print('Error during requests to {0} : {1}'.format(url, str(e)))

	if page is not None:
			html = BeautifulSoup(page, 'html.parser') #Format the html script for beautiful soup module
			entrys = html.find_all('div',class_ ='entry-content') #Find all divs of type entry-content
			entrys.pop(0) #Remove the first div of type entry because it does not contain movie details

			for movie in entrys: #Loop through entries and store movie details in movies list
				movies.append(models.Movie.create(
					count,
					movie.contents[0].text,
					movie.contents[1].text,
					movie.contents[2].text))
				count += 1


def index(request):
	"""Returns an HTTPResponse with the name of the template being rendered, 
	the request that called it and the context being passed to the template

	Keyword arguments:
	request -- the http request that called the function
	"""
	get_movies()
	context = {'movies': movies}
	return render(request, 'index.html', context)


def details(request, movie_id):
	"""Returns an HTTPResponse with the name of the template being rendered, 
	the request that called it and the context being passed to the template

	Keyword arguments:
	request -- the http request that called the function
	movie_id -- the id of the movie whose details are to be displayed
	"""
	this_movie = None
	for movie in movies: #Loop through movies to find the one specified by the movie id parameter
		if movie.movie_id == movie_id:
			this_movie = {
			'movie_name': movie.movie_name,
			'movie_length': movie.movie_length,
			'movie_times': movie.movie_times
			}

	context = {'this_movie': this_movie}
	return render(request, 'details.html', context)