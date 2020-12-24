class Connection:
    def __init__(self, places=None):
        if places is None:
            places = []
        self.places = places

    def add_place(self, place):
        self.places.append(place)
        if len(self.places) > 2:
            raise Exception('Too much places for 1 Connection')

    def connect_2_places(self, place1, place2):
        place1.add_connection(self)
        place2.add_connection(self)

    @classmethod
    def create_and_connect(cls, place1, place2):
        connection = cls()
        connection.connect_2_places(place1, place2)
        return connection

    def get_other_place(self, place):
        if self.places[0] is place:
            return self.places[1]
        return self.places[0]

    def __str__(self):
        l = len(self.places)
        if l == 2:
            return f"Connection: {self.places[0].name} - {self.places[1].name}"
        elif l == 1:
            return f"Connection: {self.places[0].name} - None"
        else:
            return f"Connection: None - None"


class Place:
    all_places = []

    def __init__(self, name, id_=None, location=None, heroes=None, connections=None):
        if id_ is None:
            id_ = Place.find_max_id() + 1

        self.id = id_
        self.name = name

        if heroes is None:
            heroes = []
        if connections is None:
            connections = []
        self.heroes = heroes
        self.connections = connections

        self.location = location
        if location:
            location.add_place(self, False)
        self.approved = False
        Place.all_places.append(self)

    @classmethod
    def find_max_id(cls):
        m = 0
        for place in cls.all_places:
            if place.id > m:
                m = place.id
        return m

    def add_connection(self, connection: Connection):
        self.connections.append(connection)
        connection.add_place(self)

    @property
    def adjacent_places(self):
        for connection in self.connections:
            yield connection.get_other_place(self)

    @property
    def adjacent_places_list(self):
        return list(self.adjacent_places)

    def add_hero(self, hero):
        self.heroes.append(hero)
        hero.place = self

    def remove_hero(self, hero):
        self.heroes.remove(hero)
        hero.place = None

    def __repr__(self):
        return f"{self.name} ({self.location.name})"
