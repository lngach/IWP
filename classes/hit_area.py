from .movie_data import MovieData


class HitArea(MovieData):
    active = None
    top = None
    bottom = None
    left = None
    right = None

    def __init__(self, *args, **kwargs):
        top = args[0] if args or kwargs.get("top") else 0.0
        bottom = args[1] if args or kwargs.get("bottom") else 0.0
        left = args[2] if args or kwargs.get("left") else 0.0
        right = args[3] if args or kwargs.get("right") else 0.0
        movie = args[4] if args or kwargs.get("movie") else ""
        self.init(top, bottom, left, right, movie)

    def init(self, top, bottom, left, right, movie):
        super().init(movie)
        self.active = True
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def is_active(self):
        return super().is_active() and self.active
