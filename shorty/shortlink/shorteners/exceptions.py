class ShortenerException(Exception):
    pass


class ShorteningProviderRequestException(ShortenerException):
    pass


class InvalidShorteningProviderResponse(ShorteningProviderRequestException):
    pass


class ShorteningProviderTimeout(ShorteningProviderRequestException):
    pass
