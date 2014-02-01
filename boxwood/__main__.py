import argparse
import json

import data


def main():
    parser = argparse.ArgumentParser(description="Process the dataset.")
    parser.add_argument('--json', action='store_true')
    parsed_args = vars(parser.parse_args())

    if parsed_args['json']:
        print as_json()
    else:
        pretty_print()


def as_json():
    return json.dumps(list(row._asdict() for row in data.dataset()))


def pretty_print():
    for x in data.dataset():
        if x.latlon is not None:
            print "======================================\n"
            print "Record: \t", x.accession_number, \
                "({})".format(x.js_safe_id())
            print "Year: \t\t", x.year
            print "Species: \t", x.species

            print "Location: \t", x.country,
            if x.latlon is not None:
                print "({}, {})".format(x.latlon[0], x.latlon[1])
            else:
                print ''

            if x.locality:
                print "Locality: \t", x.locality

            print "\n======================================\n"

if __name__ == '__main__':
    main()
