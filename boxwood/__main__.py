import data


def main():
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
