# -*- coding: utf-8 -*-
'''
MIT License

Copyright (c) 2019 Tenable Network Security, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from tenable.io import TenableIO
from .bitdiscovery import BitDiscovery
from tenable_bitdiscovery import __version__
import click, logging


@click.command()
@click.option('--tio-access-key',
    envvar='TIO_ACCESS_KEY', help='Tenable.io Access Key')
@click.option('--tio-secret-key',
    envvar='TIO_SECRET_KEY', help='Tenable.io Secret Key')
@click.option('--batch-size', '-b', 'tio_batch_size',
    envvar='BATCH_SIZE', default=1000, type=click.INT,
    help='Export/Import Batch Sizing')
@click.option('--bd-api-key', envvar='BITDISCOVERY_API_KEY',
    help='BitDiscovery API Key')
@click.option('--verbose', '-v', envvar='VERBOSITY', default=0,
    count=True, help='Logging Verbosity')
def cli(tio_access_key, tio_secret_key, tio_batch_size, bd_api_key, verbose):
    '''
    BitDiscovery -> Tenable.io Asset Importer
    '''
    # Setup the logging verbosity.
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose > 1:
        logging.basicConfig(level=logging.DEBUG)

    # Initiate the API modules
    tio = TenableIO(
        access_key=tio_access_key,
        secret_key=tio_secret_key,
        vendor='Tenable',
        product='BitDiscovery',
        build=__version__
    )
    bd = BitDiscovery(bd_api_key)

    # iterate over the result set.  When the cache reaches the appropriate size,
    # then import the data into Tenable and reset the cache.
    cache = list()
    logging.info('Initiating BitDiscovery Inventory Query')
    assets = bd.inventory.list(('bd.original_hostname', 'ends with', ''))
    for asset in assets:
        thehostname = ''
        if asset.get('bd.original_hostname') is None:
          thehostname = asset.get('bd.hostname')
        else:
          thehostname = asset.get('bd.original_hostname')
 
        if thehostname and asset.get('bd.record_type') in ['A', 'AAAA', 'PTR']:
            logging.debug('Adding {} Record for {} with address of {}'.format(
                asset.get('bd.record_type'),
                thehostname,
                asset.get('bd.ip_address')
            ))

            # generate the asset item.  If the IP Address is a IPv6 Address,
            # then we need to populate the ipv6 field, otherwise use the ipv4
            # field.
            item = {'fqdn': [thehostname]}
            if asset.get('bd.record_type') == 'AAAA':
                item['ipv6'] = [asset.get('bd.ip_address'),]
            else:
                item['ipv4'] = [asset.get('bd.ip_address'),]

            # Add the item to the cache.
            if item not in cache:
                cache.append(item)

        # Once the cache reaches the batch size, we will then pass the cache on
        # to the asset ingest API and then clear the cache.
        if len(cache) >= tio_batch_size:
            logging.info(
                'Sending {} assets into Tenable.io'.format(len(cache)))
            tio.assets.asset_import('Bit Discovery', *cache)
            cache = list()

    # As there are likely a few remaining items in the cache, we will want to
    # pass those on to the asset ingest API and drain the cache out.
    logging.info(
        'Draining the cache of {} assets into Tenable.io'.format(len(cache)))
    tio.assets.asset_import('Bit Discovery', *cache)
    logging.info(
        'Completed importing {} assets into Tenable.io'.format(assets.count))
