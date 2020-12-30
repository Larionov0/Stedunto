from .place import Place, Connection
from .location import Location
from Game.Heroes.Heroes.goblin import Goblin


def build_map():
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

    zarosly = Place.get_place_by_name('Заросли')
    zarosly.heroes.append(
        Goblin()
    )

    return places
