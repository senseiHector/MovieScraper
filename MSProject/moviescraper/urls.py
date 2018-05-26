from django.urls import path

from . import views

#Variable holding all relative app urls and linking them to their corresponding view methods
urlpatterns = [
	path('', views.index, name='index'),
	path('details/<int:movie_id>', views.details, name='details'),
]