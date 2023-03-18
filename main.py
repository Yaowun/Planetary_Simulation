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
                           make_trail=True, trail_color=self.color, trail_radius=8e5, retain=25, interval=24)
        # self.trail = attach_trail(self.body, color=self.color, radius=8e5, retain=100, interval=24)
        self.label = label(pos=self.pos, text=name, xoffset=8, yoffset=8, space=self.radius, height=12,
                           color=vec(1, 1, 1), opacity=0, box=False, line=False)
    def update(self, dt):   
        self.dt = dt.value
        self.a = acc_12(self.body.pos, bodys[0].pos, bodys[0].mass, G)
        self.v += self.a * self.dt
        self.body.pos += self.v * self.dt
        self.label.pos = self.body.pos

def run_pause(btn_run_pause):
    global running
    running = not running
    if running: btn_run_pause.text = "Pause"
    else: btn_run_pause.text = "Run"

def view_label(checkbox_label):
    for body in bodys:
        body.label.visible = not body.label.visible

def view_trial(checkbox_trail):
    for body in bodys:
        body.body.clear_trail()
        body.body.make_trail = not body.body.make_trail

def trail_length(slider_trail):
    for body in bodys:
        body.body.retain = slider_trail.value

#%% Main code
# parameter and initialize value
G = constants.G.to("km3 / (kg s2)").value
t = Time("2023-01-01")
dt = 60*60 * u.s
running = True

# initialize canvas
scene = canvas(title="Solar System Planetary Orbit Simulation\n", width=600, height=600, background=color.black, autoscale = False)
text_time = wtext(pos=scene.title_anchor, text=t.strftime("%Y-%m-%d %H:%M:%S"))
names = ["Sun", "Mercury", "Venus", "Earth", "Mars"] # , "Jupiter", "Saturn", "Uranus", "Neptune"
bodys = []
for i, name in enumerate(names):
    body = np.load("./data/"+name+".npy", allow_pickle=True).item()
    bodys.append(Body(body["ID"], body["name"], body["mass"], body["radius"], body["color"], t))
scene.range = 1.2*mag(bodys[-1].pos)
background = sphere(texture="./fig/background.jpg", radius=5*mag(scene.center - scene.camera.pos), shininess=0)
btn_run_pause = button(pos=scene.caption_anchor, text="Pause", bind=run_pause)
scene.append_to_caption("\nView Settings:\n")
checkbox_label = checkbox(pos=scene.caption_anchor, text="Label ", checked=True, bind=view_label)
checkbox_trail = checkbox(pos=scene.caption_anchor, text="Trail ", checked=True, bind=view_trial)
scene.append_to_caption("\nTrail Length: ")
slider_trail = slider(pos=scene.caption_anchor, min=0, max=100, value=25, bind=trail_length)

# simulation
while True:
    rate(5*24)
    if running:
        for body in bodys[1:]:
            body.update(dt)
        text_time.text = t.strftime("%Y-%m-%d %H:%M:%S")
    if mag(scene.center - scene.camera.pos) > background.radius:
        background.visible = False
    else:
        background.visible = True
    t += dt