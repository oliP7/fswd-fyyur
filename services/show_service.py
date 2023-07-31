import datetime

from sqlalchemy import or_

from app_models.db_model import db
from app_models.show import Show
# This must be imported, so we can fetch all relevant info for the show
from app_models.venue import Venue
from app_models.artist import Artist


class ShowService:

    @staticmethod
    def get_all_shows() -> list[dict]:
        """
        Returns list of shows
        :return:
        """

        shows: list[Show] = Show.query.all()
        data = [ShowService.__parse_show_display(show) for show in shows]

        return data

    @staticmethod
    def create_show(request) -> Show:
        """
        Creates a show depending on the form data that is sent in the request
        :param request:
        :return:
        """
        show = ShowService.__parse_show_obj(request)
        return show

    @staticmethod
    def show_search(search_term: str):
        """
        Search a show by artist name or venue name -> if the search term is contained than will give us a list of all shows. Its case-insensitive
        :param search_term:
        :return:
        """
        search_shows = db.session.query(Show).join(Artist, Show.artist_id == Artist.id).join(Venue, Show.venue_id == Venue.id)\
            .filter(or_(db.func.lower(Artist.name).contains(search_term), db.func.lower(Venue.name).contains(search_term))).all()

        return {"count": len(search_shows), "data": [ShowService.__parse_show_display(show) for show in search_shows]}

    @staticmethod
    def __shows_per_date(venue, show, attribute):
        shows = getattr(venue, attribute)
        setattr(show, "artist_name", show.artist.name)
        setattr(show, "artist_image_link", show.artist.image_link)
        shows.append(show)
        setattr(venue, attribute, shows)

    @staticmethod
    def __parse_show_display(show: Show):
        return {"venue_id": show.venue_id, "venue_name": show.venue.name,
                "artist_id": show.artist_id, "artist_name":  show.artist.name, "artist_image_link": show.artist.image_link,
                "start_time": show.start_time}

    @staticmethod
    def __parse_show_obj(request) -> Show:
        date_format = '%Y-%m-%d %H:%M:%S'
        date_obj = datetime.datetime.strptime(request.form["start_time"], date_format)
        return Show(artist_id=request.form["artist_id"], venue_id=request.form["venue_id"], start_time=date_obj)


