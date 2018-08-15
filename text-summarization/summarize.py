### Basic summarizer to directly use untokenized text. Since apparently that's too hard to provide as an example.
from services.onmt_utils import stanford_ptb_detokenizer, stanford_ptb_tokenizer, summary

if __name__ == "__main__":

    with open('example_article.txt', 'r') as f:
        text = f.read()
    tokens = stanford_ptb_tokenizer(text)
    score, p = summary(tokens)
    summary = p[0].replace(' <t>', '').replace(' </t>', '')
    print(score, summary)

    print(stanford_ptb_detokenizer(summary))