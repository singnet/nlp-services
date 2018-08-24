registry = {
    'translate_server': {
        'grpc': 6008,
        'jsonrpc': 6108,
        'snetd': 6208,
    },
}

translations = {
    "en": {
        "de": {
            # Default model from http://opennmt.net/Models-py/
            # model archive has these two files (originally called averaged-10-epoch.pt and sentencepiece.model)
            "translate_model": 'en_to_de_omnt_averaged_10_epoch.pt',
            "sentencepiece_model": 'en_de_sp.model'
        }
    },
    "de": {
        "en": {
            # Trained locally, using same sentencepiece model as en->de
            # Uses preprocessed data from en->de model available here: http://opennmt.net/Models-py/ 
            #
            # Need to use opennmt-py's preprocess.py to convert train.de/train.en etc into pytorch binary representations.
            # No need to train sentencepiece model as we can use the same tokenization as en->de
            #
            # Command to train:
            #  python  train.py -data /tmp/de2/data -save_model /tmp/extra -gpuid 1 \
            #  -layers 6 -rnn_size 512 -word_vec_size 512   \
            #  -encoder_type transformer -decoder_type transformer -position_encoding \
            #  -train_steps 100000  -max_generator_batches 32 -dropout 0.1 \
            #  -batch_size 4096 -batch_type tokens -normalization tokens  -accum_count 4 \
            #  -optim adam -adam_beta2 0.998 -decay_method noam -warmup_steps 8000 -learning_rate 2 \
            #  -max_grad_norm 0 -param_init 0  -param_init_glorot \
            #  -label_smoothing 0.1 
            #
            # Taken from http://opennmt.net/OpenNMT-py/FAQ.html#how-do-i-use-the-transformer-model
            "translate_model": 'de_to_en_joel_65000.pt',
            "sentencepiece_model": 'en_de_sp.model'
        }

    }
}