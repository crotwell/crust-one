from itertools import accumulate

class Layer:
    def __init__(self, topDepth, botDepth, vs, vs, rho):
        self.topDepth = topDepth
        self.botDepth = botDepth
        self.vp = vp
        self.vs = vs
        self.rho = rho
    def thick(self):
        return self.botDepth-self.topDepth

class CrustOneProfile:
    def __init__(self, lat, lon, layers):
        self.lat = lat
        self.lon = lon
        self.layers = layers
    def avg_vp(self):
        travelTime = 0;
        for layer in self.layers:
            travelTime += layer.vp*layer.thick();
        }
        # last layer is the halfspace (mantle), so topDepth is the moho depth
        return travelTime/self.layers[-1].topDepth;
    def avg_vs(self, layer_var):
        travelTime = 0;
        for layer in self.layers:
            travelTime += layer.vs*layer.thick();
        }
        return travelTime/self.crust_thick();
    def crust_thick(self):
        # last layer is the halfspace (mantle), so topDepth is the moho depth
        return layers[-1].topDepth

class CrustOne:
    def __init__(self, profiles):
        self.profiles = profiles
    def find_profile(self, lat, lon):
        lat_center = math.round(lat*2)/2
        lon_center = math.round(lon*2)/2
        return self.profiles(f"{lat_center}/{lon_center}")
