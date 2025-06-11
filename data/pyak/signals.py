"""Send and receive signals."""


@dataclass
class Signal:
    name: str
    payload: any = None


def signal(session_id: str, name: str, payload: any=None) ->None:
    """Signal a session."""
    ...


def next_signal(name: (str | list[str]), *, timeout: (timedelta | int |
    float)=None) ->(Signal | None):
    """Get the next signal."""
    ...
