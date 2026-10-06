import random

random.seed(1) #computers can't produce truly random numbers =>
#same random numbers every run, so results are reproducible
#they use a fixed formula that turns one number into the next and the next…

price = 100.0
VOL = 2 #size of a typical move per tick

for t in range(20):
    price += random.gauss(0, VOL) #one random step: N(0, VOL^2)
    print(t, round(price,2))