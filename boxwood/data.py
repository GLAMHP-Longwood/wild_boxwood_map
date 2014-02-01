from collections import namedtuple
import csv
import hashlib
import os


class Specimen(namedtuple('Specimen_', ['year', 'accession_number', 'species',
                                        'country', 'locality', 'latlon'])):
    """A namedtuple for specimen rows."""

    def js_safe_id(self):
        """A JavaScript-safe identifier that's probably unique."""

        hash_ = hashlib.md5(self.accession_number).hexdigest()[0:10]
        return '{}'.format(hash_)


def dataset():
    """Generate ``Specimen`` objects for each row in the dataset.

    Specify the CSV file with the ``LONGWOOD_DATASET`` environment variable.
    """

    with open(os.environ['LONGWOOD_DATASET'], 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        reader.next()
        for row in reader:

            year = row[0][0:4]
            accession_number, species = row[0:2]
            # ignore row[2] since we don't know what it is
            country, locality = row[3:5]
            latlon = normalize_latlon(row[5:])

            if latlon == '':
                latlon = 'MISSING'

            yield Specimen(year, accession_number, species, country, locality,
                           latlon)


def normalize_latlon(columns):
    """Convert latitude and longitude columns into a tuple of floats."""

    lat, lat_direction, lon, lon_direction = columns

    # if there's no lat/lon data, just return None
    if any(True for deg in (lat, lon) if deg == ''):
        return None

    lat, lon = float(lat), float(lon)

    if lat_direction == 'S':
        lat = lat * -1.0
    if lon_direction == 'W':
        lon = lon * -1.0

    return lat, lon
