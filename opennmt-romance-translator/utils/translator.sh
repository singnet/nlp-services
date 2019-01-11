#!/usr/bin/env bash
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ]
  then
    echo "Invalid arguments: ./translator.sh DATA_FOLDER SOURCE_LANGUAGE TARGET_LANGUAGE INPUT_SENTENCES_FILE OUTPUT_SENTENCES_FILE"
    exit 1
fi

file="$1/$2$3.bpe32000"
if [ -f "$file" ]
then
	th tools/tokenize.lua -case_feature -joiner_annotate -nparallel 4 -bpe_model $1/$2$3.bpe32000 < $4 > $4.tok
else
    file="$1/$3$2.bpe32000"
    if [ -f "$file" ]
    then
	    th tools/tokenize.lua -case_feature -joiner_annotate -nparallel 4 -bpe_model $1/$3$2.bpe32000 < $4 > $4.tok
	else
	    echo "BPE ($file) not found, exiting.."
	    exit 1
	fi
fi

perl -i.bak -pe "s//__opt_tgt_$3\xEF\xBF\xA8N /" $4.tok

file="$1/model_$2$3.t7"
if [ -f "$file" ]
then
	th translate.lua -replace_unk -model $1/model_$2$3.t7 -src $4.tok -output $5.tok -gpuid 1
else
    file="$1/model_$3$2.t7"
    if [ -f "$file" ]
    then
	    th translate.lua -replace_unk -model $1/model_$3$2.t7 -src $4.tok -output $5.tok -gpuid 1
	else
	    echo "Model ($file) not found, exiting.."
	    exit 1
	fi
fi

th tools/detokenize.lua -nparallel 4 < $5.tok > $5
rm *.tok*