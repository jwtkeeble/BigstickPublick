from bidict import bidict

Z_to_nuc={0:'n',1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',
          11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',19:'K',20:'Ca',
          21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',27:'Co',28:'Ni',29:'Cu',30:'Zn',
          31:'Ga',32:'Ge',33:'As',34:'Se',35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr'
}

Z_to_nuc = bidict(Z_to_nuc)

import re

def get_A_and_symbol(s: str) -> str:
    match = re.match(r"(\d+)(\D+)", s)
    if match:
        A = match.group(1)
        sym = match.group(2)
        return int(A), sym
    raise ValueError("Invalid string")


#print(Z_to_nuc[32], Z_to_nuc.inverse['Ge'])
#print(get_A_and_symbol('30Ge'))