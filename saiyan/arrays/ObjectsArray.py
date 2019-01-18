import awkward
import uproot_methods
import numpy as np

def _fast_pt(p4):
    """ quick pt calculation for caching """
    return np.hypot(p4.x,p4.y)

def _fast_eta(p4):
    """ quick eta calculation for caching """
    px = p4.x
    py = p4.y
    pz = p4.z
    pT = np.sqrt(px*px + py*py)
    return np.arcsinh(pz/pT)

def _fast_phi(p4):
    """ quick phi calculation for caching """
    return np.arctan2(p4.y,p4.x)

def _fast_mass(p4):
    """ quick mass calculation for caching """
    px = p4.x
    py = p4.y
    pz = p4.z
    en = p4.t
    p3mag2 = (px*px + py*py + pz*pz)
    return np.sqrt(np.abs(en*en - p3mag2))



class ObjectsArray(awkward.Methods):

    def __init__(self, **kwargs):

        items = kwargs
        argkeys = items.keys()
        
        p4 = None
        
        if 'p4' in argkeys:
            p4 = items['p4']
            if not isinstance(p4,uproot_methods.TLorentzVector):
                p4 = uproot_methods.TLorentzVector.from_cartesian(p4[:,0],p4[:,1],
                                                                       p4[:,2],p4[:,3])

        elif 'pt' in argkeys and 'eta' in argkeys and 'phi' in argkeys and 'mass' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_ptetaphim(items['pt'],items['eta'],
                                                                   items['phi'],items['mass'])
            del items['pt']
            del items['eta']
            del items['phi']
            del items['mass']

        elif 'pt' in argkeys and 'eta' in argkeys and 'phi' in argkeys and 'energy' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_ptetaphi(items['pt'],items['eta'],
                                                                  items['phi'],items['energy'])
            del items['pt']
            del items['eta']
            del items['phi']
            del items['energy']

        elif 'px' in argkeys and 'py' in argkeys and 'pz' in argkeys and 'mass' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_xyzm(items['px'],items['py'],
                                                              items['pz'],items['mass'])
            del items['px']
            del items['py']
            del items['pz']
            del items['mass']

        elif 'pt' in argkeys and 'phi' in argkeys and 'pz' in argkeys and 'energy' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_cylindrical(items['pt'],items['phi'],
                                                                     items['pz'],items['energy'])
            del items['pt']
            del items['phi']
            del items['pz']
            del items['energy']

        elif 'px' in argkeys and 'py' in argkeys and 'pz' in argkeys and 'energy' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_cartesian(items['px'],items['py'],
                                                                   items['pz'],items['energy'])
            del items['px']
            del items['py']
            del items['pz']
            del items['energy']

        elif 'p' in argkeys and 'theta' in argkeys and 'phi' in argkeys and 'energy' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_spherical(items['p'],items['theta'],
                                                                   items['phi'],items['energy'])
            del items['p']
            del items['theta']
            del items['phi']
            del items['energy']

        elif 'p3' in argkeys and 'energy' in argkeys:
            p4 = uproot_methods.TLorentzVector.from_p3(items['p3'],items['energy'])
            del items['p3']
            del items['energy']

        else:
            raise Exception('No valid definition of four-momentum')

        self = p4
        for arg in argkeys: self[arg] = items[arg]


    def __getattr__(self, name):
        return self[name]
