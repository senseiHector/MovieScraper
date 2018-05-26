from django.db import models

# Create your models here.
class Movie(models.Model):
	"""Movie class to represent the movie model which holds the title of the movie,
	length of the movie as well as showing times
	"""
	movie_id = models.CharField(max_length=10)
	movie_name = models.CharField(max_length=100)
	movie_length = models.CharField(max_length=100)
	movie_times = models.CharField(max_length=100)

	@classmethod
	def create(cls,movie_id, movie_name, movie_length, movie_times):
		"""Instantiates the Movie model and assigns the the parameters to the various instance variables of the model

		Keyword arguments:
		cls -- reference to the instatiating model. Django models' version of the self keyword
		movie_id -- The unique id used to identify each movie
		movie_name -- The name of the movie
		movie_length -- The total length of the movie
		movie_times -- The times(Days of the week and particular start times) which the movie will be showing at the cinema
		"""
		movie = cls(
			movie_id = movie_id,
			movie_name = movie_name, 
			movie_length = movie_length, 
			movie_times = movie_times
			)
		return movie
