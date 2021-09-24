
from .profile import Layer, CrustOneProfile, CrustOne

NUM_LATS=180
NUM_LONS=360

def parse(datadir):
    profiles = {}
    with open(datadir+"/crust1.bnds") as bnds_file:
        with open(datadir+"/crust1.vp") as vp_file:
            with open(datadir+"/crust1.vs") as vs_file:
                with open(datadir+"/crust1.rho") as rho_file:
                    for lat_idx in range(NUM_LATS):
                        for lon_idx in range(NUM_LONS):
                            strList = bnds_file.readline().strip().split()
                            bnds = [ -1*float(x) for x in strList]
                            bnds.append(6371)
                            strList = vp_file.readline().split()
                            vp = [float(x) for x in strList]
                            strList = vs_file.readline().split()
                            vs = [float(x) for x in strList]
                            strList = rho_file.readline().split()
                            rho = [float(x) for x in strList]
                            layers = []
                            for i in range(len(vp)):
                                layers.append(Layer(bnds[i], bnds[i+1], vp[i], vs[i], rho[i]))
                            lat = 89.5-lat_idx
                            lon = -179.5+lon_idx
                            profile = CrustOneProfile(lat, lon, layers)
                            profiles[f"{lat}/{lon}"] = profile
    return CrustOne(profiles)
