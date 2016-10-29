import re
import sys
import argparse

def main(args):
    with open(args.filename, "rb") as f:
        data = f.read()
        fis = re.finditer( '[\xce\xcf\xcd\xcc\xcb\xca]\xfa\xed\xfe\x0c', data)

    addrs = []
    for fi in fis:
        if args.verbose:
            str = data[fi.start(0):fi.start(0)+16]
            out = ' '.join(['{:02x}'.format(h) for h in map(ord, str)])
            print('0x{:08x}: {}'.format(fi.start(0), out))
        addrs.append(fi.start(0))

    addrs.append(len(data))
    
    for i in xrange(len(addrs)-1):
        outname = '{}.bin'.format(i+1)
        with open(outname, 'wb') as f:
            f.write(data[addrs[i]:addrs[i+1]])
            print('Written {}'.format(outname))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract the executables from Mach-O')
    parser.add_argument('filename', help='The Mach-O file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show more detail')
    args = parser.parse_args()
    main(args)