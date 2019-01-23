import uproot, uproot_methods
from Builder import Initialize

file = uproot.open("nano_5.root")
tree = file["Events"]

e = Initialize({'pt':tree.array("Electron_pt"),
              'eta':tree.array("Electron_eta"),
              'phi':tree.array("Electron_phi"),
                'mass':tree.array("Electron_mass"),
              'iso':tree.array('Electron_pfRelIso03_all')})
mu = Initialize({'pt':tree.array("Muon_pt"),
                 'eta':tree.array("Muon_eta"),
                 'phi':tree.array("Muon_phi"),
                 'mass':tree.array("Muon_mass")})
met = Initialize({'pt':tree.array("MET_pt"),
                  'eta':0,
                  'phi':tree.array("MET_phi"),
                  'mass':0})

print(met.eta)
#print(e.match(mu,0.4))
#print(e.iso)    
#print(met.closest(e))
