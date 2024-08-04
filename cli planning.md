# cli planning

## reqs

probably argparse

- -h
- options current bindings
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

## bugs

- going to top left crashes

## features

- second monitor support
