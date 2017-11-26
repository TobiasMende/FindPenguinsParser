class Post:
    def __init__(self):
        self.id = None
        self.bookmark = None
        self.date = None
        self.time = None
        self.title = None
        self.text = None
        self.images = []

    def __str__(self):
        return 'Post({}, {}, {}, {}, {}, {}, {})'.format(self.id, self.bookmark, self.date, self.time, self.title,
                                                         self.text, self.images)
