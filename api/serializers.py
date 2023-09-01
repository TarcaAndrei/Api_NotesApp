from rest_framework import serializers
from django.contrib.auth.models import User
from .models import List, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'listName']
        # fields = ('__all__')
        # fields = ['listName']

    def validate(self, data):
        list_instance = data
        print(data)
        user_request = self.context['request'].user
        if list_instance.user != user_request:
            raise serializers.ValidationError("Lista nu apartine")
        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'taskName', 'taskDetails', 'taskList']
        # fields += 'id'

    def __init__(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)
        user_request = self.context['request'].user
        self.fields['taskList'].queryset = List.objects.filter(user=user_request)
        #BUN ASA

    def validate(self, data):
        list_instance = data.get('taskList')
        user_request = self.context['request'].user
        if list_instance.user != user_request:
            raise serializers.ValidationError("Lista selectată nu aparține utilizatorlui autentificat.")
        return data
