from multiprocessing import Process, Queue
from acquisition_realtime import EMGStream
from filter_realtime import Filter
from SAD_new2 import SAD

stream = EMGStream()
filter = Filter()
sad = SAD()

q_stream_to_filter = Queue()
q_filter_to_sad = Queue()
q_sad_to_ml = Queue()

p_stream = Process(target=stream.get_buffer, args=(q_stream_to_filter,))
p_filter = Process(target=filter.run, args=(q_stream_to_filter,q_filter_to_sad,))
p_sad = Process(target=sad.run, args=(q_filter_to_sad,q_sad_to_ml,))

if __name__ == '__main__':
	p_stream.start()
	p_filter.start()
	p_sad.start()

	p_stream.join()
	p_filter.join()
	p_sad.join()


	#while True:
	#	print("TEST")
	#	if not q_filter_to_sad.empty():
	#		print(q_filter_to_sad.get())


