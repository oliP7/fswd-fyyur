import datetime

from app_models.db_model import db
from app_models.venue import Venue
# This must be imported, so we can fetch all relevant info for the show
from app_models.show import Show
from app_models.artist import Artist
from services.general_service import GeneralService


class VenueService:

    @staticmethod
    def get_venue_by_id(venue_id) -> Venue:
        """
        Returns venue by id with all necessary data calculated inside
        :param venue_id:
        :return:
        """
        venue = Venue.query.get(venue_id)
        past_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.datetime.now()).all()
        upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(
            Show.start_time >= datetime.datetime.now()).all()

        setattr(venue, "past_shows", VenueService.__transform_shows(past_shows))
        setattr(venue, "upcoming_shows", VenueService.__transform_shows(upcoming_shows))
        setattr(venue, "past_shows_count", len(past_shows))
        setattr(venue, "upcoming_shows_count", len(upcoming_shows))

        return venue

    @staticmethod
    def get_all_venues():
        """
        Returns list of venues grouped by city and state
        :return:
        """
        data = []
        venues: list[Venue] = Venue.query.all()
        venues_per_city = db.session.query(Venue.city, Venue.state, db.func.count(Venue.id)).group_by(Venue.city,
                                                                                                      Venue.state).all()
        for (city, state, count) in venues_per_city:
            data.append(VenueService.__parse_venue_per_city(city, state, venues))

        return data

    @staticmethod
    def create_venue(form_data) -> Venue:
        """
        Creates a venue depending on the form data that is sent in the request
        :param request:
        :return:
        """
        venue = VenueService.__parse_venue_obj(form_data)
        return venue

    @staticmethod
    def update_venue(form_data, venue_id):
        """
        Updates the venue from the db with our form data
        :param form_data:
        :param venue_id:
        :return:
        """
        venue_form = VenueService.__parse_venue_obj(form_data)
        venue_db: Venue = Venue.query.get(venue_id)

        for key, value in venue_db.__dict__.items():
            if key == "id":
                continue
            elif hasattr(Venue, key) and getattr(venue_form, key) != value:
                setattr(venue_db, key, getattr(venue_form, key))

    @staticmethod
    def venue_search(search_term: str):
        """
        Search a venue by name -> if the search term is contained in the venue name than will give
        us a list of all venues. Its case-insensitive
        :param search_term:
        :return:
        """
        search_venues = Venue.query.filter(db.func.lower(Venue.name).contains(search_term)).all()
        return {"count": len(search_venues), "data": [GeneralService.parse_obj_short(venue) for venue in search_venues]}

    @staticmethod
    def __transform_shows(shows):
        for show in shows:
            setattr(show, "artist_name", show.artist.name)
            setattr(show, "artist_image_link", show.artist.image_link)
        return shows

    @staticmethod
    def __parse_venue_per_city(city: str, state: str, venues: list[Venue]):
        return {"city": city, "state": state,
                "venues": [GeneralService.parse_obj_short(venue) for venue in venues if venue.city == city and venue.state == state]}

    @staticmethod
    def __parse_venue_obj(form) -> Venue:
        return Venue(name=form.name.data, address=form.address.data, city=form.city.data,
                     state=form.state.data, phone=form.phone.data, website=form.website_link.data,
                     facebook_link=form.facebook_link.data, image_link=form.image_link.data,
                     genres=form.genres.data, seeking_talent=form.seeking_talent.data,
                     seeking_description=form.seeking_description.data)
