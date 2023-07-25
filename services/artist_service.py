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
        setattr(artist, "past_shows", [])
        setattr(artist, "upcoming_shows", [])
        date_now = datetime.datetime.now()
        for show in artist.shows:
            ArtistService.__shows_per_date(artist, show, "past_shows") if date_now > show.start_time \
                else ArtistService.__shows_per_date(artist, show, "upcoming_shows")

        setattr(artist, "past_shows_count", len(getattr(artist, "past_shows")))
        setattr(artist, "upcoming_shows_count", len(getattr(artist, "upcoming_shows")))
        return artist

    @staticmethod
    def get_all_artists():
        """
        Returns list of artists
        :return:
        """
        artists = Artist.query.all()
        return [{"id": artist.id, "name": artist.name} for artist in artists]

    @staticmethod
    def create_artist(request) -> Artist:
        """
        Creates an artist depending on the form data that is sent in the request
        :param request:
        :return:
        """
        artist = ArtistService.__parse_artist_obj(request)
        return artist

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
    def __shows_per_date(artist, show, attribute):
        shows = getattr(artist, attribute)
        setattr(show, "venue_name", show.venue.name)
        setattr(show, "venue_image_link", show.venue.image_link)
        shows.append(show)
        setattr(artist, attribute, shows)

    @staticmethod
    def __parse_artist_obj(request) -> Artist:
        seeking_venue = False
        for index, form_data in enumerate(request.form):
            if form_data == "seeking_venue":
                seeking_venue = True
                break
        return Artist(name=request.form["name"], city=request.form["city"], state=request.form["state"],
                      phone=request.form["phone"], genres=[request.form["genres"]], image_link=request.form["image_link"],
                      facebook_link=request.form["facebook_link"], website=request.form["website_link"],
                      seeking_venue=seeking_venue, seeking_description=request.form["seeking_description"])
