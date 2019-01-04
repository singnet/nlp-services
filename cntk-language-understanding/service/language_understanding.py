import os
import requests
import glob
import hashlib
import logging
import datetime

import numpy as np
import cntk as C
import cntk.tests.test_utils
cntk.tests.test_utils.set_device_from_pytest_env()  # (only needed for our build system)
C.cntk_py.set_fixed_random_seed(1)  # fix a random seed for CNTK components

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("language_understanding")


class LanguageUnderstanding:
    def __init__(self,
                 train_ctf_url,
                 test_ctf_url,
                 query_wl_url,
                 slots_wl_url,
                 intent_wl_url,
                 vocab_size,
                 num_labels,
                 num_intents,
                 sentences_url
                 ):

        self.train_ctf_url = train_ctf_url
        self.test_ctf_url = test_ctf_url
        self.query_wl_url = query_wl_url
        self.slots_wl_url = slots_wl_url
        self.intent_wl_url = intent_wl_url

        self.vocab_size = vocab_size
        self.num_labels = num_labels
        self.num_intents = num_intents

        self.sentences_url = sentences_url

        self.response = dict()

    @staticmethod
    def download(url, filename=None, save=True):
        if "http://" in url or "https://" in url:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:9.0) Gecko/20100101 Firefox/10.0'}
            r = requests.get(url, headers=header, allow_redirects=True)
            if save:
                with open(filename, "wb") as handle:
                    for data in r.iter_content():
                        handle.write(data)
            else:
                return r.text
        else:
            log.debug("Not a valid URL: {}".format(url))

    @staticmethod
    def delete_old_files(folder):
        try:
            for file_path in glob.iglob("{}/*".format(folder), recursive=True):
                file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if datetime.datetime.now() - file_timestamp > datetime.timedelta(hours=24):
                    log.debug("Deleting old file: {}".format(file_path))
                    os.remove(file_path)
            return True
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def create_model_slot(emb_dim, hidden_dim, num_labels):
        with C.layers.default_options(initial_state=0.1):
            return C.layers.Sequential([
                C.layers.Embedding(emb_dim, name="embed"),
                C.layers.Recurrence(C.layers.LSTM(hidden_dim), go_backwards=False),
                C.layers.Dense(num_labels, name="classify")
            ])

    @staticmethod
    def create_model_intent(emb_dim, hidden_dim, num_intents):
        with C.layers.default_options(initial_state=0.1):
            return C.layers.Sequential([
                C.layers.Embedding(emb_dim, name='embed'),
                C.layers.Stabilizer(),
                C.sequence.reduce_sum(C.layers.Recurrence(C.layers.LSTM(hidden_dim), go_backwards=False)),
                C.layers.Dense(num_intents, name='classify')
            ])

    @staticmethod
    def create_reader(in_path, vocab_size, num_intents, num_labels, is_training):
        return C.io.MinibatchSource(C.io.CTFDeserializer(in_path, C.io.StreamDefs(
            query=C.io.StreamDef(field="S0", shape=vocab_size, is_sparse=True),
            intent=C.io.StreamDef(field="S1", shape=num_intents, is_sparse=True),
            slot_labels=C.io.StreamDef(field="S2", shape=num_labels, is_sparse=True)
        )), randomize=is_training, max_sweeps=C.io.INFINITELY_REPEAT if is_training else 1)

    @staticmethod
    def create_criterion_function_preferred(model, labels):
        ce = C.cross_entropy_with_softmax(model, labels)
        errs = C.classification_error(model, labels)
        return ce, errs  # (model, labels) -> (loss, error metric)

    @staticmethod
    def create_criterion_function(model):
        labels = C.placeholder(name='labels')
        ce = C.cross_entropy_with_softmax(model, labels)
        errs = C.classification_error(model, labels)
        return C.combine([ce, errs])  # (features, labels) -> (loss, metric)

    def train(self, x, y, reader, model_func, max_epochs=10, task="slot_tagging"):
        log.info("Training...")

        # Instantiate the model function; x is the input (feature) variable
        model = model_func(x)

        # Instantiate the loss and error function
        loss, label_error = self.create_criterion_function_preferred(model, y)

        # training config
        epoch_size = 18000  # 18000 samples is half the dataset size
        minibatch_size = 70

        # LR schedule over epochs
        # In CNTK, an epoch is how often we get out of the minibatch loop to
        # do other stuff (e.g. checkpointing, adjust learning rate, etc.)
        lr_per_sample = [3e-4] * 4 + [1.5e-4]
        lr_per_minibatch = [lr * minibatch_size for lr in lr_per_sample]
        lr_schedule = C.learning_parameter_schedule(lr_per_minibatch, epoch_size=epoch_size)

        # Momentum schedule
        momentums = C.momentum_schedule(0.9048374180359595, minibatch_size=minibatch_size)

        # We use a the Adam optimizer which is known to work well on this dataset
        # Feel free to try other optimizers from
        # https://www.cntk.ai/pythondocs/cntk.learner.html#module-cntk.learner
        learner = C.adam(
            parameters=model.parameters,
            lr=lr_schedule,
            momentum=momentums,
            gradient_clipping_threshold_per_sample=15,
            gradient_clipping_with_truncation=True)

        # Setup the progress updater
        progress_printer = C.logging.ProgressPrinter(tag="Training", num_epochs=max_epochs)

        # Instantiate the trainer
        trainer = C.Trainer(model, (loss, label_error), learner, progress_printer)

        # process mini batches and perform model training
        C.logging.log_number_of_parameters(model)

        # Assign the data fields to be read from the input
        if task == "slot_tagging":
            data_map = {x: reader.streams.query, y: reader.streams.slot_labels}
        else:
            data_map = {x: reader.streams.query, y: reader.streams.intent}

        t = 0
        for epoch in range(max_epochs):  # loop over epochs
            epoch_end = (epoch + 1) * epoch_size
            while t < epoch_end:  # loop over mini batches on the epoch
                data = reader.next_minibatch(minibatch_size, input_map=data_map)  # fetch mini batch
                trainer.train_minibatch(data)  # update model with it
                t += data[y].num_samples  # samples so far
            trainer.summarize_training_progress()

        return model

    def evaluate(self, x, y, reader, model_func, task="slot_tagging"):
        log.info("Evaluating...")

        # Instantiate the model function; x is the input (feature) variable
        model = model_func(x)

        # Create the loss and error functions
        loss, label_error = self.create_criterion_function_preferred(model, y)

        # process mini batches and perform evaluation
        progress_printer = C.logging.ProgressPrinter(tag="Evaluation", num_epochs=0)

        # Assign the data fields to be read from the input
        if task == "slot_tagging":
            data_map = {x: reader.streams.query, y: reader.streams.slot_labels}
        else:
            data_map = {x: reader.streams.query, y: reader.streams.intent}

        evaluator = None
        while True:
            minibatch_size = 500
            data = reader.next_minibatch(minibatch_size, input_map=data_map)
            if not data:
                break

            evaluator = C.eval.Evaluator(loss, progress_printer)
            evaluator.test_minibatch(data)

        if evaluator:
            evaluator.summarize_test_progress()
        else:
            log.error("Error: evaluator is None")

    def language_understanding(self, intent_model=False):

        self.response = {
            "model_url": "Fail",
            "output_url": "Fail"
        }
        # Setting a hash accordingly to the inputs (URLs)
        seed = "{}{}{}{}{}{}{}".format(
            self.train_ctf_url,
            self.test_ctf_url,
            self.query_wl_url,
            self.slots_wl_url,
            self.intent_wl_url,
            self.sentences_url,
            intent_model
        )
        m = hashlib.sha256()
        m.update(seed.encode("utf-8"))
        m = m.digest().hex()
        # Get only the first and the last 10 hex
        uid = m[:10] + m[-10:]

        data_folder = "./data/{}".format(uid)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        user_data = {
            "train": ["{}/train.ctf".format(data_folder), self.train_ctf_url],
            "test": ["{}/test.ctf".format(data_folder), self.test_ctf_url],
            "query": ["{}/query.wl".format(data_folder), self.query_wl_url],
            "slots": ["{}/slots.wl".format(data_folder), self.slots_wl_url],
            "intent": ["{}/intent.wl".format(data_folder), self.intent_wl_url]
        }

        for data_set, data_source in user_data.items():
            if not os.path.exists(data_source[0]):
                log.info("{}: Downloading...".format(data_source[1]))
                self.download(data_source[1], data_source[0])
            else:
                log.info("{}: Reusing...".format(data_source[0]))

        # number of words in vocab, slot labels, and intent labels
        vocab_size = self.vocab_size
        num_labels = self.num_labels
        num_intents = self.num_intents

        # model dimensions
        emb_dim = 150
        hidden_dim = 300

        # Create the containers for input feature (x)
        x_input = C.sequence.input_variable(vocab_size)

        # Training the models
        reader = self.create_reader(user_data["train"][0], vocab_size, num_intents, num_labels, is_training=True)
        if intent_model:
            #  label (y)
            y_input = C.input_variable(num_intents)
            z_intent = self.create_model_intent(emb_dim, hidden_dim, num_intents)
            z_intent = self.train(x_input, y_input, reader, z_intent, task="intent")
            z = z_intent
        else:
            #  label (y)
            y_input = C.sequence.input_variable(num_labels)
            z_slot_tagging = self.create_model_slot(emb_dim, hidden_dim, num_labels)
            z_slot_tagging = self.train(x_input, y_input, reader, z_slot_tagging, task="slot_tagging")
            z = z_slot_tagging

        # Testing the models
        if os.path.exists(user_data["test"][0]):
            reader = self.create_reader(user_data["test"][0], vocab_size, num_intents, num_labels, is_training=False)
            if intent_model:
                self.evaluate(x_input, y_input, reader, z, task="intent")
            else:
                self.evaluate(x_input, y_input, reader, z, task="slot_tagging")

        # load dictionaries
        query_wl = [line.rstrip("\n") for line in open(user_data["query"][0])]
        slots_wl = [line.rstrip("\n") for line in open(user_data["slots"][0])]
        intent_wl = [line.rstrip("\n") for line in open(user_data["intent"][0])]
        query_dict = {query_wl[i]: i for i in range(len(query_wl))}
        intent_dict = {intent_wl[i]: i for i in range(len(intent_wl))}

        # let"s run a sequence through
        sentences_file_content = self.download(self.sentences_url, save=False)
        sentences = sentences_file_content.split("\n")[:-1]
        log.debug("Sentences: {}".format(sentences))
        output = []
        for sent in sentences:
            if not all(x in sent for x in ["BOS", "EOS"]):
                seq = "BOS {} EOS".format(sent)
            else:
                seq = sent

            w = [query_dict[w] for w in seq.split() if w in query_dict]
            one_hot = np.zeros([len(w), len(query_dict)], np.float32)
            for t in range(len(w)):
                one_hot[t, w[t]] = 1

            pred = z(x_input).eval({x_input: [one_hot]})[0]
            if intent_model:
                best = np.argmax(pred)
                output.append("{} -> {}".format(seq, intent_wl[int(best)]))
            else:
                best = np.argmax(pred, axis=1)
                output.append(str(list(zip(seq.split(), [slots_wl[s] for s in best]))))

        output_folder = "/opt/singnet/output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Saving the trained model
        model_file = "{}.model".format(uid)
        z.save("{}/{}".format(output_folder, model_file))

        log.info("Output: {}".format(output))
        output_file = "{}.txt".format(uid)
        with open("{}/{}".format(output_folder, output_file), "w+") as f:
            if intent_model:
                for idx, line in enumerate(output):
                    f.write("{}: {}\n".format(idx, output[idx]))
            else:
                for idx, line in enumerate(sentences):
                    f.write("{}: {}\n{}: {}\n".format(idx, line, idx, output[idx]))

        # Removing old files (> 24h)
        self.delete_old_files(data_folder)
        self.delete_old_files(output_folder)

        self.response["model_url"] = "http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Output/{}".format(model_file)
        self.response["output_url"] = "http://54.203.198.53:7000/LanguageUnderstanding/CNTK/Output/{}".format(output_file)
        return self.response
