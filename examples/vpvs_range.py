#import sys
#sys.path.append("src")
import crustone

c1 = crustone.parse()
min=9999
max=-1
for p in c1.profiles.values():
    vpvs = p.avg_vpvs()
    #print(f"{p.lat},{p.lon},{vpvs}")
    if vpvs > max:
        max = vpvs
    if vpvs < min:
        min = vpvs
print(f"Crust1.0 vp/vs Min: {min},  Max: {max}")


c2 = crustone.CrustTwo()

min=9999
max=-1
for p in c2.profiles.values():
    vpvs = p.asProfile().avg_vpvs()
    no_comma = p.name.replace(',','\,')
    #print(f"{p.code},{no_comma},{vpvs}")
    if vpvs > max:
        max = vpvs
    if vpvs < min:
        min = vpvs
print(f"Crust2.0 vp/vs Min: {min},  Max: {max}")
