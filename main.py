import input, process, sys, time
sys.setrecursionlimit(1000000)
#  "a_example.in"
#  "b_small.in"
#  "c_medium.in"
#  "d_big.in"
#  "t_test.in"
print('pizza run')
inputdata = input.inputmap("d_big.in")
p = process.Process(inputdata)
p.run()
print('Done')
print(time.process_time())



