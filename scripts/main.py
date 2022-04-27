from multiprocessing import Process, Queue
from acquisition_realtime import EMGStream
from filter_realtime import Filter
from SAD_final import SAD
from decoder_realtime import Decoder
from gui_2048 import Board
from gui_text import GUI
# import gui_main

stream = EMGStream()
filter = Filter()
sad = SAD()
decoder = Decoder()
# gui = Board()
gui = GUI()

q_stream_to_filter = Queue()
q_filter_to_sad = Queue()
q_sad_to_ml = Queue()
q_ml_to_gui = Queue()

p_stream = Process(target=stream.get_buffer, args=(q_stream_to_filter,))
p_filter = Process(target=filter.run, args=(q_stream_to_filter,q_filter_to_sad,))
p_sad = Process(target=sad.run, args=(q_filter_to_sad,q_sad_to_ml,))
p_decoder = Process(target=decoder.run, args=(q_sad_to_ml,q_ml_to_gui))
p_gui = Process(target=gui.run, args=(q_ml_to_gui,))

# p_gui = Process(target=gui_main.run, args=(q_ml_to_gui,))

if __name__ == '__main__':
	p_stream.start()
	p_filter.start()
	p_sad.start()
	p_decoder.start()
	p_gui.start()

	p_stream.join()
	p_filter.join()
	p_sad.join()
	p_decoder.join()
	p_gui.join()

	#while True:
	#	print("TEST")
	#	if not q_filter_to_sad.empty():
	#		print(q_filter_to_sad.get())


