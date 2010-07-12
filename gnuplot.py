import os

def convert_function_str(s):
    import re
    a = str(s)
    a = re.sub(r'([0-9])x', r'\1*x', a, 100)
    a = re.sub(r'\^', r'**', a, 100)
    return a
    
def plot_function(f):
    g = Gnuplot('plot.png')
    g.plot(convert_function_str(f))
    del g
    
    return './plot.png'

class Gnuplot:
	def __init__(self, f):
	#	print ("opening new gnuplot session...")
		self.session = os.popen("gnuplot","w")
		self.send('set terminal png')
		self.file = str(f)
		self.send('set output "%s"' % self.file)
		self.send("set xlabel 'x'")
		self.send("set ylabel 'y'")
	def __del__(self):
	#	print ("closing gnuplot session...")
		self.session.close()
	def send(self, cmd):
		self.session.write(cmd + '\n')
		self.session.flush()
	def plot(self, s):
	    self.send('plot ' + s)
	def replot(self):
	    self.send('set terminal png')
	    self.send('set output "%s"' % self.file)
	    self.send('replot')
