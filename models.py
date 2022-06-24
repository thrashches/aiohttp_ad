from pydantic import BaseModel
from app import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    _idx1 = db.Index('app_users_username', 'username', unique=True)


class UserValidationModel(BaseModel):
    username: str
    password: str


class AdvertisementModel(db.Model):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_created': str(self.date_created),
            'user_id': self.user_id
        }


class AdvertisementValidationModel(BaseModel):
    title: str
    description: str
    user_id: int
