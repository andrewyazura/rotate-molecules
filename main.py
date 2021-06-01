import math

import chemcoord
import numpy as np
import pandas
from progress.bar import PixelBar as Bar


def convert_gjf_to_molecule(filename):
    coords = pandas.read_table(
        filename,
        delim_whitespace=True,
        names=('atom', 'x', 'y', 'z'),
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


def rotation_matrix(axis, angle):
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(angle / 2.0)
    b, c, d = -axis * math.sin(angle / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array(
        [
            [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
        ]
    )


def rotate(axis, point, angle):
    return np.dot(rotation_matrix(axis, angle), point)


def rotate_molecule_part(coords, axis, offset, angle):
    result = coords.copy()
    for index, atom in result.iterrows():
        atom_coords = np.array(atom['x':])
        atom_coords = atom_coords - offset

        if not atom_coords.all():
            continue

        d = math.degrees(angle_between_vectors(axis, atom_coords))
        if d < 90 or d > 270:
            atom_coords = rotate(axis, atom_coords, angle)
            atom_coords = atom_coords + offset
            result.loc[index, 'x':] = atom_coords

    return result


if __name__ == '__main__':
    molecule = convert_gjf_to_molecule('input.gjf')
    index, neighbours = find_atom_with_neighbours(molecule, 'C', {'C', 'N', 'O'})
    rotation_axis = get_unit_vector(get_bond_vector(molecule, neighbours['N'], index))

    pbar = Bar('Processing', max=360)
    for angle in range(1, 361):
        rotate_molecule_part(
            molecule._frame.copy(),
            rotation_axis,
            get_coords(molecule, neighbours['N']),
            math.radians(angle),
        ).to_csv(
            f'results/rot-{angle}.gjf',
            sep=' ',
            float_format='%.8f',
            index=False,
            header=False,
        )
        pbar.next()

    pbar.finish()
    print('Done!')
