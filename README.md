# Rotate molecules

The purpose of this repo's code is to rotate a part of a molecule with the glycosidic bond around C-N bond. It creates 360 `.gjf` files, each file containing a modified molecule. 

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

## Example

Here is an example molecule. You can see the C-N bond in the middle.

<details>
   <summary>Preview</summary>
   
   Front view:
   
   ![image](https://user-images.githubusercontent.com/39884112/120292957-727fe280-c2cd-11eb-9067-904f65b1dc7f.png)
   
   Side view:
   
   ![image](https://user-images.githubusercontent.com/39884112/120294962-6137d580-c2cf-11eb-995b-b8a0e714b634.png)

</details>

The main goal is to rotate all the atoms above the C-N bond, while atoms below have to remained fixed.

<details>
   <summary>Preview</summary>
   
   ![image](https://user-images.githubusercontent.com/39884112/120293316-cdb1d500-c2cd-11eb-82ac-428361abf84a.png)

</details>

On the next image you can see rotation axis painted white, nitrogen atom as the origin point. To determine whether an atom should be rotated, an angle between a vector from the center nitrogene atom to the atom (marked yellow or red) and rotation axis (white) is calculated. If the angle is greater than 90 and less than 270, the atom is below the nitrogen atom and should be fixed.

<details>
   <summary>Preview</summary>
   
   ![image](https://user-images.githubusercontent.com/39884112/120294826-436a7080-c2cf-11eb-97b2-3dffea1d6a76.png)

</details>
