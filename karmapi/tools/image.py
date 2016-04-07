"""
Build a path
"""
import argparse
from datetime import date, datetime, timedelta

from karmapi import base, weather
from matplotlib import pyplot

parser = argparse.ArgumentParser()

parser.add_argument("path", nargs='*')

parser.add_argument("--field", nargs='*', default=[])

parser.add_argument("--start")
parser.add_argument("--end")

parser.add_argument("--source", default='euro')

parser.add_argument("--karmapi", default='.')

args = parser.parse_args()

path_template = '{source}/{year}/{month}/{day}/{field}'

dates = []
if args.start:
    start = date(*[int(x) for x in args.start.split('/')])
    dates.append(start)
    
if args.end:
    end = date(*[int(x) for x in args.end.split('/')])

    aday = timedelta(days=1)
    day = start + aday
    while day < end:
        dates.append(day)

        day += aday

parms = base.Parms()
print(args.source)
parms.source = args.source

paths = args.path
for field in args.field:

    parms.field = field
    for day in dates:

        parms.day = day.day
        parms.month = day.month
        parms.year = day.year

        print(parms.__dict__.keys())
        path = path_template.format(parms.__dict__)
        paths.append(path)

        
for path in paths:
    
    print(path)
    continue

    # need meta data to config module properly
    meta = base.get_all_meta_data(path)

    raw = weather.RawWeather()
    raw.from_dict(meta)

    data = base.get(path)

    ndata = raw.day_to_numpy(data)

    pyplot.imsave(path.replace('/', '-') + '.png', ndata)
