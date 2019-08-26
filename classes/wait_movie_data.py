from .movie_data import MovieData


class WaitMovieData(MovieData):

    wait_time = None

    def __init__(self, *args, **kwargs):
        time = args[0] if args or kwargs.get("time") else 0
        movie = args[1] if args or kwargs.get("movie") else ''
        self.init(time, movie)

    def init(self, time, movie):
        super().init(movie)
