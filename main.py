import chemcoord
import numpy as np
import pandas

coords = pandas.read_table(
    'input.txt',
    delim_whitespace=True,
    names=('atom', 'x', 'y', 'z'),
    dtype={'atom': str, 'x': np.float64, 'y': np.float64, 'z': np.float64},
)
molecule = chemcoord.Cartesian(frame=coords)
bonds = molecule.get_bonds()

rotate_bond = None

for atom_index in bonds:
    if coords.loc[atom_index, 'atom'] != 'C':
        continue

    connected = {coords.loc[i, 'atom']: i for i in bonds[atom_index]}
    if {'C', 'N', 'O'}.issubset(connected):
        rotate_bond = (atom_index, connected['N'])
        break

print(rotate_bond)
