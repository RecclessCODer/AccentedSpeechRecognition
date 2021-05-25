import numpy as np

import fast-ctc-decode



alphabet = "NACGT"

posteriors = np.random.rand(100, len(alphabet)).astype(np.float32)

seq, path = beam_search(posteriors, alphabet, beam_size=5, beam_cut_threshold=0.1)

print(seq)
