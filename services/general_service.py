import datetime


class GeneralService:

    @staticmethod
    def parse_obj_short(obj):
        return {"id": obj.id, "name": obj.name, "num_upcoming_shows": len(GeneralService.__get_upcoming_shows(obj))}

    @staticmethod
    def __get_upcoming_shows(obj):
        date_now = datetime.datetime.now()
        return [show for show in obj.shows if date_now < show.start_time]
