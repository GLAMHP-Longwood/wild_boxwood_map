from collections import namedtuple
import csv
import hashlib
import os


class Specimen(namedtuple('Specimen_', ['year', 'accession_number', 'species',
                                        'country', 'locality', 'latlon',
                                        'has_picture'])):
    """A namedtuple for specimen rows."""

    def js_safe_id(self):
        """A JavaScript-safe identifier that's probably unique."""

        hash_ = hashlib.md5(self.accession_number).hexdigest()[0:10]
        return '{}'.format(hash_)


def dataset():
    """Generate ``Specimen`` objects for each row in the dataset.

    Specify the CSV file with the ``LONGWOOD_DATASET`` environment variable.
    """

    dataset_path = os.environ['LONGWOOD_DATASET']
    img_dir_path = os.path.join(os.path.dirname(dataset_path), 'img/')

    with open(dataset_path, 'rbU') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        reader.next()
        for row in reader:

            year = row['ACC_NUM'][0:4]
            accession_number = row['ACC_NUM']
            species = row['NAME']
            country = row['COUNTRY_FULL']
            locality = row['LOCALITY']
            latlon = normalize_latlon(row['LAT_DEGREE'], row['LAT_DIR'],
                                      row['LONG_DEGREE'], row['LONG_DIR'],
                                      row['HumanLat'], row['HumanLong'])

            _possible_img = os.path.join(img_dir_path,
                                         '{}.jpg'.format(accession_number))
            has_picture = os.path.isfile(_possible_img)

            yield Specimen(year, accession_number, species, country, locality,
                           latlon, has_picture)


def normalize_latlon(*columns):
    """Convert latitude and longitude columns into a tuple of floats."""

    lat, lat_direction, lon, lon_direction, human_lat, human_lon = columns

    if human_lat and human_lon:
        return float(human_lat), float(human_lon)

    # if there's no lat/lon data, just return None
    if any(True for deg in (lat, lon) if deg == ''):
        return None

    lat, lon = float(lat), float(lon)

    if lat_direction == 'S':
        lat = lat * -1.0
    if lon_direction == 'W':
        lon = lon * -1.0

    return lat, lon
