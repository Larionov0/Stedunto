from typing import List, Optional
from .place import Place


class Location:
    def __init__(self, name, is_safe=False, mobs_info=None, places=None):
        self.name = name
        self.is_safe = is_safe

        if not mobs_info:
            mobs_info = {}
        self.mobs_info = mobs_info

        if not places:
            places = []
        self.places: List[Place] = places

    def add_place(self, place, symetry=True):
        self.places.append(place)
        if symetry:
            place.location = self

    @classmethod
    def create_from_dict(cls, dct):
        location = cls(dct['name'])
        location.fill_places_from_dict(dct)
        return location

    def fill_places_from_dict(self, dct):
        for place_dict in dct['places']:
            Place(place_dict['name'], 1, place_dict['id'], self)

    def find_place_by_id(self, id_):
        for place in self.places:
            if place.id == id_:
                return place
        raise ValueError(f"{self.name} -> {id_} ???")

    def find_places_by_id(self, *ids):
        places = []
        for place in self.places:
            if place.id in ids:
                places.append(place)

        if len(places) == len(ids):
            return places
        raise ValueError
