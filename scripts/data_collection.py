import timer

tim = timer.Timer("vocalized",5,"test.txt")

#word_list = ['yes', 'no']

word_list = ["yes", "no",
"zero",
"one",
"two",
"three",
"four",
"five",
"six",
"seven",
"eight",
"nine",
"ten",
"up",
"down",
"left",
"right",
"north",
"south",
"east",
"west",
"stop",
"lamp",
"table",
"desk",
"chair",
"bed",
"computer",
"mouse",
"stove",
"microwave",
"sink",
"toilet"]



word_list = word_list * 3
tim.run(word_list)

tim.mainloop()