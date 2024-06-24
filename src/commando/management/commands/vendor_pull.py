import requests
from helpers import download_to_local

from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings


STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

VENDOR_STATICFILES = {
        "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
        "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    }

class Command(BaseCommand):    

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading Vendor static files")
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(f"failed to download {url}")
            print(name, url, out_path)
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(self.style.SUCCESS('successfuly updated vendor files'))
        else:
            self.stdout.write(self.style.WARNING('some files were not updated'))