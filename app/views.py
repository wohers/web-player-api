from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer, UserRegisterSerializer, GetUserSerializer, TrackSerializer,  FavoriteTrackSerializer, SimplifiedFavoriteSerializer, HeroesSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied, AuthenticationFailed
from .models import Track, FavoriteTrack, Favorite, Heroes
import mutagen
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def create_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'data': {
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'second_name': user.second_name,
                    'is_staff': user.is_staff
                }
            }
        }, status=status.HTTP_201_CREATED)
    raise ValidationError(serializer.errors)
    


@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        if not user:
            raise AuthenticationFailed
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'data': {
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'second_name': user.second_name,
                    'is_staff': user.is_staff
                }
            }
        }, status=status.HTTP_200_OK)
    raise ValidationError(serializer.errors)


@api_view(['GET'])
def get_me(request):
    user = request.user
    serializer = GetUserSerializer(user)
    return Response({
        'data': {
            'user': serializer.data
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({
        'message': 'success'
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def track_list(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = request.FILES['audio_file']
            audio_info = mutagen.File(audio_file.temporary_file_path())
            duration = int(audio_info.info.length)
            serializer.save(duration=duration)
            return Response({
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)
    return None


@api_view(['GET', 'PUT', 'DELETE'])
def track_detail(request, pk):
    track = Track.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = TrackSerializer(track)
        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TrackSerializer(track, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors)
    elif request.method == 'DELETE':
        track.delete()
        return Response({
            'data': {
                'code': 204,
                'message': 'success'
            }
        },status=status.HTTP_200_OK)
    return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    favorite = get_object_or_404(
        Favorite.objects.prefetch_related('favoritetrack_set__track'),
        user=request.user
    )
    serializer = SimplifiedFavoriteSerializer(favorite)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_action(request, track_id):
    track = get_object_or_404(Track, id=track_id)

    favorite, _ = Favorite.objects.get_or_create(user=request.user)

    if favorite.tracks.filter(id=track_id).exists():
        favorite.tracks.remove(track)
        return Response({'status': 'removed'}, status=status.HTTP_200_OK)
    else:
        favorite.tracks.add(track)
        return Response({'status': 'added'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_heroes(request):
    heroes = Heroes.objects.all()
    serializer = HeroesSerializer(heroes, many=True)
    return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)