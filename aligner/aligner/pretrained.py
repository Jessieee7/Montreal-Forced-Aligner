import os

from .base import BaseAligner, TEMP_DIR, TriphoneFmllrConfig, TriphoneConfig

class PretrainedAligner(BaseAligner):
    def __init__(self, archive, corpus, output_directory,
                    temp_directory = None, num_jobs = 3, call_back = None):

        if temp_directory is None:
            temp_directory = TEMP_DIR
        self.temp_directory = temp_directory
        self.output_directory = output_directory
        self.corpus = corpus

        self.dictionary = archive.load_dictionary()

        self.dictionary.output_directory = os.path.join(temp_directory, 'dictionary')
        self.dictionary.write()
        archive.export_triphone_model(self.tri_directory)

        if self.corpus.num_jobs != num_jobs:
            num_jobs = self.corpus.num_jobs
        self.num_jobs = num_jobs
        self.call_back = call_back
        if self.call_back is None:
            self.call_back = print
        self.verbose = False
        self.tri_fmllr_config = TriphoneFmllrConfig(**{'realign_iters': [1, 2],
                                                        'fmllr_iters': [1],
                                                        'num_iters': 3})
        self.tri_config = TriphoneConfig()

    def do_align(self):
        self.train_tri_fmllr()