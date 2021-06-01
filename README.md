# Rotate molecules

The purpose of this repo's code is to rotate part of molecule with the glycosidic bond around C-N bond.

## Note

This is a made-to-order project. It won't be maintained in the future.

## Main problem

The main difficulty when rotating an atom (a point in 3D space) around a C-N bond was that the rotation axis isn't always passing through the origin.
I solved this by following this steps:
1. Subtract N atom's coordinates from each of the atoms coordinates.
   1. So the N atom is now in the origin, and the rotation axis is passing through the center.
2. Rotate each atom around rotation axis.
3. Add N atom's coordinates to each of the atoms coordinates.
   1. So the N atom is now back in its place.
