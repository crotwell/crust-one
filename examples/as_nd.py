#import sys
#sys.path.append("src")
import crustone

c1 = crustone.parse()
p = c1.find_profile(31.1, -80.9)
print(p.as_nd_model())
