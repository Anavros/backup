
import load
import tasks

# To use this script, create a file called `config.py` in this directory,
# and define the variables `d_links`, `d_syncs`, `d_balls`, and `bconfig`.

# TODO: More details.


def main(argv, config):
    print("Loading files in {}...".format(config.bconfig))
    files = load.filelist(config.bconfig)
    if len(argv) > 1:
        for command in argv[1:]:
            if   command == 'list':
                tasks.list(files)
            elif command == 'size':
                tasks.size(files)
            elif command == 'link':
                tasks.link(files, config.d_links)
            elif command == 'sync':
                tasks.sync(files, config.d_syncs)
            elif command == 'ball':
                tasks.ball(files, config.d_balls, config.bconfig)
            else:
                print("Unknown command:", command)
    else:
        # Default behavior without arguments: backup everything.
        tasks.link(files, config.d_links)
        tasks.sync(files, config.d_syncs)
        tasks.ball(files, config.d_balls, config.bconfig)
    print("All tasks complete.")


if __name__ == '__main__':
    import sys
    try:
        import config
    except ImportError:
        print("Create a file `config.py` in the same directory as this script.")
        print("Define the variables `d_links`, `d_syncs`, `d_balls`, and `bconfig`.")
        print("These are root-anchored paths for links, syncs (copies), and tarballs.")
        print("`bconfig` is the path to the backup configuration file.")
    else:
        main(sys.argv, config)
