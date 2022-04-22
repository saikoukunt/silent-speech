from kaldi.asr import GmmLatticeFasterRecognizer, LatticeFasterDecoderOptions
from kaldi.util.table import SequentialMatrixReader
import os
import scipy.io.wavfile as wavf

class Decoder():
    def __init__(self):
        decoder_opts = LatticeFasterDecoderOptions()
        decoder_opts.beam = 13.0
        decoder_opts.lattice_beam = 6.0

        self.asr = GmmLatticeFasterRecognizer.from_files("final.mdl", "HCLG.fst", "words.txt", decoder_opts)
        self.feats_rspec = ("ark:compute-mfcc-feats --config=models/silent-speech/conf/mfcc.conf "
               "scp:wav.scp ark:- |")
        self.utt_num = 0
        self.fs = 1000
        self.wav_path = "./wavs/"

    def rescale_data(self, data):
        # convert back to ADC value
        data[:,0:4] = (data[:,0:4]/1000*1009/3.3 + 0.5)*(2**10)
        data[:,4:] = (data[:,4:]/1000*1009/3.3 + 0.5)*(2**6)

        # center at 0
        data[:,0:4] = (data[:,0:4] - 512) * (2**6)
        data[:,4:] = (data[:,4:] - 32) * (2**10)

        return data.astype(dtype='int16')

    
    def run(self, input, output):
        while True:
            if (not input.empty()):
                data = input.get()

                # create wav file
                data = self.rescale_data(data)
                out_f = os.path.join(self.wav_path,f'utt_{self.utt_num}.wav')
                wavf.write(out_f, self.fs, data)

                # create wav.scp
                wavscp = open('./wav.scp')
                path = os.path.join(os.getcwd(), self.wav_path)
                fname = f'utt_{self.utt_num}.wav'
                fullpath = path + '/' + fname
                wavscp.write(f'utt_{self.utt_num}\t{fullpath}\n')

                # decode
                with SequentialMatrixReader(self.feats_rspec) as feats_reader:
                    for (fkey, feats) in feats_reader:
                        out = self.asr.decode(feats)
                        print(out["text"])
                        output.put(out["text"])
                        
                self.utt_num += 1

    