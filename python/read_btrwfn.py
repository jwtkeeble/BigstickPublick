from utils import Z_to_nuc, get_A_and_symbol

import argparse 

parser = argparse.ArgumentParser(prog='read binary file', description='')
parser.add_argument('-N', '--nucleus', default='6Be', type=str, help='Nucleus')
parser.add_argument('-K', '--nkeep',   default=1,     type=int, help='Number of Eigenstates to be expected in the .btrwfn file')
args=parser.parse_args()

NNcore=20
ZZcore=20

nucleus = args.nucleus
A, sym = get_A_and_symbol(nucleus)
Z = Z_to_nuc.inverse[sym]
N = A-Z

nqubits_z = Z-ZZcore if (Z != 40) else 0
nqubits_n = N-NNcore if (N != 40) else 0
nqubits = nqubits_n + nqubits_z

nkeep = args.nkeep

import struct
import os
from tqdm import tqdm

def read_btyes(record_format, f):
    record_size = struct.calcsize(record_format)
    record = f.read(record_size)
    return struct.unpack(record_format, record)

record_format = "i"*nqubits + "f"*nkeep  # num qubits + num eigenstates
record_size = struct.calcsize(record_format)

filename = f"../{nucleus}.btrwfn"
data = []

states = []
coeffs = []

file_size = os.path.getsize(filename)

with open(filename, "rb") as f:
    with tqdm(total=file_size, unit="B", unit_scale=True, desc="Reading File") as pbar:
        while True:
            record = f.read(record_size) # read 1 state & coeff (until end of `f`)
            if len(record) < record_size:
                break
            record_unpack = struct.unpack(record_format, record) # un-pack state & coeff
            states.append(record_unpack[:-1]) 
            coeffs.append(record_unpack[-1])
            
            data.append(record_unpack)

            pbar.update(len(record))

import numpy as np
states = np.array(object=states, dtype=np.int64)
coeffs = np.array(object=coeffs, dtype=np.float64)

nconfigs = coeffs.shape[0]

zdata = {
        'ZZ':Z, # NOTE: -1 for default value
        'NN':N,
        'ZZcore':ZZcore,
        'NNcore':NNcore,
        'jztab':-1,
        'tztab':-1,
        'n_qubits':nqubits,
        'n_configs':nconfigs,
        'n_qubits_n':nqubits_n,
        'n_qubits_p':nqubits_z,
        'Nshift':-1,
        'states':states,
        'coeffs':coeffs
}
np.savez_compressed(file=f'{args.nucleus}.btrwfn.npz',**zdata)

print(states, states.shape)
print(coeffs, coeffs.shape)
# Print the results
#for i, record in enumerate(data):
#    print(f"Line {i + 1}: Integers: {record[:2]}, Float: {record[2]}")