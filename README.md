# BitDiscovery to Tenable.io asset importer

This script will import the assets discovered from BitDiscovery and import them into Tenable.io's asset model.

## Prerequisites

* BitDiscovery API Key
* Tenable.io API keys: [How to get API Keys for Tenable.io][tio_api_keys]
* Python 3 installed with pip.

## Installation: 

```
sudo pip install .
```

## Options

```
Usage: tenable-bitdiscovery [OPTIONS]

  BitDiscovery -> Tenable.io Asset Importer

Options:
  --tio-access-key TEXT     Tenable.io Access Key
  --tio-secret-key TEXT     Tenable.io Secret Key
  -b, --batch-size INTEGER  Export/Import Batch Sizing
  --bd-api-key TEXT         BitDiscovery API Key
  -v, --verbose             Logging Verbosity
  --help                    Show this message and exit.
```

## Usage

Running the script once installed is a simple matter of passing the require parameters so that the script can authenticate to both systems:

```
tenable-bitdiscovery \
  --tio-access-key {TENABLE.IO_ACCESS_KEY} \
  --tio-secret-key {TENABLE.IO_SECRET_KEY} \
  --bd-api-key {BITDISCOVERY_API_KEY}
```

Running the script automatically on a schedule is also quite simple.  All you need to do is add the appropriate cronjob:

```
0 0 * * *	/path.to/tenable-bitdiscovery --tio-access-key {TENABLE.IO_ACCESS_KEY} --tio-secret-key {TENABLE.IO_SECRET_KEY} --bd-api-key {BITDISCOVERY_API_KEY}
```


[tio_api_keys]: https://docs.tenable.com/tenableio/vulnerabilitymanagement/Content/Settings/GenerateAPIKey.htm
