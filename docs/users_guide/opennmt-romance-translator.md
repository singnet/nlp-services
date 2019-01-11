[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../assets/singnet-logo.jpg?raw=true 'SingularityNET')

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

### Welcome

The service receives as input sentences, a source language (which the sentences were written) and target language 
that the sentences will be translated. Using the multi-way [OpenNMT Model](http://opennmt.net/Models/), isolated for
every language pair, the service gets the sentences, breaks them into tokens and than feed the target model.
The model output translated tokens that are put together to become the output of service (translated sentences).

### What’s the point?

The service process input sentences and returns a translation, accordingly to input parameters. 

The model trained for this service has the following parameters:

- 4 layers
- 1000 hidden size
- 600 embedding size
- BRNN 32K shared BPE

Note that each language pair has its own trained model, so to use the full service you'll need to 
download all 10 models (~2.7Gb).

### How does it work?

The user must provide the following inputs:

 - `gRPC method`: translate.
 - `source_lang`: the source language in which the sentences were written.
 - `target_lang`: target language that the sentences will be translated.
 - `sentences_url`: URL file with sentences to be translated.

The output format is:
 - `translation`: sentences translated by the specific model.
 
You can use this service from [SingularityNET DApp](http://beta.singularitynet.io/).

You can also call the service from SingularityNET CLI (`snet`).

Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0.00000001 54.203.198.53:7076 translate '{"source_lang": "pt", "target_lang": "it", "sentences": "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_sentences.txt"}'
unspent_amount_in_cogs before call (None means that we cannot get it now):1

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

### What to expect from this service?

Inputs:

 - `gRPC method`: translate
 - `source_lang`: "es"
 - `target_lang`: "fr"
 - `sentences_url`: "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_one_sentence.txt"

Response:

```
response:
translation:
je suis une personne très heureuse.
```

Inputs:

 - `gRPC method`: translate
 - `source_lang`: "es"
 - `target_lang`: "it"
 - `sentences_url`: "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_one_sentence.txt"

Response:

```
response:
translation:
io sono una persona molto felice.
```

Inputs:

 - `gRPC method`: translate
 - `source_lang`: "es"
 - `target_lang`: "pt"
 - `sentences_url`: "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_one_sentence.txt"

Response:

```
response:
translation:
eu sou uma pessoa muito feliz.
```

Inputs:

 - `gRPC method`: translate
 - `source_lang`: "es"
 - `target_lang`: "ro"
 - `sentences_url`: "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_one_sentence.txt"

Response:

```
response:
translation:
eu sunt o persoană foarte fericită.
```