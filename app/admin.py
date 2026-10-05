from django.contrib import admin
from .models import CustomUser, Track, Favorite, FavoriteTrack, Heroes
admin.site.register(CustomUser)
admin.site.register(Track)
admin.site.register(Favorite)
admin.site.register(FavoriteTrack)
admin.site.register(Heroes)