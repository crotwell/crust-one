
from profile import Layer, CrustOneProfile, CrustOne

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
                            bnds = bnds_file.readline().strip().split()
                            vp = vp_file.readline().split()
                            vs = vs_file.readline().split()
                            rho = rho_file.readline().split()
                            layers = []
                            for i in range(len(vp)):
                                layers.append(Layer(bnds[i], bnds[i+1], vp[i], vs[i], rho[i]))
                            lat = 89.5f-latIdx
                            lon = -179.5f+lonIdx
                            profile = Crust1Profile(lat, lon, layers)
                            profiles[f"{lat}/{lon}"] = profile
    return CrustOne(profiles)
