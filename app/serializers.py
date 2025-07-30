from rest_framework import serializers
from .models import CustomUser, Track, FavoriteTrack, Favorite
from rest_framework.authentication import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'second_name', 'password']

    def save(self, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            second_name=self.validated_data['second_name'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            return user
        return False


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'second_name', 'is_staff']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'audio_file', 'cover_image', 'duration', 'uploaded_at']
        read_only_fields = ['duration']


class FavoriteTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = FavoriteTrack
        fields = ['id', 'track']


class SimplifiedFavoriteSerializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'tracks']

    def get_tracks(self, obj):
        favorite_tracks = obj.favoritetrack_set.all().select_related('track')
        return [
            {
                'id': ft.track.id,
                'title': ft.track.title,
                'artist': ft.track.artist,
                'audio_file': ft.track.audio_file.url if ft.track.audio_file else None,
                'cover_image': ft.track.cover_image.url if ft.track.cover_image else None,
                'duration': ft.track.duration,
                'uploaded_at': ft.track.uploaded_at
            }
            for ft in favorite_tracks
        ]