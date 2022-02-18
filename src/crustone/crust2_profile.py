
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from .data import crust2  # relative-import the *package* containing the templates
from .profile import Layer

class CrustTwoCodeProfile:
    def __init__(self, code, name, layers):
        self.code = code
        self.name = name
        self.layers = layers
    def asProfile(self, lat=-1, lon=-1):
        return CrustTwoProfile(lat, lon, self.code, self.name, self.layers)

class CrustTwoProfile:
    def __init__(self, lat, lon, code, name, layers):
        self.lat = lat
        self.lon = lon
        self.code = code
        self.name = name
        self.layers = layers
    def avg_vp(self):
        travelTime = 0;
        for layer in self.layers[:-1]:
            travelTime += layer.vp*layer.thick();
        return travelTime/self.crust_thick();
    def avg_vs(self):
        travelTime = 0;
        for layer in self.layers[:-1]:
            vel = layer.vs
            if layer.vs == 0.0:
                # water? use vp
                vel = layer.vp
            travelTime += vel*layer.thick();
        return travelTime/self.crust_thick();
    def avg_vpvs(self):
        return self.avg_vp()/self.avg_vs()
    def crust_thick(self):
        # last layer is the halfspace (mantle), so topDepth is the moho depth
        return self.layers[-1].topDepth-self.layers[0].topDepth
    def __str__(self):
        s = f"{self.code}/{self.name} for {self.lat}/{self.lon}\n"
        for layer in self.layers[:-1]:
            s += f"{round(layer.thick(), 2)} ({layer.topDepth} to {layer.botDepth}), {layer.vp} {layer.vs} {layer.rho}\n"
        layer = self.layers[-1]
        s += f"0 ({layer.topDepth} as halfspace), {layer.vp} {layer.vs} {layer.rho}"
        return s


class CrustTwo:
    def __init__(self):
        self.profiles = parse_key()
        self.type_key = parse_type()
    def find_profile(self, lat, lon):
        if lat > 90 or lat < -90:
            raise Exception(f"Lat must be between -90 and 90 but was {lat}")
        if lon < -180 or lon > 360:
            raise Exception(f"Lon must be between -180 and 360 but was {lon}")
        lat_center = round(lat/2.0)*2-1
        lon_center = round(lon/2.0)*2+1
        if lat_center < -89:
            # south pole is wrong in above calc
            lat_center = -89
        if lon_center > 180:
            # needs to be -180 to 180
            lon_center = lon_center - 360
        code = self.type_key[f"{lat_center}/{lon_center}"]
        code_profile = self.profiles[code]
        return CrustTwoProfile(lat_center, lon_center, code_profile.code, code_profile.name, code_profile.layers)


NUM_LATS=90
NUM_LONS=180

def parse_key():
    profiles = {}
    with pkg_resources.open_text(crust2, "CNtype2_key.txt") as key_file:
        lines = key_file.readlines()
        lines = lines[5:] # first 5 lines are info/labels
        num_keys = int(len(lines)/5)
        for j in range(num_keys):
            name_list = lines[5*j].split()
            code = name_list[0]
            name = " ".join(name_list[1:])
            vp = lines[5*j+1].split()
            vs = lines[5*j+2].split()
            rho = lines[5*j+3].split()
            thick = lines[5*j+4].split()
            thick[7] = 6371 - float(thick[8]) # replace .inf with radius of earth minus crust thick
            layers = []
            top_depth = 0
            for i in range(len(vp)):
                bot_depth = top_depth + float(thick[i])
                layers.append(Layer(top_depth, bot_depth, vp[i], vs[i], rho[i]))
                top_depth = bot_depth
            profiles[code] = CrustTwoCodeProfile(code, name, layers)
    return profiles



def parse_type():
    types = {}
    with pkg_resources.open_text(crust2, "CNtype2.txt") as type_file:
        lons = []
        lon_list = type_file.readline().split()
        for l in lon_list:
            lons.append(int(l))
        for lat in range(-90, 90, 2):
            type_list = type_file.readline().split()
            lat = int(type_list[0])
            for i in range(len(lons)):
                lon = lons[i]
                lat_center = round(lat/2.0)*2-1
                lon_center = round(lon/2.0)*2+1
                types[f"{lat_center}/{lon_center}"] = type_list[i+1]
    return types
