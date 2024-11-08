import click
import kbd


@click.group()
def cli():
    pass


@cli.command()
def list():
    """List something"""
    for binding, action in kbd.hotkeys.items():
        print(f"""binding: {binding}, 
              action: {action}""")


@cli.command(epilog="""
\b
angle(x,y):   sets the cursor moving in the direction set by x, y
              positive x values move to the right, positive y values move downwards
             
dangle(x,y):  same as above but inverse, intened to be used on the 'release' action, 
              allows you to input the same values, therefore cancelling out the 'angle' action
             
reset(None):  resets the cursor, both speed and movement, but not position 
             
moveTo(x,y):  moves the cursor to coordinates (x,y)
             
center(None): moves the cursor to the center of the screen
             
speedChange(change, check, setVal):
              updates the speed at which the cursor moves
             
toggleHold(): when hold is True, ??
             
click(button, press): 
              button can be "left", "right", or "middle"
              press (True, False), determines if it's a mouseDown action or mouseUp action
              a normal keybind for this would have 'press' be True on press, and False on release
              
pause():      pauses kbdmouse until the keybind is set again
             
quit():       quits kbdmouse
             
scroll(amount, hold)
              a positive amount will zoom in, negative zooms out
              hold does ??
""")
@click.option('-k', '--keybind', help="type the keybind rather than doing it manually")
@click.option('-p', '--press', prompt=True, type=click.Choice(kbd.actionsKeys))
@click.option('-r', '--release', prompt=True, type=click.Choice(kbd.actionsKeys))
def set(press, release, keybind):
    """Set a value"""
    print(keybind)
    print(f"Setting press: {press}, release: {release}")

    # Prompt for additional inputs based on the action selected
    press_args = []
    release_args = []

    if press in kbd.actionArgs:
        press_args = [click.prompt(f"Enter {arg} for {press}")
                      for arg in kbd.actionArgs[press]]

    if release in kbd.actionArgs:
        release_args = [click.prompt(
            f"Enter {arg} for {release}") for arg in kbd.actionArgs[release]]

    print(f"Press arguments: {press_args}")
    print(f"Release arguments: {release_args}")

    # You can now call the corresponding functions with these arguments
    if press_args:
        kbd.actions[press](*press_args)

    if release_args:
        kbd.actions[release](*release_args)


@cli.command()
@click.argument('key')
def remove(key):
    """Remove a key/value pair"""
    print(f"Removing key: {key}")


@cli.command()
def run():
    """Run something"""
    kbd.run()


if __name__ == "__main__":
    cli()
