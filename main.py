import math

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


def get_unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    v1_u = get_unit_vector(v1)
    v2_u = get_unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def find_atom_with_neighbours(molecule, atom=None, neighbours=[]):
    bonds = molecule.get_bonds()
    for atom_index in bonds:
        if atom and molecule.loc[atom_index, 'atom'] != atom:
            continue

        connected = {molecule.loc[i, 'atom']: i for i in bonds[atom_index]}
        if neighbours.issubset(connected):
            return atom_index, connected


def rotate_molecule_part(coords, rotation_vector, offset, angle):
    result = coords.copy()
    print(result)
    print(offset)
    for index, atom in result.iterrows():
        atom_coords = np.array(atom['x':])
        atom_coords -= offset

        d = angle_between_vectors(rotation_vector, atom_coords)
        if d < math.pi / 2 or d > math.tau * 3 / 4:
            # rotate
            atom_coords += offset
            result.loc[index, 'x':] = atom_coords

    print(result)


if __name__ == '__main__':
    molecule = convert_gjf_to_molecule('input.gjf')
    index, neighbours = find_atom_with_neighbours(molecule, 'C', {'C', 'N', 'O'})
    rotation_vector = get_unit_vector(get_bond_vector(molecule, neighbours['N'], index))

    rotate_molecule_part(
        molecule._frame.copy(),
        rotation_vector,
        get_coords(molecule, neighbours['N']),
        math.radians(360),
    )
