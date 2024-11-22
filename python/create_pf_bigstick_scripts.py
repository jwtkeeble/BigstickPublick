import os
import numpy as np
from utils import Z_to_nuc

def create_bigstick_file(N: int,Z: int) -> str:
    A = N+Z
    sym = Z_to_nuc[Z]
    iso = f'{A}{sym}'
    input_file = f'input_{iso}.bigstick'
    
    NNcore=20
    ZZcore=20
    
    Zval = Z-ZZcore if (Z != 40) else 0
    Nval = N-NNcore if (N != 40) else 0

    Jz2 = 0 if A%2==0 else 1
    with open(input_file, "w") as f:
        f.write('t         ! menu choice \n')
        f.write(f'outputs/{iso}\n')
        f.write('pf        !  name of .sps file \n')
        f.write(f'{Zval} {Nval}  ! # of valence protons, neutrons \n')
        f.write(f'{Jz2}    ! 2 x Jz of systems \n')
        f.write('0         !  LANCZOS FRAGMENT SIZE (0 = use default)\n')
        f.write('kb3g                        \n')
        f.write('end                         \n')
        f.write('ld    ! Lanczos menu option \n')
        f.write('1 100 ! # states to keep, max # iterations \n')
        f.write(' ! Not optimizing initial pivot vector')
    return input_file

for Z in range(20,40,1):
    for N in range(Z,40,1): # NOTE: isospin symmetric
        A = N+Z
        sym = Z_to_nuc[Z]
        iso = f'{A}{sym}'
        file = create_bigstick_file(N,Z)
        print(f'Created: {file}')
        cmd = f'sbatch -J {iso} submit.sh --nucleus={iso}'
        print(f'Submitting SLURM: {cmd}')
        #os.system(command=cmd)