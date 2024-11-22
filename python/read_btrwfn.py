import jax.cloud_tpu_init
from utils import Z_to_nuc, get_A_and_symbol

import argparse 

parser = argparse.ArgumentParser(prog='read binary file', description='')
parser.add_argument('-N', '--nucleus', default='6Be', type=str, help='Nucleus')
parser.add_argument('-K', '--nkeep',   default=1,     type=int, help='Number of Eigenstates to be expected in the .btrwfn file')
args=parser.parse_args()

#NNcore=12
#ZZcore=12

nucleus = args.nucleus
A, sym = get_A_and_symbol(nucleus)
Z = Z_to_nuc.inverse[sym]
N = A-Z

from utils import get_valence_and_core

ZZ, ZZcore = get_valence_and_core(x=Z)
print('ZZ, ZZcore: ',ZZ, ZZcore)
NN, NNcore = get_valence_and_core(x=N)
print('NN, NNcore: ',NN, NNcore)

#ZZ = Z-ZZcore if (Z != 20) else 0
#NN = N-NNcore if (N != 20) else 0
valence = ZZ + NN

Nspstates=24 # NOTE: pf-shell 
if (ZZ != 0 and NN != 0):
    Nqubits = Nspstates
    Nqubits_n = int(Nqubits/2)
    Nqubits_p = int(Nqubits/2)
elif (ZZ == 0):
    Nqubits = int(Nspstates/2)
    Nqubits_n = int(Nqubits)
    Nqubits_p = 0
elif (NN == 0):
    Nqubits = int(Nspstates/2)
    Nqubits_p = int(Nqubits)
    Nqubits_n = 0
else:
    raise ValueError(f'Must have at least 1 valence neutron or 1 valence proton, but got valence neutron: {NN} valence protn: {ZZ}')


if(ZZ==0):
    Nshift=Nqubits
else:
    Nshift=0

nkeep = args.nkeep

import struct
import os
import numpy as onp
import jax 
jax.config.update('jax_enable_x64',True)
from jax import numpy as jnp
from tqdm import tqdm

def read_btyes(record_format, f):
    record_size = struct.calcsize(record_format)
    record = f.read(record_size)
    return struct.unpack(record_format, record)

record_format = "i"*valence + "f"*nkeep  # num qubits + num eigenstates
record_size = struct.calcsize(record_format)
print(f'record_format: {record_format}')
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
            #print(record_unpack)
            idx = onp.array([x-1-Nshift for x in record_unpack[:-1]])
            #print(idx)
            states.append(idx)
            
            coeffs.append(record_unpack[-1])
            
            data.append(record_unpack)

            pbar.update(len(record))

states = jnp.array(object=states, dtype=jnp.uint8)
coeffs = jnp.array(object=coeffs, dtype=jnp.float64)

nconfigs = coeffs.shape[0]

zdata = {
    'ZZ':ZZ,
    'NN':NN,
    'ZZcore':ZZcore,
    'NNcore':NNcore,
    'jztab':-1, # NOTE: -1 for default value
    'tztab':-1,
    'n_qubits':Nqubits,
    'n_configs':nconfigs,
    'n_qubits_n':Nqubits_n,
    'n_qubits_p':Nqubits_p,
    'Nshift':Nshift,
    'states':states,
    'coeffs':coeffs
}

output_file = f'{args.nucleus}.btrwfn.npz'
#onp.savez(file=output_file,**zdata)
onp.savez_compressed(file=output_file,**zdata)
print(f"Data saved to: {output_file} | n_configs: {zdata['n_configs']}")

#print(states, states.shape)
#print(coeffs, coeffs.shape)
# Print the results
#for i, record in enumerate(data):
#    print(f"Line {i + 1}: Integers: {record[:2]}, Float: {record[2]}")