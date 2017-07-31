from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Profile, Topic


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail')
    class Meta:
        model = User
        depth = 1
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_staff', 'profile', 'profile_url')


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        depth = 1
        model = Topic
        fields = ('url', 'id', 'name', 'description')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    user = serializers.ReadOnlyField(source='user.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    favorite_topics = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        queryset=Topic.objects.all(),
        view_name='topic-detail'
    )

    class Meta:
        model = Profile
        depth = 1
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name',
                  'current_position', 'about_you', 'favorite_topics', 'user',
                  'user_url')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance

