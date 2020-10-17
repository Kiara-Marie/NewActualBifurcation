# NewActualBifurcation

This model is a rough attempt at simulating the movement of the ions and Rydbergs in the fist few nanoseconds after the laser pulse. 


```
usage: modelBifurcation.py [-h] [--shells [SHELLS]] [--points [POINTS]] [--c [C]] [--show [SHOW]] [--save [SAVE]]
                           [--time [TIME]] [--name [NAME]] [--frames [FRAMES]] [--fps [FPS]] [--a [A]] [--dist [DIST]]
                           [--tempDrop [TEMPDROP]]

Run the bifurcation model

optional arguments:
  -h, --help            show this help message and exit
  --shells [SHELLS]     Target number of shells
  --points [POINTS]     Target number of particles
  --c [C], --careful [C]Whether to run extra (time consuming) checks to verify code is working properly
  --show [SHOW]         Whether to show the animation
  --save [SAVE]         Whether to save results to file
  --time [TIME]         Time (in ns) to consider densities from RESMO (only used by certain versions of the model)
  --name [NAME]         Filename for file to save
  --frames [FRAMES]     Number of frames for the animation
  --fps [FPS]           Framerate for the animation
  --a [A]               Acceleration coefficient; should be positive
  --dist [DIST]         Maximum distance for an ion to be considered near
  --tempDrop [TEMPDROP] Coefficient for temperature drop
  ```
