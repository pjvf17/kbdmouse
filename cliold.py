import argparse
import kbd


def list_command(args):
    # Your logic for the list command
    for binding, action in kbd.hotkeys.items():
        print(f"""binding: {binding}, 
              action: {action}""")


def set_command(args):
    # Your logic for the set command
    key = args.key
    value = args.value
    print(f"Setting {key} to {value}")


def remove_command(args):
    # Your logic for the remove command
    key = args.key
    print(f"Removing key: {key}")


def main():
    parser = argparse.ArgumentParser(description="A simple CLI")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # List command
    parser_list = subparsers.add_parser('list', help='List something')
    parser_list.set_defaults(func=list_command)

    # Set command
    parser_set = subparsers.add_parser('set', help='Set a value', usage="%(prog)s -h press release", description="Available actions: " +
                                       ', '.join(kbd.actions))
    # parser_set.add_argument('key', type=str, help='The key to set')
    parser_set.add_argument('press', type=str, help='action executed on keybind press',
                            choices=list(kbd.actions), metavar="press")
    parser_set.add_argument('release', type=str,
                            help='action executed on keybind release', 
                            choices=list(kbd.actions), metavar="release")
    parser_set.set_defaults(func=set_command)

    actionSubParsers = parser_set.add_subparsers(title="actions", dest="action")
    # Define help messages for each action
    actions_help = {
        'angle': 'Set the angle to a specific value.',
        'dangle': 'Adjust the angle by a delta value.',
        'reset': 'Reset the system to its default state.',
        'moveTo': 'Move to a specific position.',
        'center': 'Center the system.',
        'speedChange': 'Change the speed to a new value.',
        'click': 'Perform a click action.',
        'pause': 'Pause the system.',
        'quit': 'Quit the system.',
        'scroll': 'Scroll to a specific position or by a delta.'
    }

    # Create subparsers for each action with help messages
    for action, help_text in actions_help.items():
        pass
        # actionSubParsers.add_parser(action, help=help_text)



    # Remove command
    parser_remove = subparsers.add_parser(
        'remove', help='Remove a key/value pair')
    parser_remove.add_argument('key', type=str, help='The key to remove')
    parser_remove.set_defaults(func=remove_command)

    parser.add_argument('--run', action='store_true', help='Run something')

    args = parser.parse_args()

    if args.run:
        kbd.run()
    elif args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
