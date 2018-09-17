# Named Entity Recognition Services

#### This repository contains a named entity recognition service.

##### Avaliable methods of sentiment analysis:

- Tagger - Taggning sentences.
- Tokenizer - Tokenize sentences.
- Chunker - Chunk sentences.

WIP = Work in Progress

## Deployment:

#### Deploy a new service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/named_entity_recognition/named_entity_recognition/deploy/deploy_service.sh | bash
```

#### Update a running service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/named_entity_recognition/named_entity_recognition/deploy/update_service.sh | bash
```

#### Remove a running service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/named_entity_recognition/named_entity_recognition/deploy/remove_service.sh | bash
```

#### Start a running container service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/named_entity_recognition/named_entity_recognition/deploy/start_running_service.sh | bash
```

#### Stop a running container service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/named_entity_recognition/named_entity_recognition/deploy/stop_running_service.sh | bash
```

## Usage:

### Tagger:
#### Method signature: 
tag()

To use this method, you must build the input message as shown below:

#### Input Message Attributes:
- value - Base64 text

#### Service call example:
```
$ snet client call tag '{"value": "VGVzdGluZyBzZXJ2aWNl"}' --no-confirm
```

#### Output example:
The result will be a base64 text including the tagged sentence.

Output example:

```
$ ...

```

### Tokenizer:
#### Method signature: 
tag()

To use this method, you must build the input message as shown below:

#### Input Message Attributes:
- value - Base64 text

#### Service call example:
```
$ snet client call tokenize '{"value": "VGVzdGluZyBzZXJ2aWNl"}' --no-confirm
```

#### Output example:
The result will be a base64 text including the tokenized sentence.

Output example:

```
$ ...

```

### Chuncker:
#### Method signature: 
tag()

To use this method, you must build the input message as shown below:

#### Input Message Attributes:
- value - Base64 text

#### Service call example:
```
$ snet client call chunk '{"value": "VGVzdGluZyBzZXJ2aWNl"}' --no-confirm
```

#### Output example:
The result will be a base64 text including the chuncked sentence.

Output example:

```
$ ...

```