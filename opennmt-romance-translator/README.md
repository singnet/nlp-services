[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# OpenNMT Romance Translator

This service uses [OpenNMT romance model](http://forum.opennmt.net/t/training-romance-multi-way-model/86)
to translate sentences accordingly to these language pairs:
 
- PT<->ES
- PT<->FR
- PT<->IT
- PT<->RO
- FR<->ES
- FR<->IT
- FR<->RO
- ES<->IT
- ES<->RO
- IT<->RO

Where:

- PT: Portuguese
- FR: French
- ES: Spanish
- IT: Italian
- RO: Romanian

It is part of our [NLP Services](https://github.com/singnet/nlp-services).

## Getting Started

### Requirements

- [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
- [Node 8+ w/npm](https://nodejs.org/en/download/)
- [Torch with LuaJIT](http://torch.ch/docs/getting-started.html)

### Development

Clone this repository:

```
$ git clone https://github.com/singnet/nlp-services.git
$ cd nlp-services/opennmt-romance-translator
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
   "DAEMON_END_POINT": "http://54.203.198.53:7076",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "snet",
   "SERVICE_ID": "opennmt-romance-translator",
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

Prepare folder structure (download models and OpenNMT files):
```
$ cd utils/
$ ./prepare_data.sh ./data
$ cd ..
```

Start the service and `SNET Daemon`:
```
$ python3 run_romance_translator_service.py
```

### Calling the service:

Inputs:

 - `gRPC method`: translate.
 - `source_lang`: the source language in which the sentences were written.
 - `target_lang`: target language that the sentences will be translated.
 - `sentences_url`: URL file with sentences to be translated.

Local (testing purpose):

```
$ python3 test_romance_translator_service.py
Endpoint (localhost:7003): 
Method (translate):
Source Language (pt): 
Target Language (it): 
Sentences URL (Example URL):

response:
translation:
sono favorevole alla relazione ripresa in esubero, che riconosce che le agenzie dell'unione europea di notizie sono state assegnate dal punto di vista della responsabilità della commissione.
in bielorussia, la democrazia e le loro istituzioni sono state prese dal punto di vista dell'unione europea.
indica anche l'orientamento dell'ordine del giorno recato, e l'obiettivo dell'unione europea, e gli obiettivi in collaborazione sono stati in collaborazione.
il recente risultato delle elezioni sono state dimostrate che il messaggio del g 20 divide a due campi.
signor presidente, vorrei ringraziare quest'aula per aver inserito l'ordine del giorno dell'ordine del giorno dell'ordine del giorno dell'ordine del giorno.
sono quando presenteremo i risultati che i cittadini europei si aspettano di non essere i risultati che i cittadini europei si aspettano di no, e ciò che dicono non è il consiglio, la commissione e il parlamento europeo.
sono in grado di richiedere la possibilità di richiedere un modo più informato e, di conseguenza, una forma più responsabile di responsabilità.
la base dell'eccezione dell'eccezione dell'insieme è stata data a un piano di sostituzione dell'insieme 15.000.
abbiamo constatato, con una certa inquietura, che le misure che alcuni stati membri stiano cercando di introdurre il risultato di una violazione della concorrenza non sono state introdotte dalle norme di concorrenza.
per quanto riguarda il contenuto della relazione goldstone, l'unione europea non può rimanere indifferente.
```

The service returns the output (translation) of the specific trained model.

For further instructions about the output of this service, check the [User's Guide](../docs/users_guide/opennmt-romance-translator.md).

Through SingularityNET (follow this [link](https://dev.singularitynet.io/tutorials/publish/) 
to learn how to publish a service and open a payment channel to be able to call it):

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0.00000001 54.203.198.53:7076 translate '{"source_lang": "pt", "target_lang": "fr", "sentences_url": "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_sentences.txt"}'
unspent_amount_in_cogs before call (None means that we cannot get it now):1

response:
translation:
par écrit. - (ro) je soutiens le rapport de l'année prochaine, qui reconnaît que les agences de notateurs de notateurs ont été faites à l'heure actuelle de l'assemblée et de la transparence.
par écrit. - compte tenu de l'union européenne et de ses instituteurs, il s'agit du bon nom de l'union européenne et de leurs instituteurs de la démocratie au belarus.
il s'agit également d'une fois de plus d'une partie de l'intermédiaire de l'assemblée et de l'objectif d'une coopération à l'encontre de l'argent 2008.
le récent résultat des électeurs démontre que le ppe s'est divisé en deux camps.
monsieur le président, je tiens à remercier cette assemblée pour l'assemblée d'avoir été inclus à l'ordre du jour de l'agence des marchés européens.
quand nous avons fait, quand nous avons déposé les résultats que les citoyens s'attendent à ne pas s'attendre à la légitimité et à la confiance de nos concitoyens et de la confiance.
j'ai donc besoin d'exiger la possibilité de consommateurs d'une façon plus informée et d'une façon plus responsable d'une manière plus responsable.
la base de l'intérêt de l'ordre du jour est très importante de l'importance de l'exception de l'importance de l'exception de l'union européenne et de l'exception de l'exception de l'union européenne.
nous constatons, avec une certaine inquiétude, une certaine inquiétude de l'heure actuelle, les mesures que certains états membres de l'ue tentent d'introduire une violation de la concurrence de la concurrence.
au cours du contenu du rapport de ce rapport, l'union européenne n'est pas indifférente.
```

Note that this translation was not good enough.

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)