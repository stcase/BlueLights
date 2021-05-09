import tinytuya

d = tinytuya.BulbDevice('bf2c9c76ed0e17591de2tm', '192.168.1.103', '61174a33c99e06eb')
d.set_version(3.3)
data = d.status()

print('Dictionary %r' % data)

d.set_colour(0,255,0)

#d.set_brightness(1000)

#d.set_white(1000,10)
