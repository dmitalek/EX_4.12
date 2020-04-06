import uuid
import datetime

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    __tablename__ = 'athelete'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    name = db.Column(db.Text)
    gold_medals = db.Column(db.Integer)
    silver_medals = db.Column(db.Integer)
    bronze_medals = db.Column(db.Integer)
    total_medals = db.Column(db.Integer)
    gender = db.Column(db.Text)
    sport = db.Column(db.Text)
    birthdate = db.Column(db.Text)
    height = db.Column(db.Text)
    weight = db.Column(db.Text)
    country = db.Column(db.Text)

class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    gender = db.Column(db.Text)
    email = db.Column(db.Text)
    birthdate = db.Column(db.Text)
    height = db.Column(db.Text)

def connect_db():
    
    engine = db.create_engine(db_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    
    print("Ищем атлетов")
    user_id = input("Введите id пользователя")
    return int(user_id)
    
def convert_str_to_date(date_str):
    
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def nearest_by_bd(user, session):
    
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    
    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd
    return athlete_id, athlete_bd


def nearest_by_height(user, session):
    
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}
    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height


def main():
    
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя нет ")
    else:
        bd_athlete, bd = nearest_by_bd(user, session)
        height_athlete, height = nearest_by_height(user, session)
        print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd))
        print("Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height))


if __name__ == "__main__":
    main()