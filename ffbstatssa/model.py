import pkg_resources
pkg_resources.require("SQLAlchemy>=0.3.10")
from turbogears.database import metadata, mapper
# import some basic SQLAlchemy classes for declaring the data model
# (see http://www.sqlalchemy.org/docs/04/ormtutorial.html)
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relation
# import some datatypes for table columns from SQLAlchemy
# (see http://www.sqlalchemy.org/docs/04/types.html for more)
from sqlalchemy import String, Unicode, Integer, DateTime, Float
from ffbstatssa.lib.identity import *


# data tables
teams_table = Table('teams', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('owner', String),
)

scores_table = Table('scores', metadata,
    Column('id', Integer, primary_key=True),
    Column('score', Float),
    Column('possible_score', Float),
    Column('team_id', Integer, ForeignKey('teams.id')),
)

weeks_table = Table('weeks', metadata,
    Column('id', Integer, primary_key=True),
    Column('week_num', Integer),
    Column('comments', String),
)

games_table = Table('games', metadata,
    Column('id', Integer, primary_key=True),
    Column('week_id', Integer, ForeignKey('weeks.id')),
)
    
games_scores_table = Table('games_scores', metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('score_id', Integer, ForeignKey('scores.id')),
)

games_teams_table = Table('games_teams', metadata,
    Column('id', Integer, primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('game_id', Integer, ForeignKey('games.id')),
)

opponents_table = Table('opponents', metadata,
    Column('id', Integer, primary_key=True),
    Column('score01_id', Integer, ForeignKey('scores.id')),
    Column('score02_id', Integer, ForeignKey('scores.id')),
)

# model classes
class Team(object):
    '''
    Attributes:
    name, owner, scores, games, total_points, total_possible_points, efficiency, wins, losses
    '''
    def __init__(self, name, owner, scores):
        self.name = name
        self.owner = owner
        self.scores = scores
        
    def __repr__(self):
        return "<Team('%s', '%s')>" % (self.name, self.owner)
    
    def total_points(self):
        total_points = 0
        for score in self.scores:
            total_points += score.score
        return total_points
    total_points = property(total_points)
    
    def total_possible_points(self):
        total_possible_points = 0
        for score in self.scores:
            total_possible_points += score.possible_score
        return total_possible_points
    total_possible_points = property(total_possible_points)
    
    def efficiency(self):
        result = 0
        if self.total_possible_points > 0:
            result = float(self.total_points) / float(self.total_possible_points)
        else:
            result = 0
        return result
    efficiency = property(efficiency)
    
    def wins(self):
        result = 0
        for game in self.games:
            our_score = 0
            their_score = 0
            for score in game.scores:
                if score.team == self:
                    our_score = score.score
                else:
                    their_score = score.score
            if our_score > their_score:
                result += 1
        return result
    wins = property(wins)
    
    def losses(self):
        result = 0
        for game in self.games:
            our_score = 0
            their_score = 0
            for score in game.scores:
                if score.team == self:
                    our_score = score.score
                else:
                    their_score = score.score
            if our_score < their_score:
                result += 1
        return result
    losses = property(losses)

class Score(object):
    def __init__(self, score, possible_score, team):
        self.score = score
        self.possible_score = possible_score
        self.team = team
        
    def __repr__(self):
        return "<Score('%s', '%s', '%s')>" % (
            self.score, self.possible_score, self.team.name
        )

class Week(object):
    def __init__(self, week_num, comments):
        self.week_num = week_num
        self.comments = comments
        
    def __repr__(self):
        return "<Week('%s', '%s')>" % (self.week_num, self.comments)

class Game(object):
    def __init__(self, week, teams, scores):
        self.week = week
        self.teams = teams
        self.scores = scores
        
    def __repr__(self):
        teams = []
        scores = []
        for score in self.scores:
            teams.append(score.team.name)
            scores.append(score.score)
        return "<Game('%s', '%s', '%s')>" % (
            self.week.week_num, teams, scores
        )

# mappers between data tables and classes
mapper(Team, teams_table)
mapper(Score, scores_table,
       properties={
           'team' : relation(
               Team, backref='scores'),
       }
)
mapper(Week, weeks_table)
mapper(Game, games_table,
       properties={
           'week' : relation(
               Week, backref='games'),
           'scores' : relation(
               Score, secondary=games_scores_table, backref='game'),
           'teams' : relation(
               Team, secondary=games_teams_table, backref='games'),
       }
)
