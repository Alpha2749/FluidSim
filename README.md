# Interactive fluid particle simulator in Python & PyGame!
##### (Written for the Boot.dev 2025 Hackathon)


## Introduction
This is a simple interactive particle simulator written in Python.
I have had the idea of playing around with something 'tactile' like this, but have always been put off by the complexity of it.
However, after some fantastic videos from 10 Minute Papers on fluid simulation topics, I have decided to give it a crack for the 2025 Boot.dev hackathon!

I must admit, I think I bit off more than I can chew (at the moment!), especially in this short timespan. 
So what began as the desire to write a full Fluid-Implicit-Particle (FLIP) simulator, ended up being more of a hacked-together, basic (pun intended) Position Based Dynamics (PBD) simulator.

While the technicals behind it aren't what I set out to do, I had to pivot because I realised that what I was trying to do wasn't feasible in the time I had allotted for myself to write this.
Keeping this in mind, I'm quite happy with what I've managed to get done in this short timespan. I may come back to this and polish it up/ add more features. However, I think I will likely try to write an actual FLIP simulator, in a more reasonable amount of time... (Maybe for the Boot.dev capstone project? :P)

Anyway, you've probably had enough of reading my short novella now, so here is the real fun:

## Installation
There are several options to install this, I made this with the uv package/ project manager. So I would recommend using that. Although I have left a requirements.txt which (should) work too with a regular venv.

#### Using uv
1. Install uv (one-time setup, if you don't already have it) [uv github](https://github.com/astral-sh/uv)

```
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```
# On Windows. 
# Note, you will need to restart your CMD as the newly installed uv will not be found in the active session.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

1. Clone the repo and change directory into it
   
```
git clone https://github.com/Alpha2749/FluidSim.git
cd FluidSim
```

3. To run the project using uv, simply run the following:
   
```
uv run main.py
```


## Usage
You have the following options:
- **Left Click** - Attract particles to cursor
- **Right Click** - Repel particles from cursor
- **Buttons**
  - ***Clear Simulation*** - Clears the simulation box
  - ***Spawn Particles*** - Spawns particles *(as indicated by the Particles to spawn slider)*
- **On-screen Sliders** - Change simulation parameters at runtime
  - ***Particles to spawn*** - How many particles to spawn with the spawn particles button
  - ***Gravity*** - Changes the gravity of the ~situation~ simulation!
  - ***Drag Coefficient*** - How much friction plays an effect (I think it'd broken, in my implementation. 1 works best, but higher is fun too!)
  - ***Mouse Strength*** - How much force the cursor applies when right or left clicking

*(Hopefully I can add more in the future)*

## Demonstration
Here is some media of the simulator in action.


**GIF of the simulator in action** ***(I swear it is higher FPS in real life)***
![](https://github.com/Alpha2749/FluidSim/blob/main/media/fluid_sim_gif.gif)


**Some images**
![](https://github.com/Alpha2749/FluidSim/blob/main/media/sim1.PNG)

![](https://github.com/Alpha2749/FluidSim/blob/main/media/sim2.PNG)

![](https://github.com/Alpha2749/FluidSim/blob/main/media/sim3.PNG)

![](https://github.com/Alpha2749/FluidSim/blob/main/media/simheart.png)

## Aside
There are definitely a lot of issues with this code, and a lot of things I want to change...

First of all, it is not very optimised, hence I have tried to pick a particle amount that seems to work ok, but any more and everything breaks.
My initial tests were even worse, hence I looked into some way to make sure particles were only actually checking neighboring particles, which led me to the spatial grid solutions from several youtube videos and other rabbit holes.

Secondly, especially towards the end, I was very much rushing to get it done. So a lot of my code is quite dirty, and there are way more magic numbers than I would like. 
I am certain there are a lot of constants that aren't actually being used anywhere which I need to clean up.

Lastly, I am pretty sure I have some energy being lost somewhere, and I'm not sure where, as even with a 1.0 damping factor, and a 1.0 drag coefficient, the particles still seem to lose energy. So there is definitely a lot wrong with this.

All things considered, I think it is still a pretty fun little applet, and I think this has helped me understand what is and isn't achievable.
I do plan on writing the FLIP method in the future, but I definitely need to give myself more time to do that. I initially started this wanting to write that, but after watching several videos and reading through a bunch of academic literature, I realised that the time I had given myself was not enough to get that done...

If you've read all this, thank you! And I hope you enjoy this little sim, even if it isn't quite what I want it to be.

