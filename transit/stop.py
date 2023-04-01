from dataclasses import dataclass, field

@dataclass
class Stop:
    name: str
    id: str = ""
    route_associations: list = field(default_factory=list)

    def is_associated_with_multiple_routes(self):
        return len(self.route_associations) > 1