from restfly.endpoint import APIEndpoint
from restfly.iterator import APIIterator

class InventoryIterator(APIIterator):
    _id = '0000000000' #Placeholder for the first record
    _limit = 1000 #As large as 10000 but may cause timeout issues

    def _get_page(self):
        if not self._query.__contains__('after'):
          self._query['after'] = self._id

        self._query['limit'] = self._limit
        self._query['columns'] = 'bd.original_hostname,bd.hostname,bd.record_type,bd.ip_address,id'
        resp = self._api.post('inventory',
            params=self._query, json=self._f).json()
        for asset in resp['assets']:
            self._query['after'] = asset['id']
        self.page = resp['assets']


class InventoryAPI(APIEndpoint):
    def list(self, *search, size=1000):
        '''
        A simple inventory listing method.

        Args:
            search (tuple):
                A 3-part tuple detailing what kind of search to use.  For
                example, a tuple of
                ``('bd.original_hostname', 'ends with', '')``
            size (int, optional):
                The size of the page to request to the BitDiscovery API.  If
                left unspecified, the default is 1000.
            total (int, optional):

        Returns:
            obj:`InventoryIterator`:
                the iterator object.
        '''
        return InventoryIterator(self._api,
            _limit=size,
            _query={'sortorder': 'true', 'inventory': 'false'},
            _f=[{'column': s[0], 'type': s[1], 'value': s[2]} for s in search]
        )
