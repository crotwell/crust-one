#import sys
#sys.path.append("src")
import crustone

c1 = crustone.parse()
p = c1.find_profile(31.1, -80.9)
print(f"Crust1: lat:{p.lat} lon:{p.lon} average vp:{p.avg_vp()} vs:{p.avg_vs()}  thick:{p.crust_thick()}")
print("Crust1 Profile:")
print(p)

print()

c2 = crustone.CrustTwo()
lat = 31.1
lon = -81.9
p = c2.find_profile(lat, lon)
print(f"Crust2: lat:{p.lat} lon:{p.lon} vp:{p.avg_vp()} vs:{p.avg_vs()}  thick:{p.crust_thick()}")
print("Crust2 Profile:")
print(p)
