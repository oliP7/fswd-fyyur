import re
from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL

from app_models.genre_enum import Genre
from app_models.state_enum import State


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField(
        'seeking_description'
    )

    def validate(self, **kwargs):
        validated = Form.validate(self)

        if not validated:
            return False

        if not is_valid_phone(self.phone.data):
            self.phone.errors.append("Invalid phone")
            return False

        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append("Invalid genres")
            return False

        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append("Invalid state")
            return False

        return True



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

    website_link = StringField(
        'website_link'
    )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
        'seeking_description'
    )

    def validate(self, **kwargs):
        validated = Form.validate(self)

        if not validated:
            return False

        if not is_valid_phone(self.phone.data):
            self.phone.errors.append("Invalid phone")
            return False

        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append("Invalid genres")
            return False

        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append("Invalid state")
            return False

        return True


def is_valid_phone(number):
    """Validation on phone number"""
    regex = re.compile('^\(?\d{3}\)?[-. ]?\d{3}[-. ]\d{4}$')
    return regex.match(number)
