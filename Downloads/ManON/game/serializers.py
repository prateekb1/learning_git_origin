from rest_framework import serializers
from .models import GameModel, SearchModel, ResumeGame


class GameModelSerializer(serializers.ModelSerializer):
    """for serializing data to required format"""
    user_id = serializers.CharField(max_length=20)
    # id = serializers.IntegerField()
    # player1 = serializers.CharField(max_length=100)
    # player1_score = serializers.IntegerField(default=0)
    # player2 = serializers.CharField(max_length=50)
    dateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # player2_score = serializers.IntegerField(default=0)
    # player1_team = serializers.CharField(max_length=50)
    # player2_team = serializers.CharField(max_length=50)

    class Meta:
        model = GameModel
        read_only = ['id']
        fields = "__all__"

    def create(self, validated_data):
        return GameModel.objects.create(**validated_data)


class SearchModelSerializer(serializers.ModelSerializer):
    """To serialize and create the data of Searched team"""

    class Meta:
        model = SearchModel
        fields = '__all__'


class ResumeModelSerializer(serializers.ModelSerializer):
    """To serialize and create the data of Searched team"""
    user_id = serializers.IntegerField()
    gameState = serializers.JSONField()

    class Meta:
        model = ResumeGame
        fields = '__all__'

    # def create(self, validated_data):
    #     return ResumeGame.objects.create(**validated_data)
