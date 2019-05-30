from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'text', 'specialty', 'plan', 'plan_rez', 'plan_clock',
                  'plan_clock_rez', 'plan_all', 'plan_rez_all', 'plan_clock_all',
                  'plan_defect', 'plan_defect_all', 'cex_plan_all', 'cex_defect_all')