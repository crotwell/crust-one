#import sys
#sys.path.append("src")
import crustone

c1 = crustone.parse()
p = c1.find_profile(31.1, -80.9)
print(f"{p.lat} {p.lon} {p.avg_vp()} {p.avg_vs()}  {p.crust_thick()}")
print("Profile:")
print(p)
