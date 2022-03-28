from collections import deque
import numpy as np
import scipy

class channel():
    def __init__(self, signal, channel_num):
        super().__init__()
    
        #frame_length is time
        self.sample_rate = 1000

        self.channel_num = channel_num -1
        self.hasData = True

        self.signal = signal.signal
        self.timestamp = signal.time
        self.signal_length = len(self.signal)
        self.frame_length = 50 * self.data_rate # in samples
        self.frame_shift = 25 * self.data_rate # in samples
        
        self.num_frames = (self.signal_length-self.frame_length)/self.frame_shift
        self.num_features = 14
        self.MFCC = np.zeros((self.num_frames, self.num_features))

    def calculate(self):
        # recalculate signal length params
        self.signal_length = len(self.signal)
        self.num_frames = (self.signal_length-self.frame_length)/self.frame_shift
        self.MFCC = np.zeros((self.num_frames, self.num_features))

        # Split into frames
        pad_signal_length = self.num_frames * self.frame_shift + self.frame_length
        z = np.zeros((pad_signal_length-self.signal_length))
        pad_signal = np.append(self.signal,z) # zero-pad signal so that all frames have enough samples

        indices = np.tile(np.arange(0, self.frame_length),(self.num_frames,1)) \
            + np.tile(np.arange(0, self.num_frames * self.frame_shift, \
            self.frame_shift), (self.frame_length,1)).T
        frames = pad_signal[indices.astpe(numpy.int32, copy=False)]

        # Hamming window
        frames *= np.hamming(self.frame_length)

        # Fourier transform and Power Spectrum
        mag_frames = np.absolute(np.fft.rfft(frames))
        pow_frames = ((1/self.frame_length) * ((mag_frames)**2))

        # Filter banks (maybe move coefficient calculation to constructor?)
        nfilt = 15 # might need to reduce since our sampling rate is lower
        low_freq_mel = 0
        high_freq_mel = (2595 * np.log10(1+(self.sample_rate/2)/700)) # Hz to mel conversion
        mel_points = np.linspace(low_freq_mel,high_freq_mel,nfilt+2) # equally spaced in  mel scale
        hz_points = (700*(10**(mel_points/2595) - 1)) # Convert back to Hz
        bins = np.floor((self.frame_length+1)*hz_points/ self.sample_rate)

        fbank = np.zeros((nfilt,int(np.floor(self.frame_length/2+1))))
        for m in range(1, nfilt+1):
            f_m_minus = int(bin[m-1])   # left
            f_m = int(bin[m])           # center
            f_m_plus = int(bin[m+1])    #right

            for k in range(f_m_minus, f_m):
                f_bank[m-1,k] = (k-bin[m-1])/(bin[m]-bin[m-1]) # calculate filter coeffs
            for k in range(f_m, f_m_plus):
                f_bank[m-1,k] = (bin[m+1]-k)/(bin[m+1]-bin[m]) # calculate filter coeffs

        filter_banks = np.dot(pow_frames, fbank.T)
        filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks) # replace zeros for numerical stability
        filter_banks = filter_banks ** 0.1 # Root compression

        # Discrete cosine transform
        num_ceps = 6
        mfcc = scipy.fftpack.dct(filter_banks,type=2,axis=1,norm='ortho')[:,0:(num_ceps+1)]
        mfcc_delta = np.zeros((mfcc.shape[0],num_ceps))

        # Mean normalization + write to global



    
