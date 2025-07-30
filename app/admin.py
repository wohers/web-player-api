from django.contrib import admin
from .models import CustomUser, Track, Favorite, FavoriteTrack

admin.site.register(CustomUser)
admin.site.register(Track)
admin.site.register(Favorite)
admin.site.register(FavoriteTrack)