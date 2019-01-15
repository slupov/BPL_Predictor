from django.db import models


# Create your models here.

class MatchRawData(models.Model):
    date = models.DateField(null=True)
    home_team = models.CharField(max_length=60)
    away_team = models.CharField(max_length=60)
    full_time_home_goals = models.IntegerField()
    full_time_away_goals = models.IntegerField()
    full_time_result = models.FloatField()
    half_time_home_goals = models.IntegerField(null=True)
    half_time_away_goals = models.IntegerField(null=True)
    half_time_result = models.FloatField(null=True)
    attendance = models.IntegerField(null=True)
    home_shots = models.IntegerField(null=True)
    away_shots = models.IntegerField(null=True)
    home_woodwork_hits = models.IntegerField(null=True)
    away_woodwork_hits = models.IntegerField(null=True)
    home_corners = models.IntegerField(null=True)
    away_corners = models.IntegerField(null=True)
    home_fouls_commited = models.IntegerField(null=True)
    away_fouls_commited = models.IntegerField(null=True)
    home_offsides = models.IntegerField(null=True)
    away_offsides = models.IntegerField(null=True)
    home_red_cards = models.IntegerField(null=True)
    away_red_cards = models.IntegerField(null=True)
    home_yellow_cards = models.IntegerField(null=True)
    away_yellow_cards = models.IntegerField(null=True)

    def __str__(self):
        return self.home_team + " " +\
               str(self.full_time_home_goals) +" : " +\
               str(self.full_time_away_goals) + " " +\
               self.away_team


