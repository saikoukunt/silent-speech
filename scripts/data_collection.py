import timer

tim = timer.Timer("vocalized",5,"test.txt")

word_list = ['yes', 'no', 'up', 'down', 'left', 'right']

tim.run(word_list)

tim.mainloop()