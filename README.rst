

HPD-20 Editor
=============

Synopsis
--------

Program to copy kits around (shared in internet?), modify scales for melodic stuff
create chains, appl modifications on pan, volume, sweep etc.

The HPD-20 can not be edited via MIDI (at least there is no SysEx documented).

This small program will need backups that you create in the SYS-USB Memory menu to work with. Sorry, there is no other way to make it more interactive.
On the other hand it will help you to manage and exchange your kits with other people, create easily melody based kits
and last but not least to print your settings on some paper so you will have them ready i.e. for live performances and you just forgot some important setting.

Usage
-----

Install with pip (sudo pip install hpd20)

I removed wx as it is broken on the mac (install manually: sudo pip install wx or similar)

Run the program as: hpd20-ui

You need to:

- Create a Memorydump on a USB stick of the HPD-20 (without user instruments, as that takes too much time).

- Copy the file to your PC.

- Load it into the program using the File menu.

- Make your changes

- Save the changes it into a file with the same name pattern (from 001-100 i.e. BKUP-002.HS0).

- Restore on the HPD-20 from that file.

Hint: don't overwrite the original file, just in case to be save.



Roadmap
-------

(x) = todo
(/) = done

- (/) read memory dump (BKUP-???.HS0)

- (/) save all kits into folder

- (/) load single kit from folder

- (/) patch simple scales with modes on instrument A

- (/) patch scales with different layouts (across, around, etc.)

- (/) retrieve note for melodic pads (instruments 348-433

- (/) fetch basic information from kit and pad

- (/) UI the whole stuff (tkinter?)

- (x) patch scales on instrument B

- (x) copy or swap kits

- (x) publish on various musician sites

- (x) edit MFX stuff

Macro operations todo
---------------------

- (/) patch scales

- (x) pan over a pad-set

- (x) swap left right (M1 <-> M2, M3 <-> M4, S1 <-> S8 etc...)


Generic todo
------------

get more pitches from some instruments that are for now presumed in C (i.e. Roto Toms, Cowbell)



