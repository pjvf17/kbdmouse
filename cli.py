import argparse
import kbd

def list_command(args):
    # Your logic for the list command
    print(kbd.curAng)
    for binding, action in kbd.hotkeys.items():
        print(f"binding: {binding}, action: {action}")

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
    parser_set = subparsers.add_parser('set', help='Set a value')
    parser_set.add_argument('key', type=str, help='The key to set')
    parser_set.add_argument('value', type=str, help='The value to set')
    parser_set.set_defaults(func=set_command)
    
    # Remove command
    parser_remove = subparsers.add_parser('remove', help='Remove a key/value pair')
    parser_remove.add_argument('key', type=str, help='The key to remove')
    parser_remove.set_defaults(func=remove_command)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
