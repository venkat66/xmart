import googlemaps
from django.conf import settings



class GmapsClient(object):
    #Google Maps client class
    def __init__(self):

        try:
            self.client = googlemaps.Client(key=settings.GMAPS_API_KEY)
        except googlemaps.exceptions as e:
            print(f"authentication error: {e}")
    
    
    def getcoords(self,place):

        try:
            geocode_result = self.client.geocode(place)
            result=geocode_result[0]["geometry"]["location"]
            return result
        except:
            print("geocodeerror")