from app_models.db_model import db


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    music_genres = db.Column(db.ARRAY(db.String(120)))

    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")
