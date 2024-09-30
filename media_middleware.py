import os
from whitenoise.middleware import WhiteNoise
from django.conf import settings

class MediaWhiteNoise(WhiteNoise):
    def __init__(self, application, root=None, **kwargs):
        self.media_root = root or settings.MEDIA_ROOT
        super().__init__(application, root=root, **kwargs)

    def add_files(self, *args, **kwargs):
        # Call parent method to add static files
        super().add_files(*args, **kwargs)
        
        # Now add media files
        if self.media_root:
            self.add_files(self.media_root, prefix=settings.MEDIA_URL)