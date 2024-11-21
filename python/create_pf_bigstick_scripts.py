import os
import numpy as np
from utils import Z_to_nuc

def create_bigstick_file(N: int,Z: int) -> str:
    A = N+Z
    sym = Z_to_nuc[Z]
    iso = f'{A}{sym}'
    input_file = f'input_{iso}.bigstick'
    Jz2 = 0 if A%2==0 else 1
    with open(input_file, "w") as f:
        f.write('t         ! menu choice ')
        f.write(f'{iso}')
        f.write('pf        !  name of .sps file ')
        f.write(f'{Z} {N}  ! # of valence protons, neutrons ')
        f.write(f'{Jz2}    ! 2 x Jz of systems ')
        f.write('0         !  LANCZOS FRAGMENT SIZE (0 = use default)')
        f.write('kb3g                        ')
        f.write('end                         ')
        f.write('ld    ! Lanczos menu option ')
        f.write('1 100 ! # states to keep, max # iterations ')
        f.write(' ! Not optimizing initial pivot vector ')
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