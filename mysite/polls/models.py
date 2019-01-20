from django.db import models


# Create your models here.

class MatchRawData(models.Model):
    class Meta:
        unique_together = (('date', 'home_team', 'away_team'),)

    date = models.DateField(null=True)
    season = models.CharField(max_length=5, null=True)
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
        return "Date: %s Season: %s %s %s:%s %s FTR: %s" \
              % (self.date, self.season, self.home_team, self.full_time_home_goals,
                 self.full_time_away_goals, self.away_team, self.full_time_result)


class ExtractedFixtures(models.Model):
    class Meta:
        unique_together = (('season', 'home_team', 'away_team'),)

    season = models.CharField(max_length=5)
    home_team = models.CharField(max_length=60)
    away_team = models.CharField(max_length=60)
    home_form = models.FloatField()
    away_form = models.FloatField()
    result = models.FloatField()
    home_concentration = models.FloatField()
    away_concentration = models.FloatField()
    goal_diff = models.FloatField()
    score_diff = models.FloatField()
    history = models.FloatField()
    home_motivation = models.FloatField()
    away_motivation = models.FloatField()

    def __str__(self):
        return "Season: " + self.season + " " + self.home_team + " " + \
               self.away_team


class SeasonTables(models.Model):
    class Meta:
        unique_together = (('season', 'team', 'round_start', 'round_end'))

    season = models.CharField(max_length=5)
    team = models.CharField(max_length=60)
    round_start = models.DateField(null=True)
    round_end = models.DateField(null=True)
    wins = models.IntegerField(null=True)
    draws = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    goals_scored = models.IntegerField(null=True)
    goals_received = models.IntegerField(null=True)
    position = models.IntegerField(null=True)

    def __str__(self):
        return "Season: %s, Pos: [%s], Team: %s, Round dates: %s - %s, W: %s, D: %s, " \
              "L: %s Pts: %s GS: %s, GR: %s" % \
              (str(self.season), str(self.position), str(self.team),
               str(self.round_start), str(self.round_end), str(self.wins),
               str(self.draws), str(self.losses), str(self.points),
               str(self.goals_scored), str(self.goals_received))