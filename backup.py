
import load
import tasks
from configparser import ConfigParser


def main(args):
    conf = ConfigParser()
    conf.read('config.ini')
    try:
        s = conf[args.section]
    except KeyError:
        print("Unknown section: '{}'. Check your config.ini file.".format(args.section))
        exit(1)

    print("Loading files in {}...".format(s['backupconfig']))
    files = load.filelist(s['backupconfig'])

    if args.tasks:
        for task in args.tasks:
            if   task == 'list':
                tasks.list(files)
            elif task == 'size':
                tasks.size(files)
            elif task == 'link':
                tasks.link(files, s['links'])
            elif task == 'sync':
                tasks.sync(files, s['syncs'])
            elif task == 'ball':
                tasks.ball(files, s['balls'], s['backupconfig'])
            else:
                print("Unknown command:", command)
    else:
        # Default behavior without arguments: backup everything.
        tasks.link(files, s['links'])
        tasks.sync(files, s['syncs'])
        tasks.ball(files, s['balls'], s['backupconfig'])
    print("All tasks complete.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("section")
    parser.add_argument("tasks", nargs='*')
    main(parser.parse_args())
