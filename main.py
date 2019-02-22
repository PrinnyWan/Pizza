import input, process, sys, time
sys.setrecursionlimit(1000000)
#  "a_example.in"
#  "b_small.in"
#  "c_medium.in"
#  "d_big.in"
print('pizza run')
inputdata = input.inputmap("c_medium.in")
p = process.processdata()
p.run(inputdata)
print('Done')
print(time.process_time())



