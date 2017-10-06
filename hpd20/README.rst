

TODO Model
==========

- reverse engineer MFX parameters

- load SCL scale files

- check md5 while loading

Refactor Model
--------------

- derive kit and pad from memoryops

- cleanup instrumentname (put in classes)

- error analysis missing: file load/save


TODO UserInterface
==================

- send edited values to model

- save current kit to .hpd20.cfg

- create KitDialog to set global kit values (volume, balance, pad-sensitivity), after reverse engineering MFX also these

- create ScaleDialog to view and set scale (include non temperament from .scl files)

- copy pad parameters to clipboard

- add apply button, ask user if pad changes should be applied

- cents values with symbols ♭♮♯ - + (quarter note) v ^ slightly up/down

Refactor UI Control
-------------------

- put the grid in own class/file

- more intelligent setting of grid parameters (now a big blob difficult to maintain)

- show pitch with cents deviation

- config out of ui (gets own model)



