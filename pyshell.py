import pty, termios, struct, fcntl
from twisted.internet import protocol, reactor, task

def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

class MyProcessProtocol(protocol.ProcessProtocol):
    def __init__(self,fd):
        self.fd=fd
        reactor.callLater(0, self.execute, 'export TERM=xterm')
        reactor.callLater(0.1, self.execute, 'cmatrix')
        reactor.callLater(3, self.resize, (20,20))
#        reactor.callLater(2, self.execute, '\x03') #BREAK
#        reactor.callLater(1, self.execute, 'tput cols')
#        reactor.callLater(1, self.execute, 'tput lines')

    def execute(self,cmd):
        if self.transport:
            self.transport.write(cmd+'\n')

    def resize(self,dims):
        set_winsize(self.fd,dims[0],dims[1])

    def outReceived(self, data):
#        print(repr(data))
        print(data)
#        pass

master, slave = pty.openpty()
proc = MyProcessProtocol(master)
#reactor.spawnProcess(proc, 'script', ['/dev/null'])
reactor.spawnProcess(proc, 'script', ['/dev/null'],usePTY=(master,slave,'xterm'))
reactor.run()
