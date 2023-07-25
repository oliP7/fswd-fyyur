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
        setattr(venue, "past_shows", [])
        setattr(venue, "upcoming_shows", [])
        date_now = datetime.datetime.now()
        for show in venue.shows:
            VenueService.__shows_per_date(venue, show, "past_shows") if date_now > show.start_time \
                else VenueService.__shows_per_date(venue, show, "upcoming_shows")

        setattr(venue, "past_shows_count", len(getattr(venue, "past_shows")))
        setattr(venue, "upcoming_shows_count", len(getattr(venue, "upcoming_shows")))
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
    def create_venue(request) -> Venue:
        """
        Creates a venue depending on the form data that is sent in the request
        :param request:
        :return:
        """
        venue = VenueService.__parse_venue_obj(request)
        return venue

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
    def __shows_per_date(venue, show, attribute):
        shows = getattr(venue, attribute)
        setattr(show, "artist_name", show.artist.name)
        setattr(show, "artist_image_link", show.artist.image_link)
        shows.append(show)
        setattr(venue, attribute, shows)

    @staticmethod
    def __parse_venue_per_city(city: str, state: str, venues: list[Venue]):
        return {"city": city, "state": state,
                "venues": [GeneralService.parse_obj_short(venue) for venue in venues if venue.city == city and venue.state == state]}

    @staticmethod
    def __parse_venue_obj(request) -> Venue:
        seeking_talent = False
        for index, form_data in enumerate(request.form):
            if form_data == "seeking_talent":
                seeking_talent = True
                break
        return Venue(name=request.form["name"], address=request.form["address"], city=request.form["city"],
                     state=request.form["state"], phone=request.form["phone"], website=request.form["website_link"],
                     facebook_link=request.form["facebook_link"], image_link=request.form["image_link"],
                     genres=[request.form["genres"]], seeking_talent=seeking_talent,
                     seeking_description=request.form["seeking_description"])
