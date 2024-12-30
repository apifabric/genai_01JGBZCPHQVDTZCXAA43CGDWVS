# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Country(Base):
    """description: Stores details about countries participating in the Eurovision contest."""
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    code = Column(String)
    flag_image = Column(String)

class Contestant(Base):
    """description: Stores details of contestants participating in the Eurovision contest."""
    __tablename__ = 'contestant'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey('country.id'))
    bio = Column(String)

class Song(Base):
    """description: Stores information about songs that contestants perform."""
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    duration = Column(Integer)
    contestant_id = Column(Integer, ForeignKey('contestant.id'))
    language = Column(String)

class Judge(Base):
    """description: Stores details about judges in the Eurovision contest."""
    __tablename__ = 'judge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey('country.id'))
    experience_years = Column(Integer)

class Vote(Base):
    """description: Records votes given by judges to songs performed by contestants."""
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    judge_id = Column(Integer, ForeignKey('judge.id'))
    song_id = Column(Integer, ForeignKey('song.id'))
    points = Column(Integer)
    vote_time = Column(DateTime)

class Host(Base):
    """description: Stores information about the hosts of the Eurovision contest."""
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey('country.id'))
    years_hosted = Column(Integer)

class Event(Base):
    """description: Records details of Eurovision events held annually."""
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    city = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

class EventParticipation(Base):
    """description: Links contestants to the events they participate in."""
    __tablename__ = 'event_participation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'))
    contestant_id = Column(Integer, ForeignKey('contestant.id'))

class Jury(Base):
    """description: Associates judges with the events they are judging."""
    __tablename__ = 'jury'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'))
    judge_id = Column(Integer, ForeignKey('judge.id'))

class Performance(Base):
    """description: Stores details about performances in the Eurovision events."""
    __tablename__ = 'performance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'))
    song_id = Column(Integer, ForeignKey('song.id'))
    performance_time = Column(DateTime)

class VoteSummary(Base):
    """description: Stores the total points received by each song, calculated manually."""
    __tablename__ = 'vote_summary'
    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey('song.id'))
    total_points = Column(Integer)

class AudienceVote(Base):
    """description: Records audience votes for songs performed in events."""
    __tablename__ = 'audience_vote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'))
    song_id = Column(Integer, ForeignKey('song.id'))
    points = Column(Integer)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    country_row_1 = Country(name="United Kingdom", code="UK", flag_image="uk_flag.png")
    country_row_2 = Country(name="Germany", code="DE", flag_image="de_flag.png")
    country_row_3 = Country(name="Sweden", code="SE", flag_image="se_flag.png")
    country_row_4 = Country(name="Italy", code="IT", flag_image="it_flag.png")
    contestant_row_1 = Contestant(name="Contestant A", country_id=1, bio="Talented singer from UK.")
    contestant_row_2 = Contestant(name="Contestant B", country_id=2, bio="Top performer from Germany.")
    contestant_row_3 = Contestant(name="Contestant C", country_id=3, bio="Rising star from Sweden.")
    contestant_row_4 = Contestant(name="Contestant D", country_id=4, bio="Legendary singer from Italy.")
    song_row_1 = Song(title="Song A", duration=180, contestant_id=1, language="English")
    song_row_2 = Song(title="Song B", duration=190, contestant_id=2, language="German")
    song_row_3 = Song(title="Song C", duration=200, contestant_id=3, language="Swedish")
    song_row_4 = Song(title="Song D", duration=210, contestant_id=4, language="Italian")
    judge_row_1 = Judge(name="Judge A", country_id=1, experience_years=5)
    judge_row_2 = Judge(name="Judge B", country_id=2, experience_years=7)
    judge_row_3 = Judge(name="Judge C", country_id=3, experience_years=10)
    judge_row_4 = Judge(name="Judge D", country_id=4, experience_years=3)
    vote_row_1 = Vote(judge_id=1, song_id=1, points=12, vote_time=datetime.now())
    vote_row_2 = Vote(judge_id=2, song_id=2, points=10, vote_time=datetime.now())
    vote_row_3 = Vote(judge_id=3, song_id=3, points=8, vote_time=datetime.now())
    vote_row_4 = Vote(judge_id=4, song_id=4, points=6, vote_time=datetime.now())
    host_row_1 = Host(name="Host A", country_id=1, years_hosted=2)
    host_row_2 = Host(name="Host B", country_id=2, years_hosted=1)
    host_row_3 = Host(name="Host C", country_id=3, years_hosted=3)
    host_row_4 = Host(name="Host D", country_id=4, years_hosted=1)
    event_row_1 = Event(year=2023, city="London", start_date=date(2023, 5, 1), end_date=date(2023, 5, 14))
    event_row_2 = Event(year=2022, city="Berlin", start_date=date(2022, 6, 4), end_date=date(2022, 6, 18))
    event_row_3 = Event(year=2021, city="Stockholm", start_date=date(2021, 5, 2), end_date=date(2021, 5, 16))
    event_row_4 = Event(year=2020, city="Rome", start_date=date(2020, 4, 25), end_date=date(2020, 5, 9))
    event_participation_row_1 = EventParticipation(event_id=1, contestant_id=1)
    event_participation_row_2 = EventParticipation(event_id=2, contestant_id=2)
    event_participation_row_3 = EventParticipation(event_id=3, contestant_id=3)
    event_participation_row_4 = EventParticipation(event_id=4, contestant_id=4)
    jury_row_1 = Jury(event_id=1, judge_id=1)
    jury_row_2 = Jury(event_id=2, judge_id=2)
    jury_row_3 = Jury(event_id=3, judge_id=3)
    jury_row_4 = Jury(event_id=4, judge_id=4)
    performance_row_1 = Performance(event_id=1, song_id=1, performance_time=datetime.now())
    performance_row_2 = Performance(event_id=2, song_id=2, performance_time=datetime.now())
    performance_row_3 = Performance(event_id=3, song_id=3, performance_time=datetime.now())
    performance_row_4 = Performance(event_id=4, song_id=4, performance_time=datetime.now())
    vote_summary_row_1 = VoteSummary(song_id=1, total_points=12)
    vote_summary_row_2 = VoteSummary(song_id=2, total_points=10)
    vote_summary_row_3 = VoteSummary(song_id=3, total_points=8)
    vote_summary_row_4 = VoteSummary(song_id=4, total_points=6)
    audience_vote_row_1 = AudienceVote(event_id=1, song_id=1, points=100)
    audience_vote_row_2 = AudienceVote(event_id=2, song_id=2, points=200)
    audience_vote_row_3 = AudienceVote(event_id=3, song_id=3, points=150)
    audience_vote_row_4 = AudienceVote(event_id=4, song_id=4, points=180)
    
    
    
    session.add_all([country_row_1, country_row_2, country_row_3, country_row_4, contestant_row_1, contestant_row_2, contestant_row_3, contestant_row_4, song_row_1, song_row_2, song_row_3, song_row_4, judge_row_1, judge_row_2, judge_row_3, judge_row_4, vote_row_1, vote_row_2, vote_row_3, vote_row_4, host_row_1, host_row_2, host_row_3, host_row_4, event_row_1, event_row_2, event_row_3, event_row_4, event_participation_row_1, event_participation_row_2, event_participation_row_3, event_participation_row_4, jury_row_1, jury_row_2, jury_row_3, jury_row_4, performance_row_1, performance_row_2, performance_row_3, performance_row_4, vote_summary_row_1, vote_summary_row_2, vote_summary_row_3, vote_summary_row_4, audience_vote_row_1, audience_vote_row_2, audience_vote_row_3, audience_vote_row_4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
