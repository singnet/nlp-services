[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](docs/assets/singnet-logo.jpg 'SingularityNET')

[![CircleCI](https://circleci.com/gh/singnet/nlp-services.svg?style=svg)](https://circleci.com/gh/singnet/nlp-services)

# Natural Language Processing Services

This repository contains a number of [SingularityNET](http://singularitynet.io) services for understanding or manipulating natural language.

Each service has it's own README.md with full details:

[HTML User's Guide Hub](https://singnet.github.io/nlp-services/)

## Getting Started

For more details on how to publish and test a service, select it from the list below:

### Services:

- [CNTK Language Understanding](cntk-language-understanding/) 
([User's Guide](docs/users_guide/cntk-language-understanding.md)) - CNTK recurrent LSTM network to process text for slot tagging and intent classification
[[Reference](https://cntk.ai/pythondocs/CNTK_202_Language_Understanding.html)].
- [Named Entity Recognition](named-entity-recognition/) - Recognize entities like PERSON, ORGANIZATION and LOCATION inside texts.
- [OpenNMT Romance Translator](opennmt-romance-translator/) - OpenNTM model to translate romance languages [[Reference](http://forum.opennmt.net/t/training-romance-multi-way-model/86)].
- [Sentiment Analysis](sentiment-analysis/) - Sentiment Analysis of sentences in different formats, please check the service home page out.
- [Text Summarization](text-summarization/) - Create a summary for a piece of text. Currently limited to the domain of news articles.
- [Translation](translation/) - Convert between language pairs. Currently limited to English <-> German.

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) 
before submitting an issue. If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Artur Gontijo** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)
* **Glauter Lemos** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)
* **Joel Pitt** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)

## Licenses

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Each service is licensed as followed:

- cntk-language-understanding - [MIT License](https://github.com/Microsoft/CNTK/blob/master/LICENSE.md)
- opennmt-romance-translator - [MIT License](https://github.com/OpenNMT/OpenNMT/blob/master/LICENSE.md)