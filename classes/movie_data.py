class MovieData():
    movieId = None

    def __init__(self, *args, **kwargs):
        movie = args[0] if args or kwargs.get("movie") else ""
        if movie == "":
            self.init("")
        else:
            self.init(movie)

    def init(self, movie):
        self.movieId = movie

    def is_active(self):
        return self.movieId != ""

    def movie_status_key(self):
        if self.is_active():
            return self.movieId + '_status'
        return ""

    def movie_start_key(self):
        if self.is_active():
            return self.movieId + '_play'
        return ""

    def movie_stop_key(self):
        if self.is_active():
            return self.movieId + '_stop'
        return ""

    def movie_pause_key(self):
        if self.is_active():
            return self.movieId + '_pause'
        return ""
