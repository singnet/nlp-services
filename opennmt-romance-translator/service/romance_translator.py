import os
import pathlib
import requests
import hashlib
import datetime
import subprocess
import base64
import logging
import traceback

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("romance_translator")


class RomanceTranslator:
    def __init__(self, source_lang, target_lang, sentences_url):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.sentences_url = sentences_url

        self.response = dict()

    @staticmethod
    def _is_base64(sb):
        try:
            if type(sb) == str:
                sb_bytes = bytes(sb, 'ascii')
            elif type(sb) == bytes:
                sb_bytes = sb
            else:
                raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
        except Exception as e:
            log.error("Not Base64: " + str(e))
            return False

    def translate(self):

        try:
            # Setting a hash accordingly to the inputs
            seed = "{}{}{}".format(
                self.source_lang,
                self.target_lang,
                datetime.datetime.now()
            )
            m = hashlib.sha256()
            m.update(seed.encode("utf-8"))
            m = m.digest().hex()
            # Get only the first and the last 10 hex
            uid = m[:10] + m[-10:]

            if "http://" in self.sentences_url or "https://" in self.sentences_url:
                header = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:9.0) Gecko/20100101 Firefox/10.0'}
                r = requests.get(self.sentences_url, headers=header, allow_redirects=True)
                sentences = r.text
            else:
                if self._is_base64(self.sentences_url):
                    sentences = base64.b64decode(self.sentences_url)
                else:
                    sentences = self.sentences_url

            in_sentences = "input_{}.txt".format(uid)
            out_sentences = "output_{}.txt".format(uid)

            with open("utils/{}".format(in_sentences), "w+", encoding="utf-8") as f:
                f.write(sentences)

            utils_path = pathlib.Path(__file__).absolute().parent.parent.joinpath("utils")
            p = subprocess.Popen(["sh",
                                  "translator.sh",
                                  "./data",
                                  self.source_lang,
                                  self.target_lang,
                                  in_sentences,
                                  out_sentences],
                                 cwd=str(utils_path))
            p.wait()

            self.response["translation"] = ""
            with open("utils/{}".format(out_sentences), "r", encoding="utf-8") as f:
                for idx, line in enumerate(f.readlines()):
                    self.response["translation"] += line

            if os.path.exists("utils/{}".format(in_sentences)):
                os.remove("utils/{}".format(in_sentences))
            if os.path.exists("utils/{}".format(out_sentences)):
                os.remove("utils/{}".format(out_sentences))

            return self.response

        except Exception as e:
            log.error(e)
            traceback.print_exc()
            self.response["translation"] = "Fail"
            return self.response
