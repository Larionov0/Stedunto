from .place import Place, Connection
from .location import Location
from Game.Heroes.Heroes.goblin import Goblin
import json


class PlaceNotFound(Exception):
    pass


class Map:
    def __init__(self, places, locations):
        self.locations = locations
        self.places = places

    def get_place_by_name(self, name):
        return Place.get_place_by_name(self.places, name)

    def get_place_by_loc_and_name(self, location_name, name):
        for place in self.places:
            if place.name == name and place.location.name == location_name:
                return place
        raise PlaceNotFound(f'Не нашлось локации с таким названием: {location_name}:{name}')

    def get_place_by_xname(self, xname='Location_name:place_name'):
        loc_name, place_name = xname.split(':')
        return self.get_place_by_loc_and_name(loc_name, place_name)

    @classmethod
    def create_from_json_file(cls, filename='Game/Locations/map.json'):
        with open(filename, encoding='utf-8') as file:
            map_data = json.load(file)

        locations = list(map(lambda loc_dict: Location(loc_dict['name']), map_data['locations']))
        locations_dict = {loc.name: loc for loc in locations}

        places = []
        for location_dict in map_data['locations']:
            for place_name in location_dict['places']:
                places.append(Place(place_name, location=locations_dict[location_dict['name']]))

        world_map = cls(places, locations)

        connections_dict = map_data['connections']
        for loc_name in connections_dict:
            connections_in_loc = connections_dict[loc_name]
            for connection_list in connections_in_loc:
                Connection.create_and_connect(
                    world_map.get_place_by_loc_and_name(loc_name, connection_list[0]),
                    world_map.get_place_by_loc_and_name(loc_name, connection_list[1])
                )
        return world_map


def old_build_map():
    locations_list = [
        Location('Статический лес'),
        Location('Динамический лес'),
        Location('Ванная площадь')
    ]
    locations = {loc.name: loc for loc in locations_list}

    places = [
        Place('Опушка', location=locations['Статический лес']),
        Place('Поляна', location=locations['Статический лес']),
        Place('Тропа', location=locations['Статический лес']),

        Place('Лесок', location=locations['Динамический лес']),
        Place('Тропина', location=locations['Динамический лес']),
        Place('Заросли', location=locations['Динамический лес']),

        Place('Рынок', location=locations['Ванная площадь']),
        Place('Аудиторная', location=locations['Ванная площадь']),
    ]
    places_dict = {place.name: place for place in places}

    connections = [
        ['Опушка', 'Поляна'],
        ['Опушка', 'Тропа'],
        ['Тропа', 'Поляна'],

        ["Лесок", "Тропина"],
        ["Тропина", "Заросли"],
        ["Заросли", "Лесок"],

        ["Рынок", "Аудиторная"],

        ["Тропа", "Тропина"],
        ["Рынок", "Опушка"]
    ]

    for row in connections:
        Connection.create_and_connect(places_dict[row[0]], places_dict[row[1]])

    zarosly = Place.get_place_by_name(places, 'Заросли')
    zarosly.add_hero(Goblin())

    for _ in range(3):
        Place.get_place_by_name(places, 'Лесок').add_hero(
            Goblin()
        )

    map_ = Map(places, locations_list)
    return map_


def build_map():
    return Map.create_from_json_file()
