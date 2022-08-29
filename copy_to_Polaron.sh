# Simple script to push the code to the Polaron server

cp * ~/Polaron/test/calc
sed -i 's/self.Polaron = False/self.Polaron = True/' ~/Polaron/test/calc/options.py
