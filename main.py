import numpy as np
import astropy.units as u
from astropy import constants
from astropy.time import Time
from astroquery.jplhorizons import Horizons
from vpython import *

def acc_12(p1, p2, m2, G):
    r = p1 - p2
    return -G * m2 / mag2(r) * norm(r)

class Body():
    def __init__(self, ID, name, mass, radius, color, t):
        self.ID = ID
        self.mass = mass
        self.radius = radius
        self.color = color
        self.q = Horizons(id=self.ID, location="@sun", epochs=t.tdb.jd).vectors()
        self.pos = vec(self.q["x"].to("km").value[0], self.q["y"].to("km").value[0], self.q["z"].to("km").value[0])
        self.v = vec(self.q["vx"].to("km / s").value[0], self.q["vy"].to("km / s").value[0], self.q["vz"].to("km / s").value[0])
        self.a = vec(0, 0, 0)
        self.body = sphere(pos=self.pos, v=self.v, mass=self.mass, radius=np.log(self.radius)*8e5, color=self.color, 
                           make_trail=True, trail_color=self.color, trail_radius=8e5, retain=trail_length, interval=trail_interval)
        self.label = label(pos=self.pos, text=name, xoffset=8, yoffset=8, space=self.radius, height=12,
                           color=vec(1, 1, 1), opacity=0, box=False, line=False)
    def update(self, dt):   
        self.dt = dt.value
        self.a = acc_12(self.body.pos, bodys[0].pos, bodys[0].mass, G)
        self.v += self.a * self.dt
        self.body.pos += self.v * self.dt
        self.label.pos = self.body.pos

def init():
    global bodys, t, running, reseting
    for i, name in enumerate(names):
        planet = np.load("./data/"+name+".npy", allow_pickle=True).item()
        bodys[i].body.visible = False
        bodys[i].label.visible = False
        bodys[i].body.clear_trail()
        bodys[i].__init__(planet["ID"], planet["name"], planet["mass"], planet["radius"], planet["color"], t_start)
    ecliptic_plane.visible = False
    checkbox_label.checked = True
    checkbox_trail.checked = True
    checkbox_ecliptic.checked = False
    slider_trail.value = trail_length
    length_trail(slider_trail)
    scene.range = 1.2*mag(bodys[-1].pos)
    scene.forward = vec(0, 0, -1)
    t = t_start
    running = True
    reseting = False

def run_pause(btn_run_pause):
    global running
    running = not running
    if running: btn_run_pause.text = "Pause"
    else: btn_run_pause.text = "Run"

def reset(btn_reset):
    global reseting
    reseting = not reseting

def shutdown(btn_stop):
    global going
    going = not going

def view_label(checkbox_label):
    for body in bodys:
        body.label.visible = not body.label.visible

def view_trial(checkbox_trail):
    for body in bodys:
        body.body.clear_trail()
        body.body.make_trail = not body.body.make_trail

def view_ecliptic(checkbox_ecliptic):
    ecliptic_plane.visible = not ecliptic_plane.visible

def length_trail(slider_trail):
    for body in bodys:
        body.body.retain = slider_trail.value
    text_trail.text = " {} Earth Days".format(str(int(dt.value*trail_interval*slider_trail.value/86400)))

def clear_screen():
    btn_run_pause.delete()
    btn_reset.delete()
    btn_stop.delete()
    checkbox_label.delete()
    checkbox_trail.delete()
    slider_trail.delete()
    scene.delete()
    scene.title = ""
    scene.caption = "Solar System Planetary Orbit Simulation has stopped."

#%% Main code
# parameter and initialize value
G = constants.G.to("km3 / (kg s2)").value
t_start = Time("2023-01-01")
dt = 60*60 * u.s
trail_interval = 24
trail_length = 50
running = True
reseting = False
going = True

# initialize canvas
scene = canvas(title="Solar System Planetary Orbit Simulation\n", width=600, height=600, background=color.black, autoscale = False)
text_time = wtext(pos=scene.title_anchor, text=t_start.strftime("%Y-%m-%d %H:%M:%S"))
names = ["Sun", "Mercury", "Venus", "Earth", "Mars"] # , "Jupiter", "Saturn", "Uranus", "Neptune"
bodys = []
for i, name in enumerate(names):
    planet = np.load("./data/"+name+".npy", allow_pickle=True).item()
    bodys.append(Body(planet["ID"], planet["name"], planet["mass"], planet["radius"], planet["color"], t_start))
scene.range = 1.2*mag(bodys[-1].pos)
background = sphere(texture="./fig/background.jpg", radius=5*mag(scene.center - scene.camera.pos), shininess=0)
ecliptic_plane = cylinder(pos=vec(0, 0, -1), axis=vec(0, 0, 1), radius=1.2*mag(bodys[-1].pos), color=color.yellow, opacity=0.2, shininess=0, visible = False)
btn_run_pause = button(pos=scene.caption_anchor, text="Pause", bind=run_pause)
btn_reset = button(pos=scene.caption_anchor, text="Reset", bind=reset)
btn_stop = button(pos=scene.caption_anchor, text="Shutdown", bind=shutdown)
scene.append_to_caption("\nView Settings:\n")
checkbox_label = checkbox(pos=scene.caption_anchor, text="Label ", checked=True, bind=view_label)
checkbox_trail = checkbox(pos=scene.caption_anchor, text="Trail ", checked=True, bind=view_trial)
checkbox_ecliptic = checkbox(pos=scene.caption_anchor, text="Ecliptic Plane ", checked=False, bind=view_ecliptic)
scene.append_to_caption("\nTrail Length: ")
slider_trail = slider(pos=scene.caption_anchor, min=0, max=100, value=trail_length, bind=length_trail)
text_trail = wtext(pos=scene.caption_anchor, text=" {} Earth Days".format(str(int(dt.value*trail_interval*trail_length/86400))))

# simulation
t = t_start
while going:
    rate(5*24)
    if running:
        for body in bodys[1:]:
            body.update(dt)
        text_time.text = t.strftime("%Y-%m-%d %H:%M:%S")
        t += dt
    if reseting:
        init()
    if mag(scene.center - scene.camera.pos) > background.radius:
        background.visible = False
    else:
        background.visible = True
clear_screen()