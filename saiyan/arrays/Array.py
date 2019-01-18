import awkward
import uproot_methods

def Initialize(**kwargs):
        items = kwargs
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

        return out

class Dangerousness(object):
    def __getattr__(self, name):
        return self[name]

class ObjectsArray(Dangerousness,awkward.Methods):
    def __init__(self, **kwargs):
        self = Initialize(**kwargs)
        # adding dangerousness to the ObjectArray
        self.__class__ = Methods.mixin(Dangerousness, self.__class__)

class CollectionsArray(Dangerousness,awkward.Methods):
    def __init__(self, **kwargs):
        self = Initialize(**kwargs)
        # adding dangerousness to the JaggedArray
        self.__class__ = Methods.mixin(Dangerousness, self.__class__)
        # adding dangerousness to the ObjectArray inside it
        self.content.__class__ = Methods.mixin(Dangerousness,, self.content.__class__)



