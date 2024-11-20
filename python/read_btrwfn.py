import argparse 

parser = argparse.ArgumentParser(prog='read binary file', description='')
parser.add_argument('-N','--nucleus',default='6Be',type=str,help='Nucleus')
parser.add_argument('-K','--nkeep',default=1,type=int,help='number of eigenstates in file')

args=parser.parse_args()
nucleus = args.nucleus
nkeep = args.nkeep

import struct
import os
from tqdm import tqdm

def read_btyes(record_format, f):
    record_size = struct.calcsize(record_format)
    record = f.read(record_size)
    return struct.unpack(record_format, record)

record_format = "i"*12 + "f"*nkeep  # num qubits + num eigenstates
record_size = struct.calcsize(record_format)

filename = f"../outputs/{nucleus}.btrwfn"
data = []

states = []
coeffs = []

file_size = os.path.getsize(filename)

with open(filename, "rb") as f:
    with tqdm(total=file_size, unit="B", unit_scale=True, desc="Reading File") as pbar:
        while True:
            record = f.read(record_size) # read 1 state & coeff (until end of `f`)
            if not record:
                break
            
            record_unpack = struct.unpack(record_format, record) # un-pack state & coeff
            states.append(record_unpack[:-1]) 
            coeffs.append(record_unpack[-1])

            data.append(record_unpack)

            pbar.update(len(record))

import numpy as np
states = np.array(object=states, dtype=np.uint8)
coeffs = np.array(object=coeffs, dtype=np.float64)

zdata = {
         'states':states,
         'coeffs':coeffs
}
np.savez_compressed(file=f'{args.nucleus}.btrwfn.npz',**zdata)

print(states)
print(coeffs)
# Print the results
#for i, record in enumerate(data):
#    print(f"Line {i + 1}: Integers: {record[:2]}, Float: {record[2]}")