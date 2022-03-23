import timer

tim = timer.Timer("vocalized",5,"test.txt")

word_list = ['yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no' ,'yes', 'no']

tim.run(word_list)

tim.mainloop()