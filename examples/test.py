from MPUdriver import MPUDriver as mpu
mpu = mpu()
mpu.self_test()

# while True:
#   mpu()

# from timeit import default_timer as timer
# while True:
#   start = timer()
#   mpu()
#   fin = timer() - start
#   print(f'looptime: {fin:.2f}s')
#   print(mpu())
#   break