print list(file('myfile.jpg').read()) #'\xff'
print ord('\xff') #255
print format(ord('\xff')) #255
print '{:08b}'.format(ord('\xff')) #11111111
print ' '.join(map( lambda c: '{:08b}'.format(ord(c)), list(file('myfile.jpg').read())))
