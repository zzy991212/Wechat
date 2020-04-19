import os
import struct
buffsize = 1024
def sendfile(filepath,sock):
    if os.path.isfile(filepath):
        fileinfo_size = struct.calcsize('128sl')
        fhead = struct.pack('128sl', os.path.basename(filepath).encode(), os.stat(filepath).st_size)
        sock.send(fhead)
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(buffsize)
            if not data:
                break
            sock.send(data)

def recvfile(filesavepath,sock):
    fileinfo_size = struct.calcsize('128sl')
    buf = sock.recv(fileinfo_size)
    if buf:
        filename, filesize = struct.unpack('128sl', buf)
        fn = filename.strip(b'\00')
        fn = fn.decode()
 
        recvd_size = 0  
        fp = open(filesavepath+fn, 'wb')
        while not recvd_size == filesize:
            if filesize - recvd_size > buffsize:
                data = sock.recv(buffsize)
                recvd_size += len(data)
            else:
                data = sock.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()
    return fn