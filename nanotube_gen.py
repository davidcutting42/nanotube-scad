# nanotube_gen.py
# Written by David Cutting
# Version 0.1, 5/6/18

# Nanotube generation utility. Takes a list of coordinates in a .txt file from
# avogadro, removes preceding C and all whitespace, and then creates an openscad
# file that contains all atoms and all bonds.

from solid import *
from math import *
import re
import sys

sys.setrecursionlimit(10000)

scale = 5   # All given coordinates are multiplied by this, and the result is
            # assumed to be in mm
dia = 4     # Diameter of the bond cylinders
sphere_d = 6    # Diameter of the atoms
bond_length = 1.421 # Calculated length of the bonds. To find this, run bond_length_util and pick the mode
bond_length_err = 0.05 # Bond length is allowed within bond_length plus of minus this

fname = raw_input("File Name (.txt, do not include extension): ")
f = open(fname + ".txt", "r")

atom_coord = []

for line in f:
    exp = re.compile("(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+")
    string = exp.search(line)
    if string:
        atom_coord.append([float(string.group(1)),
        float(string.group(2)),
        float(string.group(3))])

tube_solid = translate([0,0,0])

def bond_length_util():
    for atom in range(0,len(atom_coord)-1):
        coord = atom_coord[atom]
        cooord = atom_coord[atom+1]
        add = sqrt(pow(coord[0]-cooord[0],2)+pow(coord[1]-cooord[1],2)+pow(coord[2]-cooord[2],2))
        print add

# bond_length_util() # Uncomment to print all bond lengths between one atom and the following.

for atom in range(0,len(atom_coord)):
    coord = atom_coord[atom]
    atom_gen = sphere(d=sphere_d)
    atom_gen = translate(v=[coord[0]*scale, coord[1]*scale, coord[2]*scale])(atom_gen)
    tube_solid += atom_gen
    for atom_bond in range(0,len(atom_coord)):
        bond_coord = atom_coord[atom_bond]
        bond_len = sqrt(pow(coord[0]-bond_coord[0],2)+pow(coord[1]-bond_coord[1],2)+pow(coord[2]-bond_coord[2],2))
        if(bond_len > bond_length-bond_length_err and bond_len < bond_length+bond_length_err):

            bond_solid = cylinder(h=bond_len*scale, d=dia, center=False)
            diff_x = coord[0]*scale-bond_coord[0]*scale
            diff_y = coord[1]*scale-bond_coord[1]*scale
            diff_z = coord[2]*scale-bond_coord[2]*scale


            yaw = degrees(atan2(diff_y, diff_x))
            pitch = 270-degrees(atan2(diff_z, sqrt(diff_x**2 + diff_y**2)))

            bond_solid = rotate([0,pitch, 0])(bond_solid)
            bond_solid = rotate([0, 0, yaw])(bond_solid)
            bond_solid = translate([coord[0]*scale, coord[1]*scale, coord[2]*scale])(bond_solid)


            tube_solid += bond_solid

segments = raw_input("Set Segments? (y/n): ")
if(segments == 'y'):
    scad_render_to_file(tube_solid,
                                filepath=fname+".scad",
                                file_header='$fn = 50;',
                                include_orig_code=False)
else:
    scad_render_to_file(tube_solid,
                                filepath=fname+".scad",
                                include_orig_code=False)
