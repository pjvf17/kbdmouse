# cli planning

## reqs

probably argparse

- -h
- -c, --current: current bindings
- -s (positional): set binding
  - key combo
  - action
  - modifier (speed, position, clicking, etc.)
- -r (probably by number after options?): remove a binding
- -l log debug output to a file
- something that displays key combos

less important:

- -d: display defaults
- -dd: reset to defaults

- the above is all configured into a config file
  - how tf do config files work?
  - configparser?
  - or json
    - maybe this because I know it best
    - <https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/>

## refactoring

- [ ] Hotkey refactor
  - [ ] Hotkeys need to take an 'action' for 'press' and 'release'
    - actions include:
      - [ ] move (dir)
      - [ ] antimove (-dir) (maybe unnecssary, but it's how I currently have it)
      - [ ] reset dir / speed, solves many bugs
      - [ ] moveTo (pos)
      - [ ] speed_change (speed, check(?), setVal (speed = input (this could be a seperate func, maybe?)))
      - [ ] toggleHold
      - [ ] click (right|left|middle)
      - [ ] pause
      - [ ] stop/quit
      - [ ] scroll (in, out)
      - [ ] prefix ?
- [ ] yo what does hold do

---

perhaps what I'm doing is creating a new HotKey interface of some sort, which can both be the thing that's outputted on print, and what creates a HotKey?

Key combo is currently seperate from the HotKey object. But the initiation should probably be one function.. though I guess it doesn't need to

## bugs

- [ ] going to top left crashes
- [ ] refactor so kbd doesn't just start the program
- [x] seperate out kbd-working.py for alfred / personal use

## features

- second monitor support

### full cli / no .py business

<https://pybit.es/articles/how-to-package-and-deploy-cli-apps/>
