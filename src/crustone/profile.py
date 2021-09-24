from itertools import accumulate
import math

class Layer:
    def __init__(self, topDepth, botDepth, vp, vs, rho):
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
        for layer in self.layers[:-1]:
            travelTime += layer.vp*layer.thick();
        return travelTime/self.crust_thick();
    def avg_vs(self):
        travelTime = 0;
        for layer in self.layers[:-1]:
            travelTime += layer.vs*layer.thick();
        return travelTime/self.crust_thick();
    def crust_thick(self):
        # last layer is the halfspace (mantle), so topDepth is the moho depth
        return self.layers[-1].topDepth-self.layers[0].topDepth
    def __str__(self):
        s = f"{self.lat}/{self.lon}\n"
        for layer in self.layers[:-1]:
            s += f"{round(layer.thick(), 2)} ({layer.topDepth} to {layer.botDepth}), {layer.vp} {layer.vs} {layer.rho}\n"
        layer = self.layers[-1]
        s += f"0 ({layer.topDepth} as halfspace), {layer.vp} {layer.vs} {layer.rho}"
        return s

class CrustOne:
    def __init__(self, profiles):
        self.profiles = profiles
    def find_profile(self, lat, lon):
        lat_center = round(lat+.5)-0.5
        lon_center = round(lon+.5)-0.5
        print(f"in: {lat}/{lon} center: {lat_center}/{lon_center}")
        return self.profiles[f"{lat_center}/{lon_center}"]
