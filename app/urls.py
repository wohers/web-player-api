from django.urls import path
from .views import create_user, login_user, get_me,track_detail, track_list, get_favorites,  favorite_action, logout, get_heroes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', login_user),
    path('signup', create_user),
    path('me', get_me),
    path('logout', logout),

    path('tracks', track_list),
    path('tracks/<int:pk>', track_detail),

    path('favorites', get_favorites),
    path('favorites/<int:track_id>', favorite_action),

    path('heroes', get_heroes),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)