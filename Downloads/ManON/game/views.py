import datetime
import operator
import re
from functools import reduce

from django.db.models import Q
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from game.models import GameModel, SearchModel, ResumeGame
from game.serializers import GameModelSerializer, SearchModelSerializer, ResumeModelSerializer
from user_data.models import UserTable
from user_data.permissions import IsOwnerOrReadOnly

ModelViewSet
class GameView(APIView):
    """ Api for post the game history and retrive the game history"""
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        """to get the game history and will shown to user"""
        query_set = GameModel.objects.filter(user_id=request.user.id).order_by('-dateTime')
        serializer = GameModelSerializer(query_set, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """To store the the game details"""
        user = UserTable.objects.get(id=request.user.id)
        opponent = UserTable.objects.get(search_id=request.data['user_id'])
        if opponent.team_name != user.team_name:

            data = {
                "user_id": user.id,
                # "player_id":user.user_id,
                'player1': user.player_name,
                "player1_team": user.team_name,
                "player2": opponent.player_name,
                "dateTime": datetime.datetime.now(),
                "player2_team": opponent.team_name,
                "player1_score": request.data['player1_score'],
                "player2_score": request.data['player2_score'],
            }
            serializer = GameModelSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "user can't play with himself"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # print()
        snippet = GameModel.objects.get(id=request.query_params["id"])
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchPlayer(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = []
        result = re.match("[a-z.0-9]+@[a-z]+\.[a-z]{2,3}", request.query_params["id"])
        query.append(Q(email=request.query_params['id'])) if result else query.append(
            Q(search_id=request.query_params['id']))
        if UserTable.objects.filter(reduce(operator.or_, query)).exists():
            User = UserTable.objects.get(reduce(operator.or_, query))
            if request.user == User:
                return Response({"details": "You can't play with your self"}, status=status.HTTP_400_BAD_REQUEST)
            # print(User.email)
            data = {
                "user": request.user.id,
                "player_id": User.search_id,
                "player_name": User.player_name,
                "player_team": User.team_name,
                "email": User.email
            }
            player = SearchModel.objects.filter(user=request.user.id)
            if player.filter(player_id=User.search_id).exists():
                pass
            else:
                serializer = SearchModelSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            return Response({
                "user_id": User.search_id,
                "player_name": User.player_name,
                "player_team": User.team_name,
                "email": User.email,
            }, status=status.HTTP_200_OK)

        return Response({"details": "We can't find any account "}, status=status.HTTP_404_NOT_FOUND)


class SearchHistory(APIView):
    """To get the details of every user present in the database"""
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get(self, request):
        """get the details of users search history"""
        query_set = SearchModel.objects.filter(user=request.user.id)
        serializer = SearchModelSerializer(query_set, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class ResumeView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        """get the details of users search history"""
        query_set = ResumeGame.objects.filter(user=request.user.id)
        serializer = ResumeModelSerializer(query_set, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        query_set = request.data
        list1 = ResumeGame.objects.filter(user_id=request.user.id).values()
        if list1:
            gamestate = list(list1[0]["gameState"])
            # for each_dict in query_set["gameState"]:
            #     gamestate.append(each_dict)
            for each_dict in query_set["gameState"]:
                if each_dict in gamestate:
                    pass
                else:
                    gamestate.append(each_dict)
            # gamestate.append(query_set["gameState"])
        else:
            gamestate = query_set["gameState"]

        # if ResumeGame.objects.filter(user_id=request.user.id).exists():
        #     query_table = ResumeGame.objects.get(user_id=request.user.id).delete()
        data = {
            "user_id": request.user.id,
            "userid1": query_set["userid1"],
            "userid2": query_set["userid2"],
            "player1": query_set["player1"],
            "player2": query_set["player2"],
            "team1": query_set["team1"],
            "team2": query_set["team2"],
            "score1": query_set["score1"],
            "score2": query_set["score2"],
            "inningHalf": query_set["inningHalf"],
            "teamSwitching": query_set["teamSwitching"],
            "positions1": query_set["positions1"],
            "position2": query_set["position2"],
            "position3": query_set["position3"],
            "topBottom": query_set["topBottom"],
            "inning": query_set["inning"],
            "balls": query_set["balls"],
            "outs": query_set["outs"],
            "donehits": query_set["donehits"],
            "EH": query_set["EH"],
            "hitCount": query_set["hitCount"],
            "activeGameStep": query_set["activeGameStep"],
            "gameState": gamestate

        }
        #serializer = ResumeModelSerializer(data=data)
        # request.data["user_id"] = request.user.id
        if ResumeGame.objects.filter(user_id=request.user.id).exists():
            # partial = kwargs.pop('partial', False)
            # instance = self.get_object()

            serializer =ResumeModelSerializer(ResumeGame.objects.get(user_id=request.user.id), data=data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # self.perform_update(serializer)
            # serializer = ResumeModelSerializer(query_set, data=data)
        else:
            serializer = ResumeModelSerializer(data=data)
        # serializer = ResumeModelSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"details": "We can't find any account "}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        if ResumeGame.objects.filter(user_id=request.user.id).exists():
            ResumeGame.objects.get(user_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

