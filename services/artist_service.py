import datetime

from app_models.artist import Artist
from app_models.db_model import db
# This must be imported, so we can fetch all relevant info for the show
from app_models.show import Show
from services.general_service import GeneralService


class ArtistService:

    @staticmethod
    def get_artist_by_id(artist_id) -> Artist:
        """
        Returns artist by id with all necessary data calculated inside
        :param artist_id:
        :return:
        """
        artist = Artist.query.get(artist_id)
        past_shows = db.session.query(Show).join(Artist).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.datetime.now()).all()
        upcoming_shows = db.session.query(Show).join(Artist).filter(Show.artist_id == artist_id).filter(Show.start_time >= datetime.datetime.now()).all()

        setattr(artist, "past_shows", ArtistService.__transform_shows(past_shows))
        setattr(artist, "upcoming_shows", ArtistService.__transform_shows(upcoming_shows))
        setattr(artist, "past_shows_count", len(past_shows))
        setattr(artist, "upcoming_shows_count", len(upcoming_shows))

        return artist

    @staticmethod
    def get_all_artists() -> list[dict]:
        """
        Returns list of artists
        :return:
        """
        artists = Artist.query.all()
        return [{"id": artist.id, "name": artist.name} for artist in artists]

    @staticmethod
    def create_artist(form_data) -> Artist:
        """
        Returns an artist depending on the form data that is sent in the request
        :param form_data:
        :return:
        """

        artist = ArtistService.__parse_artist_obj(form_data)
        return artist

    @staticmethod
    def update_artist(form_data, artist_id):
        """
        Updates the artist from the db with our form data
        :param form_data:
        :param artist_id:
        :return:
        """
        artist_form = ArtistService.__parse_artist_obj(form_data)
        artist_db: Artist = Artist.query.get(artist_id)

        for key, value in artist_db.__dict__.items():
            if key == "id":
                continue
            elif hasattr(Artist, key) and getattr(artist_form, key) != value:
                setattr(artist_db, key, getattr(artist_form, key))

    @staticmethod
    def artist_search(search_term: str):
        """
        Search an artist by name -> if the search term is contained in the artist name than will give
        us a list of those artists. Its case-insensitive
        :param search_term:
        :return:
        """
        search_artists = Artist.query.filter(db.func.lower(Artist.name).contains(search_term)).all()
        return {"count": len(search_artists), "data": [GeneralService.parse_obj_short(artist) for artist in search_artists]}

    @staticmethod
    def __transform_shows(shows):
        for show in shows:
            setattr(show, "venue_name", show.venue.name)
            setattr(show, "venue_image_link", show.venue.image_link)
        return shows

    @staticmethod
    def __parse_artist_obj(form) -> Artist:
        return Artist(name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data,
                      genres=form.genres.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data,
                      website=form.website_link.data, seeking_venue=form.seeking_venue.data, seeking_description=form.seeking_description.data)
