[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# CNTK Language Understanding

This service uses [CNTK Language Understanding](https://cntk.ai/pythondocs/CNTK_202_Language_Understanding.html)
to process text and offer two options: slot tagging and intent classification.

It is part of our [NLP Services](https://github.com/singnet/nlp-services).

## Getting Started

### Requirements

- [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
- [Node 8+ w/npm](https://nodejs.org/en/download/)

### Development

Clone this repository:

```
$ git clone https://github.com/singnet/nlp-services.git
$ cd nlp-services/cntk-language-understanding
```

### Running the service:

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service 
(check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`).

```
{
   "DAEMON_END_POINT": "DAEMON_HOST:DAEMON_PORT",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "SERVICE_GRPC_HOST:SERVICE_GRPC_PORT",  
   "ORGANIZATION_ID": "ORGANIZATION_ID",
   "SERVICE_ID": "SERVICE_ID",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
            "TYPE": "stdout"
           }
   }
}
```

For example:

```
$ cat snetd.config.json
{
   "DAEMON_END_POINT": "http://54.203.198.53:7075",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "snet",
   "SERVICE_ID": "cntk-language-understanding",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
           "TYPE": "stdout"
           }
   }
}
```
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
$ python3 run_language_understanding_service.py
```

### Calling the service:

Inputs:

 - `gRPC method`: slot_tagging or intent.
 - `train_ctf_url`: URL of the training file.
 - `test_ctf_url`: URL of the test file.
 - `query_wl_url`: URL of the query file.
 - `slots_wl_url`: URL of the slots file.
 - `intent_wl_url`: URL of the intent file.
 - `vocab_size`: the size of vocabulary.
 - `num_labels`: number of slot labels.
 - `num_intents`: number of intent labels.
 - `sentences_url`: URL of the sentences file.

Local (testing purpose):

```
$ python3 test_language_understanding_service.py
Endpoint (localhost:7003): 
Method (slot_tagging|intent): slot_tagging
sentences (URL, one per line):
train_ctf_url (ATIS Link): 
test_ctf_url (ATIS Link): 
query_wl_url (ATIS Link): 
slots_wl_url (ATIS Link): 
intent_wl_url (ATIS Link): 
vocab_size (943): 
num_labels (129): 
num_intents (26):

response:
output URL: http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Output/684bb98e0ef1537c1b7d.txt
model  URL: http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Output/684bb98e0ef1537c1b7d.model
```

The service returns 2 URLs. First one is the output of the trained model for the given sentences.
The second is the trained model itself.

For further instructions about the output of this service, check the [User's Guide](../docs/users_guide/cntk-language-understanding.md).

Through SingularityNET (follow this [link](https://dev.singularitynet.io/tutorials/publish/) 
to learn how to publish a service and open a payment channel to be able to call it):

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0.00000001 54.203.198.53:7075 slot_tagging '{"train_ctf_url": "https://github.com/Microsoft/CNTK/blob/release/2.6/Tutorials/SLUHandsOn/atis.train.ctf?raw=true", "test_ctf_url": "https://github.com/Microsoft/CNTK/blob/release/2.6/Tutorials/SLUHandsOn/atis.test.ctf?raw=true", "query_wl_url": "https://github.com/Microsoft/CNTK/blob/release/2.6/Examples/LanguageUnderstanding/ATIS/BrainScript/query.wl?raw=true", "slots_wl_url": "https://github.com/Microsoft/CNTK/blob/release/2.6/Examples/LanguageUnderstanding/ATIS/BrainScript/slots.wl?raw=true", "intent_wl_url": "https://github.com/Microsoft/CNTK/blob/release/2.6/Examples/LanguageUnderstanding/ATIS/BrainScript/intent.wl?raw=true", "vocab_size": 943, "num_labels": 129, "num_intents": 26, "sentences_url": "http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Example/sentences.txt"}'
unspent_amount_in_cogs before call (None means that we cannot get it now):1

response:
output URL: http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Output/684bb98e0ef1537c1b7d.txt
model  URL: http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Output/684bb98e0ef1537c1b7d.model
```

The input sentences file content:
```
BOS flights from new york to seattle by delta airlines EOS
BOS how much is the ticket to washington from san francisco EOS
BOS departures from los angeles to san diego EOS
BOS what is the name of the main airport in chicago EOS
BOS i want to book a flight from miami to atlanta by american airlines EOS
```

The output file content:
```
0: BOS flights from new york to seattle by delta airlines EOS
0: [('BOS', 'O'), ('flights', 'O'), ('from', 'O'), ('new', 'B-fromloc.city_name'), ('york', 'I-fromloc.city_name'), ('to', 'O'), ('seattle', 'B-toloc.city_name'), ('by', 'O'), ('delta', 'B-airline_name'), ('airlines', 'I-airline_name'), ('EOS', 'O')]
1: BOS how much is the ticket to washington from san francisco EOS
1: [('BOS', 'O'), ('how', 'O'), ('much', 'O'), ('is', 'O'), ('the', 'O'), ('ticket', 'O'), ('to', 'O'), ('washington', 'B-toloc.city_name'), ('from', 'O'), ('san', 'B-fromloc.city_name'), ('francisco', 'I-fromloc.city_name'), ('EOS', 'O')]
2: BOS departures from los angeles to san diego EOS
2: [('BOS', 'O'), ('departures', 'O'), ('from', 'O'), ('los', 'B-fromloc.city_name'), ('angeles', 'I-fromloc.city_name'), ('to', 'O'), ('san', 'B-toloc.city_name'), ('diego', 'I-toloc.city_name'), ('EOS', 'O')]
3: BOS what is the name of the main airport in chicago EOS
3: [('BOS', 'O'), ('what', 'O'), ('is', 'O'), ('the', 'O'), ('name', 'O'), ('of', 'O'), ('the', 'O'), ('main', 'O'), ('airport', 'O'), ('in', 'B-city_name'), ('chicago', 'O')]
4: BOS i want to book a flight from miami to atlanta by american airlines EOS
4: [('BOS', 'O'), ('i', 'O'), ('want', 'O'), ('to', 'O'), ('book', 'O'), ('a', 'O'), ('flight', 'O'), ('from', 'O'), ('miami', 'B-fromloc.city_name'), ('to', 'O'), ('atlanta', 'B-toloc.city_name'), ('by', 'O'), ('american', 'B-airline_name'), ('airlines', 'I-airline_name'), ('EOS', 'O')]
```

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)