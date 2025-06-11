"""AutoKitteh Event class"""


@dataclass
class Event:
    """AutoKitteh Event as passed to entrypoints."""
    data: AttrDict
    session_id: str
