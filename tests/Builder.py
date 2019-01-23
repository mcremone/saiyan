import awkward
import uproot_methods

class Dangerousness(object):
    def __getattr__(self, name):
        return self[name]
    
class Methods(object):
    
    def match(self, cands, value):
        array1 = uproot_methods.TLorentzVectorArray.from_ptetaphim(self.pt,self.eta,self.phi,self.mass)
        array2 = uproot_methods.TLorentzVectorArray.from_ptetaphim(cands.pt,cands.eta,cands.phi,cands.mass)
        combinations = array1.cross(array2, nested=True)
        mask = (combinations.i0.delta_r(combinations.i1) <value)
        return mask.any()
    
    def closest(self, cands):
        array1 = uproot_methods.TLorentzVectorArray.from_ptetaphim(self.pt,self.eta,self.phi,self.mass)
        array2 = uproot_methods.TLorentzVectorArray.from_ptetaphim(cands.pt,cands.eta,cands.phi,cands.mass)
        combinations = array1.cross(array2, nested=True)
        if ((~(combinations.i0.eta ==0).flatten().flatten().all())|(~(combinations.i1.eta ==0).flatten().flatten().all()) ):
            criterium = combinations.i0.delta_phi(combinations.i1)
        else:
            criterium =combinations.i0.delta_r(combinations.i1)
        index_of_closest = criterium.argmin()
        return combinations.i1[index_of_closest]
        

def Initialize(items):
#        items = kwargs
    argkeys = items.keys()
    p4 = None
    if 'p4' in argkeys:
        p4 = items['p4']
        if not isinstance(p4,uproot_methods.TLorentzVectorArray):
            p4 = uproot_methods.TLorentzVectorArray.from_cartesian(p4[:,0],p4[:,1],
                                                                       p4[:,2],p4[:,3])

    elif 'pt' in argkeys and 'eta' in argkeys and 'phi' in argkeys and 'mass' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_ptetaphim(items['pt'],items['eta'],
                                                               items['phi'],items['mass'])
        del items['pt']
        del items['eta']
        del items['phi']
        del items['mass']

    elif 'pt' in argkeys and 'eta' in argkeys and 'phi' in argkeys and 'energy' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_ptetaphi(items['pt'],items['eta'],
                                                              items['phi'],items['energy'])
        del items['pt']
        del items['eta']
        del items['phi']
        del items['energy']

    elif 'px' in argkeys and 'py' in argkeys and 'pz' in argkeys and 'mass' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_xyzm(items['px'],items['py'],
                                                          items['pz'],items['mass'])
        del items['px']
        del items['py']
        del items['pz']
        del items['mass']

    elif 'pt' in argkeys and 'phi' in argkeys and 'pz' in argkeys and 'energy' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_cylindrical(items['pt'],items['phi'],
                                                                 items['pz'],items['energy'])
        del items['pt']
        del items['phi']
        del items['pz']
        del items['energy']

    elif 'px' in argkeys and 'py' in argkeys and 'pz' in argkeys and 'energy' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_cartesian(items['px'],items['py'],
                                                               items['pz'],items['energy'])
        del items['px']
        del items['py']
        del items['pz']
        del items['energy']

    elif 'p' in argkeys and 'theta' in argkeys and 'phi' in argkeys and 'energy' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_spherical(items['p'],items['theta'],
                                                               items['phi'],items['energy'])
        del items['p']
        del items['theta']
        del items['phi']
        del items['energy']

    elif 'p3' in argkeys and 'energy' in argkeys:
        p4 = uproot_methods.TLorentzVectorArray.from_p3(items['p3'],items['energy'])
        del items['p3']
        del items['energy']

    else:
        raise Exception('No valid definition of four-momentum')

    out = p4
    for name, value in items.items():
        out[name] = value

    if isinstance(out, awkward.JaggedArray):
        out.content.__class__ = type("Object", (Dangerousness, Methods, out.content.__class__), {})
        out.__class__ = type("Collection", (Dangerousness, Methods, out.__class__), {})
    else:
        out.__class__ = type("Object", (Dangerousness, Methods, out.__class__), {})

    return out



