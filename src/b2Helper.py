import Box2D


class B2Helper:
    def __init__(self, world: Box2D.b2World, ppm: int):
        self.PPM = ppm
        self.world = world

    def create_edge(self, w: int, h: int, x: int, y: int) -> Box2D.b2EdgeShape:
        x = x / self.PPM
        y = y / self.PPM
        w = w / self.PPM
        h = h / self.PPM
        edge = Box2D.b2EdgeShape(vertices=[(x, y), (w + x, h + y)])
        return edge

    def create_polygon(self, x: float, y: float, w: float, h: float) -> Box2D.b2PolygonShape:
        x = x / self.PPM
        y = y / self.PPM
        w = w / self.PPM
        h = h / self.PPM
        return Box2D.b2PolygonShape(vertices=[
            (x, y), (x + w, y), (x + w, y + h), (x, y + h)])

    def add_box_to_world(self, polygon: Box2D.b2PolygonShape, position: Box2D.b2Vec2, mass: float,
                         linear_damping: float,
                         friction: float) -> None:
        box = self.world.CreateDynamicBody(position=position, shapes=polygon)
        box.mass = mass
        box.linearDamping = linear_damping
        box.fixtures[0].friction = friction
