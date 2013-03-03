import re
import urllib2

from .models import Listing

BASE_URL = 'http://sfbay.craigslist.org/sfc/apa/'

def crawl():
    # Download the listings.
    listings_html = urllib2.urlopen(BASE_URL).readlines()

    # Parse the listings.
    matcher = re.compile(r'.*\<a href=\"(\S*)\"\>(.*)\<\/a\>')
    num_listings = 0
    for i in xrange(len(listings_html)):
        line = listings_html[i]
        match = matcher.match(line)
        if match:
            url = match.group(1)
            title = unicode(match.group(2), 'utf-8')
            price = getPrice(title)
            bedrooms = getBedrooms(title)

            # Neighborhood is listed 2 lines down.
            neighborhood_match = re.match('.*\((.*)\)', listings_html[i + 2])
            if not neighborhood_match:
                continue
            neighborhood = neighborhood_match.group(1)

            if url and title and price and neighborhood and bedrooms:
                # Save the listing if it's new or missing information.
                listing = Listing.get_by_key_name(url)
                if not (listing and listing.url and listing.title and listing.price
                                and listing.neighborhood and listing.bedrooms):
                    listing = Listing(key_name=url, url=url, title=title, price=price,
                                                        neighborhood=neighborhood, bedrooms=bedrooms)
                    listing.save()
                    num_listings += 1

    return 'Listings: {:d}'.format(num_listings)
