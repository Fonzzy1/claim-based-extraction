
class Source():
    def __init__(self, url):
        self.url = url
        self.objects=[]

    def get_urls(self):
        pass

class AudioSource(Source):
    def __init__(self, url):
        super().__init__(url)

class TextSource(Source):
    def __init__(self, url):
        super().__init__(url)

class VideoSource(Source):
    def __init__(self, url):
        super().__init__(url)










