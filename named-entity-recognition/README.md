[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# Named Entity Recognition Services

This repository contains a SingularityNET service to recognize entities inside sentences.
 
It is part of our [NLP Services](https://github.com/singnet/nlp-services).

## Getting Started

### Requirements

- [Python 3.6+](https://www.python.org/downloads/)
- [OpenJDK 8+](https://openjdk.java.net/install/)


### Development

Clone this repository:

```
$ git clone https://github.com/singnet/nlp-services.git
$ cd named-entity-recognition
```

### Running the service:

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service 
(check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`) according to the following example and replace to your service settings.

```
$ cat snetd.kovan.config.json
{
  "daemon_end_point": "http://54.203.198.53:7012",
  "ethereum_json_rpc_endpoint": "https://kovan.infura.io",
  "ipfs_end_point": "http://ipfs.singularitynet.io:80",
  "registry_address_key": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
  "passthrough_enabled": true,
  "passthrough_endpoint": "http://localhost:7013",
  "organization_id": "snet",
  "service_id": "named-entity-recognition",

  "payment_channel_storage_server": {
    "id": "storage-kovan",
    "host": "127.0.0.1",
    "client_port": 2379,
    "peer_port": 2380,
    "token": "unique-token",
    "cluster": "storage-kovan=http://127.0.0.1:2380",
    "data_dir": "etcd/storage-data-dir-kovan.etcd",
    "enabled": true
  },

  "payment_channel_storage_client": {
    "connection_timeout": "5s",
    "request_timeout": "3s",
    "endpoints": ["http://127.0.0.1:2379"]
  },

  "log": {
    "level": "debug",
    "output": {
      "current_link": "./snetd-kovan.log",
      "file_pattern": "./snetd-kovan.%Y%m%d.log",
      "rotation_count": 0,
      "rotation_time_in_sec": 86400,
      "type": "file"
    }
  }
}
```
For more details about this settings file, please click [here](https://github.com/singnet/snet-daemon). 

Install all dependencies:
```
$ pip3 install -r requirements.txt
```

Generate the gRPC codes:
```
$ sh buildproto.sh
```

Start the service and `SNET Daemon`:
```
$ python3 run_service.py
```

### Calling the service:

In another terminal, test your service with:
```
$ cd tests
$ python3 run_test_service.py

```

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Glauter Lemos** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)