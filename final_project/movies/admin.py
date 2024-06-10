from django.contrib import admin
from .models import UserProfile, Movie, Review, Category

admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Category)
