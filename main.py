import chemcoord
import numpy as np
import pandas


def convert_gjf_to_molecule(filename):
    coords = pandas.read_table(
        filename,
        delim_whitespace=True,
        names=('atom', 'x', 'y', 'z'),
        dtype={'atom': str, 'x': np.float64, 'y': np.float64, 'z': np.float64},
    )
    return chemcoord.Cartesian(frame=coords)


def get_coords(coords, atom_index):
    return np.array(coords.loc[atom_index, 'x':])


def get_bond_vector(coords, atom1, atom2):
    return get_coords(coords, atom1) - get_coords(coords, atom2)


def find_atom_with_neighbours(molecule, atom=None, neighbours=[]):
    bonds = molecule.get_bonds()
    for atom_index in bonds:
        if atom and molecule.loc[atom_index, 'atom'] != atom:
            continue

        connected = {molecule.loc[i, 'atom']: i for i in bonds[atom_index]}
        if neighbours.issubset(connected):
            return atom_index, connected


if __name__ == '__main__':
    molecule = convert_gjf_to_molecule('input.gjf')
    index, neighbours = find_atom_with_neighbours(molecule, 'C', {'C', 'N', 'O'})
    rotation_vector = get_bond_vector(molecule, index, neighbours['N'])
    print(rotation_vector)
