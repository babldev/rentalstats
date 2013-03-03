import datetime
import os
import re

from flask import Flask
from flask import render_template

from .models import Listing

NUM_WEEKS = 24

MAX_PRICE = 10000
MIN_PRICE = 500

AXIS_NAMES = [
              'SOMA / south beach',
#              'USF / panhandle',
#              'alamo square / nopa',
#              'bayview',
#              'bernal heights',
              'castro / upper market',
#              'cole valley / ashbury hts',
#              'downtown / civic / van ness',
#              'excelsior / outer mission',
#              'financial district',
#              'glen park',
#              'haight ashbury',
#              'hayes valley',
#              'ingleside / SFSU / CCSF',
#              'inner richmond',
#              'inner sunset / UCSF',
#              'laurel hts / presidio',
#              'lower haight',
#              'lower nob hill',
#              'lower pac hts',
#              'marina / cow hollow',
              'mission district',
              'nob hill',
              'noe valley',
#              'north beach / telegraph hill',
              'pacific heights',
#              'portola district',
#              'potrero hill',
#              'richmond / seacliff',
#              'russian hill',
#              'sunset / parkside',
#              'tenderloin',
#              'treasure island',
#              'twin peaks / diamond hts',
#              'visitacion valley',
#              'west portal / forest hill',
#              'western addition'
              ]


def getPrice(title):
    match = re.match(r'\$(\d*) ', title)
    if match:
        return int(match.group(1))


def getBedrooms(title):
    match = re.match(r'\$\d* / (\d)br', title)
    if match:
        return int(match.group(1))


def getPriceRows(neighborhoods):
    rows = []
    for week in xrange(NUM_WEEKS):
        row = [ '%d week(s) ago' % (NUM_WEEKS - week) ]
        for neighborhood in neighborhoods:
            # Create the query.
            query = Listing.all()
            query.filter('bedrooms =', 1)
            query.filter('neighborhood =', neighborhood)
            now = datetime.datetime.now()
            query.filter('time <', now - datetime.timedelta(7 * (NUM_WEEKS - week - 1)))
            query.filter('time >', now - datetime.timedelta(7 * (NUM_WEEKS - week)))

            # Compute the mean price.
            num_listings = 0
            sum_price = 0
            for listing in query:
                if listing.price > MIN_PRICE and listing.price < MAX_PRICE:
                    num_listings += 1
                    sum_price += listing.price
            if num_listings > 0:
                row.append(float(sum_price) / num_listings)
            else:
                row.append(0.0)

        rows.append(row)

    return rows


def getCountRows(neighborhoods):
    rows = []
    for week in xrange(NUM_WEEKS):
        row = [ '%d week(s) ago' % (NUM_WEEKS - week) ]
        for neighborhood in neighborhoods:
            # Create the query.
            query = Listing.all()
            query.filter('bedrooms =', 1)
            query.filter('neighborhood =', neighborhood)
            now = datetime.datetime.now()
            query.filter('time <', now - datetime.timedelta(7 * (NUM_WEEKS - week - 1)))
            query.filter('time >', now - datetime.timedelta(7 * (NUM_WEEKS - week)))

            row.append(query.count())

        rows.append(row)

    return rows


# Create the app.
app = Flask(__name__)


@app.route('/')
def mainRoute():
    return render_template('index.html')


@app.route('/count')
def countRoute():
    rows = getCountRows(AXIS_NAMES)
    template_values = {
                       'title' : 'Total number of 1 bedrooms posted by neighborhood',
                       'x_label' : 'Week',
                       'axis_names' : AXIS_NAMES,
                       'rows' : rows
                       }
    return render_template('chart.html', **template_values)


@app.route('/price')
def priceRoute():
    rows = getPriceRows(AXIS_NAMES)
    template_values = {
                       'title' : 'Average 1 bedroom rental price by neighborhood',
                       'x_label' : 'Week',
                       'axis_names' : AXIS_NAMES,
                       'rows' : rows
                       }
    return render_template('chart.html', **template_values)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    debug = bool(os.environ.get('DEBUG', False))
    app.run(host='0.0.0.0', port=port, debug=debug)
