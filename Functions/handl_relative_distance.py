from Functions.get_geo_distence import get_distance_miles
from users.models.user import PlayerFootballStat, Player


def handle_relative_dis(self):
    user_location = None
    try:
        user_location = self.request.user.player.location
    except:
        pass

    try:
        user_location = self.request.user.coach.location
    except:
        pass

    if user_location:
        for i in PlayerFootballStat.objects.all():
            try:
                P = Player.objects.get(id=i.player.id)
                location = P.location or i.location
                distance_miles = get_distance_miles(location, user_location)
                #
                if distance_miles:
                    P.location = location
                    P.distance_miles = distance_miles
                    P.save()

                    i.location = location
                    i.distance_miles = distance_miles
                    i.save()
            except:
                pass