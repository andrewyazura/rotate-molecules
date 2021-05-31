# Rotate molecules

The purpose of this repo's code is to rotate part of molecule with the glycosidic bond around C-N bond.

## Main problem

The main difficulty with rotating an atom (a point in 3D space) was that the rotation axis isn't always passing through the origin. 
To solve this, I made a rotation vector (coordinates of carbon atom - coordinates of nitrogen atom) and then moved each nucleus so that the nitrogen is in the center of the 3D space. 
After rotating around the vector, I moved each point back the same distance.
