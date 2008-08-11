import pkg_resources
pkg_resources.require("SQLAlchemy>=0.3.10")
from turbogears.database import metadata, mapper
# import some basic SQLAlchemy classes for declaring the data model
# (see http://www.sqlalchemy.org/docs/04/ormtutorial.html)
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relation
# import some datatypes for table columns from SQLAlchemy
# (see http://www.sqlalchemy.org/docs/04/types.html for more)
from sqlalchemy import String, Unicode, Integer, DateTime
from ffbstatssa.lib.identity import *


# data tables
teams_table = Table('teams', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('owner', String),
)

scores_table = Table('scores', metadata,
    Column('id', Integer, primary_key=True),
    Column('score', Integer),
    Column('possible_score', Integer),
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
    Column('score_id', Integer, ForeignKey('scores.id'))
)

games_teams_table = Table('games_teams', metadata,
    Column('id', Integer, primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('game_id', Integer, ForeignKey('games.id')),
)

# model classes
class Team(object):
    pass

class Score(object):
    pass

class Week(object):
    pass

class Game(object):
    pass

# mappers between data tables and classes
mapper(Team, teams_table)
mapper(Score, scores_table,
       properties={
           'team' : relation(
               Team, backref='scores')
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
