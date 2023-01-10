from django.db import models
from user_data.models import UserTable


class GameModel(models.Model):
    """model to store the game history """
    user = models.ForeignKey(UserTable, null=True, on_delete=models.CASCADE)
    # player_id = models.IntegerField(null=True)
    player1 = models.CharField(max_length=50)
    player1_score = models.IntegerField(default=0)
    player2 = models.CharField(max_length=50)
    player2_score = models.IntegerField(default=0)
    dateTime = models.DateTimeField()
    player1_team = models.CharField(max_length=50)
    player2_team = models.CharField(max_length=50)

    def __str__(self):
        return str(self.player1)


class SearchModel(models.Model):
    user = models.ForeignKey(UserTable, null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=False, null=True)
    player_id = models.IntegerField()
    player_name = models.CharField(max_length=50)
    player_team = models.CharField(max_length=50)

    def __str__(self):
        return str(self.pk)


class ResumeGame(models.Model):
    user = models.OneToOneField(UserTable, null=True, on_delete=models.CASCADE)
    userid1 = models.IntegerField()
    userid2 = models.IntegerField()
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    inningHalf = models.IntegerField(default=0)
    teamSwitching= models.BooleanField(default=True)
    positions1 = models.BooleanField()
    position2 = models.BooleanField()
    position3 = models.BooleanField(default=0)
    topBottom = models.IntegerField(null=True)
    inning = models.IntegerField()
    balls = models.IntegerField()
    outs = models.IntegerField()
    donehits = models.IntegerField()
    EH = models.BooleanField()
    hitCount = models.IntegerField(default=9)
    activeGameStep = models.IntegerField(default=0)
    gameState = models.JSONField(blank=True, default=[])

    def __str__(self):
        return str(self.userid1)