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
