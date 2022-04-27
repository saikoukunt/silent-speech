import os
import scipy.io.wavfile as wavf
import subprocess

class Decoder():
    def __init__(self):
        self.utt_num = 0
        self.fs = 1000
        self.wav_path = "./wavs/"
        self.sess = 0

        command = subprocess.run(["rm", "-rf", "../output.txt"], stdout=subprocess.DEVNULL)

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

                # os.system('rm -rf ../data/online')
                # os.system('mkdir ../data/online')
                # os.system('rm -rf ../exp/tri3a/decode') 

                command = subprocess.run(["rm", "-rf", "../data/online"], stdout=subprocess.DEVNULL)
                command = subprocess.run(["mkdir", "../data/online"], stdout=subprocess.DEVNULL)
                command = subprocess.run(["rm", "-rf", "../exp/tri3a/decode"], stdout=subprocess.DEVNULL)

                print("removed")

                # create wav file
                data = self.rescale_data(data)
                out_f = os.path.join(self.wav_path,f'utt_{self.utt_num}.wav')
                wavf.write(out_f, self.fs, data)

                # create wav.scp
                wavscp = open('../data/online/wav.scp','w')
                path = os.path.join(os.getcwd(), self.wav_path)
                fname = f'utt_{self.utt_num}.wav'
                fullpath = path + '/' + fname
                wavscp.write(f'utt_{self.utt_num}\t{fullpath}\n')
                wavscp.close()

                # create utt2spk
                u2s = open('../data/online/utt2spk','w')
                u2s.write(f'utt_{self.utt_num}\t{self.sess}\n')
                u2s.close()

                # decode
                # os.system('cd ..;./decoder.sh')
                command = subprocess.run(["./decoder.sh"], cwd=os.path.join(os.getcwd(),"/../"), stdout=subprocess.DEVNULL)

                text = open("../output.txt",'r')
                text = text.read()
                print(text)
                output.put(text)
                        
                self.utt_num += 1

