from restfly.session import APISession
from tenable_bitdiscovery import __version__
from .inventory import InventoryAPI


class BitDiscovery(APISession):
    _url = 'https://bitdiscovery.com/api/1.0'
    _vendor = 'BitDiscovery'
    _product = 'BitDiscovery'
    _build = __version__

    def __init__(self, api_key, **kwargs):
        self._api_key = api_key
        super(BitDiscovery, self).__init__(**kwargs)

    def _build_session(self, **kwargs):
        super(BitDiscovery, self)._build_session(**kwargs)
        self._session.headers.update({
            'Authorization': self._api_key
        })

    @property
    def inventory(self):
        return InventoryAPI(self)
