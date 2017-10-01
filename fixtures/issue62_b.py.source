from collections import Counter

from ast2vec.bblfsh_roles import SIMPLE_IDENTIFIER
from ast2vec.repo2.base import Repo2Base


class Repo2IdModel:
    NAME = "Repo2IdModel"


class Repo2IdCounter(Repo2Base):
    """
    Print all SIMPLE_IDENTIFIERs (and counters) from repository
    """
    MODEL_CLASS = Repo2IdModel

    def collect_id_cnt(self, root, id_cnt):
        for ch in root.children:
            if SIMPLE_IDENTIFIER in ch.roles:
                id_cnt[ch.token] += 1
            self.collect_id_cnt(ch, id_cnt)

    def convert_uasts(self, file_uast_generator):
        for file_uast in file_uast_generator:
            print("-" * 20 + " " + str(file_uast.filepath))
            id_cnt = Counter()
            self.collect_id_cnt(file_uast.response.uast, id_cnt)
            print(id_cnt)


if __name__ == "__main__":
    repo = "test/imports/"
    c2v = Repo2IdCounter(linguist="path/to/enry", bblfsh_endpoint="0.0.0.0:9432")
    c2v.convert_repository(repo)
