from abc import ABC, abstractmethod

__all__ = (
    'Shortener',
)


class Shortener(ABC):
    @abstractmethod
    def shorten(self, long_url: str) -> str:
        """
        Shorten a given `long_url`.

        :raises: shorty.shortlink.shorteners.exceptions.ShortenerException: If error occurred during shortening.
        :param long_url: Long url to shorten.
        :return: Short url pointing to a given `long_url`.
        """
        pass
