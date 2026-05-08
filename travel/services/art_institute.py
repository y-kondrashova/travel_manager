import requests

from .exceptions import (
    ExternalAPIError,
    ArtworkNotFoundError,
)


class ArtInstituteService:

    BASE_URL = "https://api.artic.edu/api/v1/artworks"

    @classmethod
    def get_artwork(cls, artwork_id):

        url = f"{cls.BASE_URL}/{artwork_id}"

        try:
            response = requests.get(url, timeout=5)

        except requests.RequestException:
            raise ExternalAPIError("Art Institute API unavailable.")

        if response.status_code == 404:
            raise ArtworkNotFoundError("Artwork does not exist.")

        if response.status_code != 200:
            raise ExternalAPIError("Unexpected Art Institute API error.")

        data = response.json().get("data")

        if not data:
            raise ArtworkNotFoundError("Artwork does not exist.")

        return {
            "external_id": data["id"],
            "title": data["title"],
        }

    @classmethod
    def search_artworks(cls, query):

        response = requests.get(
            f"{cls.BASE_URL}/search",
            params={"q": query},
            timeout=5,
        )

        response.raise_for_status()

        return response.json()
