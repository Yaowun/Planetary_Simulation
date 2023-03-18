import numpy as np
from vpython import vec

# Sun: https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
# Mercury: https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html
# Venus: https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
# Earth: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
# Mars: https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
# Jupiter: https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html
# Saturn: https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html
# Uranus: https://nssdc.gsfc.nasa.gov/planetary/factsheet/uranusfact.html
# Neptune: https://nssdc.gsfc.nasa.gov/planetary/factsheet/neptunefact.html

Sun = {"ID": 10, "name": "Sun", "mass": 1988500e24, "radius":695700, "color": vec( 1, .6, .4)}
Mercury = {"ID": 199, "name": "Mercury", "mass": 0.33010e24, "radius":2439.7, "color": vec(.8, .8, .8)}
Venus = {"ID": 299, "name": "Venus", "mass": 4.8673e24, "radius":6051.8, "color": vec(.8, .6, 0)}
Earth = {"ID": 399, "name": "Earth", "mass": 5.9722e24, "radius":6371.000, "color": vec(0, .4, 1)}
Mars = {"ID": 499, "name": "Mars", "mass": 0.64169e24, "radius":3389.5, "color": vec(1, .8, .4)}
Jupiter = {"ID": 599, "name": "Jupiter", "mass": 1898.13e24, "radius":69911, "color": vec(1, .8, .6)}
Saturn = {"ID": 699, "name": "Saturn", "mass": 568.32e24, "radius":58232, "color": vec(1, .6, 0)}
Uranus = {"ID": 799, "name": "Uranus", "mass": 86.811e24, "radius":25362, "color": vec(.8, 1, 1)}
Neptune = {"ID": 899, "name": "Neptune", "mass": 102.409e24, "radius":24622, "color": vec(.2, .2, 1)}

np.save("Sun.npy", Sun)
np.save("Mercury.npy", Mercury)
np.save("Venus.npy", Venus)
np.save("Earth.npy", Earth)
np.save("Mars.npy", Mars)
np.save("Jupiter.npy", Jupiter)
np.save("Saturn.npy", Saturn)
np.save("Uranus.npy", Uranus)
np.save("Neptune.npy", Neptune)