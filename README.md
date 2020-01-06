## Installation: 

```
gunzip bitdiscovery.tar.gz
tar -xvf bitdiscovery.tar
cd bitdiscovery
sudo python3 setup.py install
```


## Running it Make sure you update the keys to your keys:
```
tenable-bitdiscovery --tio-access-key <TENABLE_ACCESS_KEY_GOES_HERE> --tio-secret-key <TENABLE_SECRET_KEY_GOES_HERE> --bd-api-key <BITDISCOVERY_API_KEY_GOES_HERE>

```

## Add the following to make it automatically run out of cron job. Make sure you update the keys:

```
0       0      *       *       *	path.to/tenable-bitdiscovery --tio-access-key <TENABLE_ACCESS_KEY_GOES_HERE> --tio-secret-key <TENABLE_SECRET_KEY_GOES_HERE> --bd-api-key <BITDISCOVERY_API_KEY_GOES_HERE>

```
