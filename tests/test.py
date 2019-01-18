import uproot, uproot_methods
from ..saiyan.arrays.Array import *


f = uproot.open("nano_5.root")
t = f["Events"]

pt = t.array("Electron_pt")
eta = t.array("Electron_eta")
phi = t.array("Electron_phi")
mass = t.array("Electron_mass")

e_columns = {'pt':'pt','eta':'eta','phi':'phi','mass':'mass'}
e = CollectionsArray(e_columns)


