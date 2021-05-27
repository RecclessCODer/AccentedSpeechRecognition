from tqdm import tqdm
from dataloader import MultiDataset, MultiDataLoader
from model import MultiTask
import torch
import torch.nn as nn
from decoder import GreedyDecoder, BeamCTCDecoder


_test_manifest = './data/test_one.csv'
_labels = "_'ABCDEFGHIJKLMNOPQRSTUVWXYZ "
_accent_dict = 'australia,canada,england,us,ireland,scotland,wales'
_use_mfcc_in = True
_use_ivectors_in = False
_use_embeddings_in = False
_embedding_size = 256
_use_transcripts_out = True
_use_accents_out = True
_batch_size = 1
_num_workers = 4
model_path = './saved_models/TrainMulti_TRAIN__in_mfcc__out_transcripts_accents-mix0.5-focal__nblyrs-head-3-speech-2-accent-2__bnf-256__24-05-2021_18h27m26.pth'
lm = './data/language_models/cv.lm'


test_dataset = MultiDataset(_test_manifest,
                            _labels,
                            _accent_dict=_accent_dict,
                            use_mfcc_in=_use_mfcc_in,
                            use_ivectors_in=_use_ivectors_in,
                            use_embeddings_in=_use_embeddings_in,
                            embedding_size=_embedding_size,
                            use_transcripts_out=_use_transcripts_out,
                            use_accents_out=_use_accents_out)

test_loader = MultiDataLoader(test_dataset,
                              batch_size=_batch_size,
                              shuffle=True,
                              num_workers=_num_workers)

# load model
model, __ = MultiTask.load_model(model_path)
model = model.cuda()
criterion = (nn.CTCLoss(), nn.CrossEntropyLoss())

decoder = BeamCTCDecoder(_labels,
                         lm_path=lm,
                         alpha=0.8,
                         beta=1.,
                         cutoff_top_n=40,
                         cutoff_prob=1.,
                         beam_width=100,
                         num_processes=_num_workers)

target_decoder = GreedyDecoder(_labels)

# test
with torch.no_grad():
    model.eval()
    for data in tqdm(test_loader, total=len(test_loader)):
        inputs, inputs_lens, transcripts, transcripts_lens, accents = data
        inputs = inputs.cuda()
        inputs_lens = inputs_lens.cuda()
        accents = accents.cuda()

        # forward
        out_text, out_accent, out_lens, __ = model(inputs, inputs_lens)

        # decode
        split_transcripts = []
        offset = 0
        for size in transcripts_lens:
            split_transcripts.append(transcripts[offset:offset + size])
            offset += size

        decoded_output, _ = decoder.decode(out_text.data.transpose(0, 1), out_lens)
        print('Reference:')
        print(decoded_output)
        target_strings = target_decoder.convert_to_strings(split_transcripts)
        print(target_strings)




