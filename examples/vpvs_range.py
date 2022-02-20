#import sys
#sys.path.append("src")
import crustone

c1 = crustone.parse()
min=9999
max=-1
for p in c1.profiles.values():
    vpvs = p.avg_vpvs(includeIceWater=False)
    #print(f"{vpvs:3.2f},{p.lat},{p.lon}")
    if vpvs > max:
        max = vpvs
    if vpvs < min:
        min = vpvs
print(f"Crust1.0 vp/vs Min: {min:3.2f},  Max: {max:3.2f}")


c2 = crustone.CrustTwo()

min=9999
max=-1
for p in c2.profiles.values():
    vpvs = p.asProfile().avg_vpvs(includeIceWater=False)
    no_comma = p.name.replace(',','\,')
    #print(f"{vpvs:3.2f},{p.code},{no_comma}")
    if vpvs > max:
        max = vpvs
    if vpvs < min:
        min = vpvs
print(f"Crust2.0 vp/vs Min: {min:3.2f},  Max: {max:3.2f}")
