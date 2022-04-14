from multiprocessing import Process, Queue
from acquisition import EMGStream
from filter_realtime import Filter

stream = EMGStream()
filter = Filter()

q_stream_to_filter = Queue()
q_filter_to_sad = Queue()
q_sad_to_ml = Queue()

p_stream = Process(target=stream.get_buffer, args=(q_stream_to_filter,))
p_filter = Process(target=filter.run, args=(q_stream_to_filter,q_filter_to_sad,))

if __name__ == '__main__':
	p_stream.start()
	p_filter.start()
	p_stream.join()
	p_filter.join()

	while True:
		if not q_filter_to_sad.empty():
			print(q_filter_to_sad.get())
# p_sad = Process(target=, args=(q,))
# p_ml = Process(target=, args=(q,))

