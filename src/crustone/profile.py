from itertools import accumulate
import math

class Layer:
    def __init__(self, topDepth, botDepth, vp, vs, rho):
        self.topDepth = topDepth
        self.botDepth = botDepth
        self.vp = float(vp)
        self.vs = float(vs)
        self.rho = float(rho)
    def thick(self):
        return self.botDepth-self.topDepth

class CrustOneProfile:
    def __init__(self, lat, lon, layers):
        self.lat = lat
        self.lon = lon
        self.layers = layers
    def avg_vp(self, includeIceWater=False):
        travelTime = 0;
        if includeIceWater:
            layers = self.layers[:-1]
        else:
            layers = self.layers[2:-1]
        for layer in layers:
            travelTime += layer.vp*layer.thick();
        return travelTime/self.crust_thick();
    def avg_vs(self, includeIceWater=False):
        travelTime = 0;
        if includeIceWater:
            layers = self.layers[:-1]
        else:
            layers = self.layers[2:-1]
        for layer in layers:
            vel = layer.vs
            if layer.vs == 0.0:
                if (includeIceWater or layer.thick() == 0):
                    # water? use vp
                    vel = layer.vp
                else:
                    raise Exception(f"Water layer, but includeIceWater=False, {self.lat}/{self.lon} {layer.thick()}")
            travelTime += vel*layer.thick();
        return travelTime/self.crust_thick();
    def avg_vpvs(self, includeIceWater=False):
        return self.avg_vp(includeIceWater)/self.avg_vs(includeIceWater)
    def crust_thick(self):
        # last layer is the halfspace (mantle), so topDepth is the moho depth
        return self.layers[-1].topDepth-self.layers[0].topDepth
    def elevation(self):
        return -1*self.layers[0].topDepth
    def __str__(self):
        s = f"Crust1.0 {self.lat}/{self.lon}\n"
        for layer in self.layers[:-1]:
            s += f"{round(layer.thick(), 2)} ({layer.topDepth} to {layer.botDepth}), {layer.vp} {layer.vs} {layer.rho}\n"
        layer = self.layers[-1]
        s += f"0 ({layer.topDepth} as halfspace), {layer.vp} {layer.vs} {layer.rho}"
        return s
    def as_nd_model(self, bottom=77.5, includeIceWater=False):
        """
        print profile as .nd style model, for use by TauP for example.
        bottom is the depth for the bottom of the uppermost layer in the mantle
        as mantle in Crust1.0 is a halfspace. This helps when merging to avoid
        having a partial crustal layer leak in from the original global model.
        if includeIceWater is false, then the model starts at the bottom of
        the ocean, eliminating the first two layers, which are ice and water.
        """
        if includeIceWater:
            layers = self.layers
        else:
            layers = self.layers[2:]
        s = f"# Crust1.0 {self.lat}/{self.lon} ice-water={includeIceWater}\n"
        for layer in layers[:-1]:
            if layer.thick() != 0.0:
                s += f"{layer.topDepth:5.2f} {layer.vp:5.2f} {layer.vs:5.2f} {layer.rho:5.2f}\n"
                s += f"{layer.botDepth:5.2f} {layer.vp:5.2f} {layer.vs:5.2f} {layer.rho:5.2f}\n"
        # only top of mantle layer
        layer = self.layers[-1]
        s += "mantle\n"
        s += f"{layer.topDepth:5.2f} {layer.vp:5.2f} {layer.vs:5.2f} {layer.rho:5.2f}\n"
        if bottom > layer.topDepth:
            s += f"{bottom:5.2f} {layer.vp:5.2f} {layer.vs:5.2f} {layer.rho:5.2f}\n"
        return s

class CrustOne:
    def __init__(self, profiles):
        self.profiles = profiles
    def find_profile(self, lat, lon):
        if lat > 90 or lat < -90:
            raise Exception(f"Lat must be between -90 and 90 but was {lat}")
        if lon < -180 or lon > 360:
            raise Exception(f"Lon must be between -180 and 360 but was {lon}")
        lat_center = round(lat+.5)-0.5
        lon_center = round(lon+.5)-0.5
        if lon_center > 180:
            lon_center = lon_center - 360
        if lat_center < -90:
            lat_center = -89.5
        return self.profiles[f"{lat_center}/{lon_center}"]
