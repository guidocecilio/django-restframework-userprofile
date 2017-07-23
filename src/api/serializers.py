from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Profile, Topic


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_staff', 'profile')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    user = serializers.ReadOnlyField(source='user.id')
    full_name = serializers.SerializerMethodField(source='get_full_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Profile
        depth = 1
        fields = ('url', 'id', 'full_name', 'email', 'current_position',
                  'about_you', 'favorite_topics', 'user', 'user_url')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ('url', 'id', 'name', 'description')