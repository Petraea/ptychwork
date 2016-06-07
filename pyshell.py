import pty, termios, struct, fcntl
from twisted.internet import protocol, reactor

def set_winsize(fd, row, col):
#                           row, col, xpix(unused), ypix(unused))
    winsize = struct.pack("HHHH", row, col, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

class MyProcessProtocol(protocol.ProcessProtocol):
    def __init__(self,fd):
        self.fd=fd
        #Demo stuff.
        reactor.callLater(0, self.execute, 'export TERM=xterm')
        reactor.callLater(0.1, self.execute, 'cmatrix')
        reactor.callLater(1, self.resize, (20,20))
        reactor.callLater(4, self.execute, '\x03') #BREAK
        reactor.callLater(5, self.execute, 'tput cols')
        reactor.callLater(5, self.execute, 'tput lines')
        reactor.callLater(6, self.execute, '\x04') #DIE

    def execute(self,cmd):
        if self.transport:
            self.transport.write(cmd+'\n')

    def resize(self,dims):
        set_winsize(self.fd,dims[0],dims[1])

    def outReceived(self, data):
        #Do stuff here.
        print(data)

    def processExited(self,reason):
        print(reason)
        reactor.stop()

master, slave = pty.openpty()
proc = MyProcessProtocol(master)
reactor.spawnProcess(proc, 'bash',usePTY=(master,slave,'xterm'))
reactor.run()
