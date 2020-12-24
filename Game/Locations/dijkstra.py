from .place import Place
from typing import Optional


class PlaceNode:
    def __init__(self, place, prev=None):
        self.place: Place = place
        self.prev: Optional[PlaceNode] = prev


class Way:
    def __init__(self, last_place_node):
        self.last_place_node: PlaceNode = last_place_node
        self._places_list = None

    def add(self, place_node: PlaceNode):
        place_node.prev = self.last_place_node
        self.last_place_node = place_node

    def create_extension(self, place_node):
        place_node.prev = self.last_place_node
        return Way(place_node)

    def transform_to_list(self):
        lst = []
        node = self.last_place_node
        while node is not None:
            lst.insert(0, node.place)
            node = node.prev
        return lst

    @property
    def places_list(self):
        if not self._places_list:
            self._places_list = self.transform_to_list()
        return self._places_list


class DijkstraBubble:
    way: Way
    distance: int

    def __init__(self, way, distance):
        self.way = way
        self.distance = distance

    def create_extension(self, place: Place, d_distance: int):
        way = self.way.create_extension(PlaceNode(place))
        return DijkstraBubble(way, self.distance + d_distance)


class SuperDijkstra:
    instance = None
    bubbles = []

    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return cls()

    def find_shortest_way(self, place1: Place, place2: Place):
        for place in Place.all_places:
            place.approved = False

        bubble = DijkstraBubble(Way(PlaceNode(place1)), 0)
        place1.approved = True
        self.bubbles = [bubble]
        approved_bubble = bubble

        while not place2.approved:
            self.bubbles.remove(approved_bubble)
            approved_place = approved_bubble.way.last_place_node.place
            for place, distance in approved_place.adjacent_places_and_distances:
                if not place.approved:
                    new_bubble = approved_bubble.create_extension(place, distance)
                    self.aggressive_append_to_bubbles(new_bubble)

            min_bubble = self.find_min_bubble()
            min_bubble.way.last_place_node.place.approved = True
            approved_bubble = min_bubble

        for bubble in self.bubbles:
            if bubble.way.last_place_node.place is place2:
                return bubble.way

    def aggressive_append_to_bubbles(self, new_bubble: DijkstraBubble):
        i = len(self.bubbles) - 1
        result = False
        while i >= 0:
            bubble = self.bubbles[i]
            if bubble.way.last_place_node.place is new_bubble.way.last_place_node.place:
                if new_bubble.distance < bubble.distance:
                    self.bubbles[i] = new_bubble
                elif new_bubble.distance == bubble.distance:
                    self.bubbles.append(new_bubble)
                result = True
                break
            i -= 1
        if not result:
            self.bubbles.append(new_bubble)

    def find_min_bubble(self):
        min_distance = float('inf')
        min_bubble = None
        for bubble in self.bubbles:
            if bubble.distance < min_distance:
                min_distance = bubble.distance
                min_bubble = bubble
        return min_bubble

