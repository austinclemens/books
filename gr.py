from __future__ import division
import xml.etree.ElementTree as ET
import requests
import math
from datetime import datetime
from datetime import *
from dateutil.parser import *
from random import randint
import pandas as pd
import json
import re
import time


pd.options.display.width=280
# genres=['adolescence','adult','animals','anthologies','art-and-photography','artificial-intelligence','audiobook','biblical','biography-memoir','bird-watching','christian','comics-manga','conservation','dark','death','diary','disability','feminism','fiction','football','futurism','futuristic','gender','gender-and-sexuality','glbt','graphic-novels-comics','graphic-novels-manga','history-and-politics','holiday','inspirational','love','management','medical','new-adult','non-fiction','occult','paranormal-urban-fantasy','planetary-science','poetry','productivity','race','relationships','romantic','romantic','science-fiction-fantasy','scinece-nature','sex-and-erotica','sequential-art','social','surreal','teaching','textbooks','united-states','war','wildlife','women-and-gender-studies','womens','thriller','mystery','science','drama','romance','self-help','plays','action','american-history','art','autobiography','crime','']
genres=['comics','cooking','classics','crime','fantasy','historical','horror','humor','mystery','romance','science-fiction','western','biography','autobiography','history','self-help','textbook']
states=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
suburb_dict={'New York City, NY': ['Brooklyn, NY','Manhattan, NY','The Bronx, NY','Bronx, NY','Queens, NY','Staten Island, NY','New York City, NY', 'New York, NY', 'Yonkers, NY', 'Mount Vernon, NY', 'New Rochelle, NY', 'White Plains, NY', 'Scarsdale, NY', 'Nyack, NY', 'South Nyack, NY', 'Sleepy Hollow, NY', 'Tarrytown, NY', 'Pelham, NY', 'Piermont, NY', 'Bronxville, NY', 'Dobbs Ferry, NY', 'Hastings-on-Hudson, NY', 'Palisades, NY', 'Tappan, NY', 'Ardsley, NY', 'Long Beach, NY', 'Great Neck, NY', 'Valley Stream, NY', 'Elmont, NY', 'New Hyde Park, NY', 'Floral Park, NY', 'Hackensack, NJ', 'Bogota, NJ', 'Englewood, NJ', 'Garfield, NJ', 'Guttenberg, NJ', 'Palisades Park, NJ', 'Jersey City, NJ', 'Hoboken, NJ', 'Rockleigh, NJ', 'Northvale, NJ', 'Norwood, NJ', 'Alpine, NJ', 'Closter, NJ', 'Haworth, NJ', 'Demarest, NJ', 'Dumont, NJ', 'Cresskill, NJ', 'Bergenfield, NJ', 'Tenafly, NJ', 'Teaneck, NJ', 'Englewood Cliffs, NJ', 'Leonia, NJ', 'Fort Lee, NJ', 'West New York, NJ'], 'Detroit, MI': ['Allen Park, MI', 'Berkley, MI', 'Center Line, MI', 'Dearborn, MI', 'Dearborn Heights, MI', 'Eastpointe, MI', 'Ecorse, MI', 'Ferndale, MI', 'Grosse Pointe, MI', 'Hamtramck, MI', 'Harper Woods, MI', 'Hazel Park, MI', 'Highland Park, MI', 'Huntington Woods, MI', 'Inkster, MI', 'Lathrup Village, MI', 'Lincoln Park, MI', 'Melvindale, MI', 'Oak Park, MI', 'Pleasant Ridge, MI', 'Redford Township, MI', 'River Rouge, MI', 'Roseville, MI', 'Royal Oak, MI', 'Royal Oak Township, MI', 'St. Clair Shores, MI', 'Southfield, MI', 'Warren, MI', 'Wayne, MI', 'Westland, MI'], 'New Orleans, LA': ['Metairie, LA', 'Kenner, LA', 'Gretna, LA', 'Harvey, LA'], 'Boston, MA': ['Cambridge, MA', 'Malden, MA', 'Somerville, MA', 'Medford, MA', 'Everett, MA', 'Revere, MA', 'Winthrop, MA', 'Quincy, MA', 'Newton, MA', 'Chelsea, MA', 'Brookline, MA', 'Dedham, MA', 'Milton, MA', 'Natick, MA', 'Wellesley, MA', 'Waltham, MA', 'Framingham, MA'], 'Kansas City, MO': ['Sugar Creek, MO', 'North Kansas City, MO', 'Gladstone, MO', 'Raytown, MO', 'Grandview, MO', 'Riverside, MO', 'Claycomo, MO', 'Northmoor, MO', 'Houston Lake, MO', 'Randolph, MO', 'Platte Woods, MO', 'Lake Waukomis, MO', 'Oaks, MO', 'Oakview, MO', 'Oakwood, MO', 'Oakwood Park, MO', 'Shawnee Mission, KS', 'Mission, KS', 'Mission Hills, KS', 'Mission Woods, KS', 'Countryside, KS', 'Fairway, KS', 'Prairie Village, KS', 'Roeland Park, KS', 'Merriam, KS', 'Westwood, KS', 'Westwood Hills, KS'], 'Miami, FL': ['Miami\xe2\x80\x93Miami Beach, FL', 'North Miami, FL', 'North Miami Beach, FL', 'South Miami, FL', 'El Portal, FL', 'Miami Gardens, FL', 'Opa-locka, FL', 'Medley, FL', 'Richmond Heights, FL', 'Coral Gables, FL', 'Fort Lauderdale, FL', 'Hollywood, FL', 'Pompano Beach, FL', 'Deerfield Beach, FL', 'Lauderhill, FL', 'Lauderdale Lakes, FL', 'North Lauderdale, FL', 'Wilton Manors, FL', 'Dania Beach, FL', 'Hallandale Beach, FL'], 'Tampa Bay Area, FL': ['Hillsborough County, FL', 'Brandon, FL', 'East Lake-Orient Park, FL', 'Egypt Lake-Leto, FL', 'Gibsonton, FL', 'Greater Carrollwood, FL', 'Lake Magdalene, FL', 'Palm River-Clair Mel, FL', 'Pebble Creek, FL', 'Progress Village, FL', 'Riverview, FL', 'Seffner, FL', 'Temple Terrace, FL', "Town 'n' Country, FL", 'University, FL', 'Westchase, FL', 'St. Petersburg, FL', 'Clearwater, FL', 'Dunedin, FL', 'Indian Rocks Beach, FL', 'Largo, FL', 'Pinellas Park, FL', 'Tarpon Springs, FL'], 'Minneapolis-St. Paul, MN': ['Minneapolis, MN', 'Brooklyn Center, MN', 'Columbia Heights, MN', 'Edina, MN', 'Fridley, MN', 'Golden Valley, MN', 'Richfield, MN', 'Robbinsdale, MN', 'St. Anthony, MN', 'St. Louis Park, MN', 'St. Paul, MN', 'Falcon Heights, MN', 'Little Canada, MN', 'Maplewood, MN', 'Mendota Heights, MN', 'West St. Paul, MN', 'Roseville, MN'], 'Philadelphia, PA': ['Cheltenham, PA', 'Chester, PA', 'Haverford, PA', 'Lower Merion, PA', 'Upper Darby, PA', 'Camden, NJ', 'Collingswood, NJ', 'Haddonfield, NJ', 'Haddon Township, NJ', 'Haddon Heights, NJ', 'Gloucester City, NJ', 'Merchantville, NJ', 'Pennsauken, NJ', 'Palmyra, NJ', 'Riverton, NJ'], 'Memphis, TN': ['Bartlett, TN', 'Cordova, TN', 'Germantown, TN', 'Hickory Hill, TN', 'Whitehaven, TN'], 'Los Angeles, CA': ['Alhambra, CA', 'Compton, CA', 'Culver City, CA', 'East Los Angeles, CA', 'Montebello, CA', 'Monterey Park, CA', 'Glendale, CA', 'Hawthorne, CA', 'Huntington Park, CA', 'Inglewood, CA', 'Lynwood, CA', 'Maywood, CA', 'Santa Monica, CA', 'West Hollywood, CA'], 'Baltimore, MD': ['Arbutus, MD', 'Baltimore Highlands, MD', 'Brooklyn Park, MD', 'Carney, MD', 'Catonsville, MD', 'Dundalk, MD', 'Halethorpe, MD', 'Lansdowne, MD', 'Linthicum, MD', 'Lochearn, MD', 'Overlea, MD', 'Parkville, MD', 'Pikesville, MD', 'Pumphrey, MD', 'Riderwood, MD', 'Rodgers Forge, MD', 'Rosedale, MD', 'Ruxton, MD', 'Sudbrook Park, MD', 'Towson, MD', 'Woodlawn, MD'], 'Albany, NY': ['East Greenbush, NY', 'Guilderland, NY', 'Menands, NY', 'North Greenbush, NY'], 'Phoenix, AZ': ['Avondale, AZ', 'Glendale, AZ', 'Tolleson, AZ', 'Peoria, AZ', 'Tempe, AZ', 'Guadalupe, AZ', 'Scottsdale, AZ', 'Paradise Valley, AZ', 'Mesa, AZ', 'Chandler, AZ', 'Buckeye, AZ', 'Goodyear, AZ', 'Avondale, AZ', 'Surprise, AZ', 'Gilbert, AZ', 'Maricopa, AZ'], 'St. Louis, MO': ['Affton, MO', 'Lemay, MO', 'Maplewood, MO', 'Shrewsbury, MO', 'Webster Groves, MO', 'Clayton, MO', 'University City, MO', 'Pine Lawn, MO', 'Jennings, MO', 'Hazelwood, MO', 'Bridgeton, MO', 'Maryland Heights, MO', 'Florissant, MO', 'Town and Country, MO', 'Ladue, MO', 'Ferguson, MO', 'Olivette, MO', 'Creve Coeur, MO', 'Fenton, MO', 'Mehlville, MO', 'Richmond Heights, MO', 'St. Ann, MO', 'Kirkwood, MO', 'Normandy, MO', 'Brentwood, MO', 'Sunset Hills, MO', 'East St. Louis, MO'], 'San Francisco Bay Area': ['San Francisco, CA', 'Daly City, CA', 'Colma, CA', 'Brisbane, CA', 'Broadmoor, CA', 'Pacifica, CA', 'South San Francisco, CA', 'Oakland, CA', 'Alameda, CA', 'Emeryville, CA', 'Hayward, CA', 'San Leandro, CA', 'San Jose, CA', 'Campbell, CA', 'Cupertino, CA', 'Los Gatos, CA', 'Milpitas, CA', 'Santa Clara, CA'], 'Chicago, IL': ['Alsip, IL', 'Bedford Park, IL', 'Bensenville, IL', 'Berwyn, IL', 'Blue Island, IL', 'Bridgeview, IL', 'Burbank, IL', 'Burnham, IL', 'Calumet City, IL', 'Calumet Park, IL', 'Chicago Heights, IL', 'Chicago Ridge, IL', 'Cicero, IL', 'Des Plaines, IL', 'Dolton, IL', 'Elmwood Park, IL', 'Evanston, IL', 'Evergreen Park, IL', 'Franklin Park, IL', 'Harvey, IL', 'Harwood Heights, IL', 'Hickory Hills, IL', 'Hometown, IL', 'Lincolnwood, IL', 'Markham, IL', 'Merrionette Park, IL', 'Morton Grove, IL', 'Mount Prospect, IL', 'Niles, IL', 'Norridge, IL', 'Oak Lawn, IL', 'Oak Park, IL', 'Park Ridge, IL', 'River Forest, IL', 'Riverside, IL', 'River Grove, IL', 'Riverdale, IL', 'Rosemont, IL', 'Schiller Park, IL', 'Skokie, IL', 'Stickney, IL', 'Summit, IL', 'Hammond, IL'], 'Dallas, TX': ['Addison, TX', 'Balch Springs, TX', 'Carrollton, TX', 'Cockrell Hill, TX', 'DeSoto, TX', 'Duncanville, TX', 'Farmers Branch, TX', 'Garland, TX', 'Grand Prairie, TX', 'Highland Park, TX', 'Irving, TX', 'Mesquite, TX', 'Plano, TX', 'Richardson, TX', 'University Park, TX', 'Fort Worth, TX', 'Arlington, TX', 'Bedford, TX', 'Dalworthington Gardens, TX', 'Euless, TX', 'Forest Hill, TX', 'Haltom City, TX', 'Hurst, TX', 'North Richland Hills, TX', 'Pantego, TX', 'Richland Hills, TX', 'River Oaks, TX', 'Sansom Park, TX', 'Westover Hills, TX', 'Westworth Village, TX', 'White Settlement, TX'], 'Cincinnati, OH': ['Arlington Heights, OH', 'Amberley, OH', 'Cheviot, OH', 'Deer Park, OH', 'Elmwood Place, OH', 'Forest Park, OH', 'Golf Manor, OH', 'Lockland, OH', 'Mount Healthy, OH', 'North College Hill, OH', 'Norwood, OH', 'Reading, OH', 'Silverton, OH', 'Springdale, OH', 'St. Bernard, OH', 'Wyoming, OH', 'Bellevue, KY', 'Covington, KY', 'Ludlow, KY', 'Newport, KY', 'Dayton, KY', 'Fort Thomas, KY'], 'Las Vegas, NV': ['North Las Vegas, NV', 'Henderson, NV', 'Boulder City, NV', 'Paradise, NV', 'Spring Valley, NV', 'Winchester, NV', 'Sunrise Manor, NV', 'Whitney, NV'], 'Pittsburgh, PA': ['Crafton, PA', 'Ingram, PA', 'McKees Rocks, PA', 'Brentwood, PA', 'Green Tree, PA', 'Carnegie, PA', 'Dormont, PA', 'Mt. Lebanon, PA', 'Baldwin, PA', 'Castle Shannon, PA', 'Whitehall, PA', 'Munhall, PA', 'Homestead, PA', 'Braddock, PA', 'Swissvale, PA', 'Edgewood, PA', 'Wilkinsburg, PA', 'Shaler, PA', 'Bellevue, PA', 'West View, PA', 'Millvale, PA', 'Sharpsburg, PA'], 'Washington, DC': ['Bethesda, MD', 'Bladensburg, MD', 'Brentwood, MD', 'Cheverly, MD', 'Chevy Chase, MD', 'College Park, MD', 'Cottage City, MD', 'District Heights, MD', 'Gaithersburg, MD', 'Hillcrest Heights, MD', 'Hyattsville, MD', 'Kensington, MD', 'Mount Rainier, MD', 'Montgomery Village, MD', 'North Brentwood, MD', 'Rockville, MD', 'Seat Pleasant, MD', 'Silver Spring, MD', 'Suitland, MD', 'Takoma Park, MD', 'Alexandria, VA', 'Annandale, VA', 'Arlington, VA', 'Falls Church, VA', 'McLean, VA', 'Pimmit Hills, VA', 'Springfield, VA'], 'Indianapolis, IN': ['Beech Grove, IN', 'Carmel, IN', 'Clermont, IN', 'Fishers, IN', 'Greenwood, IN', 'Lawrence, IN', 'Meridian Hills, IN', 'Southport, IN', 'Speedway, IN'], 'Atlanta, GA': ['Belvedere Park, GA', 'Brookhaven, GA', 'Candler-McAfee, GA', 'Chamblee, GA', 'College Park, GA', 'Decatur, GA', 'Druid Hills, GA', 'East Point, GA', 'Gresham Park, GA', 'Hapeville, GA', 'Marietta, GA', 'North Atlanta, GA', 'North Druid Hills, GA', 'Sandy Springs, GA', 'Smyrna, GA', 'Vinings, GA'], 'Dayton, OH': ['Beavercreek, OH', 'Huber Heights, OH', 'Kettering, OH', 'Moraine, OH', 'Oakwood, OH', 'Riverside, OH', 'Trotwood, OH', 'Vandalia, OH', 'West Carrollton, OH'], 'Houston, TX': ['Aldine, TX', 'Bellaire, TX', 'Channelview, TX', 'Galena Park, TX', 'Humble, TX', 'Jersey Village, TX', 'Katy, TX', 'Meadows Place, TX', 'Pasadena, TX', 'Pearland, TX', 'Stafford, TX', 'League City, TX', 'Missouri City, TX', 'Webster, TX'], 'Cleveland, OH': ['Bratenahl, OH', 'Brook Park, OH', 'Brooklyn, OH', 'Brooklyn Heights, OH', 'Cleveland Heights, OH', 'Cuyahoga Heights, OH', 'East Cleveland, OH', 'Fairview Park, OH', 'Euclid, OH', 'Garfield Heights, OH', 'Lakewood, OH', 'Linndale, OH', 'Maple Heights, OH', 'Newburgh Heights, OH', 'Parma, OH', 'Shaker Heights, OH', 'South Euclid, OH', 'University Heights, OH', 'Warrensville Heights, OH']}
key=open('/Users/austinclemens/Desktop/books/key.txt','r').read()

# take a user id and compile a list of their books, review scores, and review timestamps
def get_user(id):
	print 'user ',id
	# get info on the user and snag the number of reviews they have
	r=requests.get('https://www.goodreads.com/user/show/'+str(id)+'.xml?key='+key)
	root=ET.fromstring(r.text.encode('ascii','ignore'))
	try:
		reviews=root.find('user/reviews_count').text
		location=root.find('user/location').text
	except:
		return
	time.sleep(1)
	user_dict={'location':location,'books':{}}
	# don't collect if user is not US based
	if location==None:
		location=''
	if any(state in location for state in states):
		# get a user's shelf, one page at a time
		for page in range(1,1+int(math.ceil(int(reviews)/200))):
			r=requests.get('https://www.goodreads.com/review/list?v=2&id='+str(id)+'&page='+str(page)+'&key='+key+'&per_page=200')
			root=ET.fromstring(r.text.encode('ascii','ignore'))
			for book in root.findall('reviews/review'):
				test=check_date(book.find('date_added').text)
				if test!=False:
					name=book.find('book/title').text
					bookid=book.find('book/id').text
					rating=book.find('rating').text
					date=test
					user_dict['books'][bookid]={'title':name,'rating':rating,'it was the summer of':date}
			time.sleep(1)
	else:
		return
	return user_dict


# make sure a book was reviewed in the summer
def check_date(reviewdate):
	reviewdate=parse(reviewdate).date()
	if reviewdate.month>=6 and reviewdate.month<=8:
		return reviewdate.year
	return False


# get the specified number of new users
def get_users(number):
	new_list=[]
	# get existing user file
	existing=pickle.load(open('/Users/austinclemens/Desktop/usersd.p','r'))
	while len(new_list)<number:
		v=randint(0,67675030)
		if v not in existing:
			new_list.append(randint(0,67675030))
	existing=existing+new_list
	pickle.dump(existing,open('/Users/austinclemens/Desktop/usersd.p','w'))
	return new_list


# run a list of users and return a userbooks dictionary (takes a dict as input so you can add to an existing one)
def run_userlist(userbookdict,userlist):
	for user in userlist:
		userbookdict.append(get_user(user))


######## ANALYSIS HERE ########
# clean the raw list to exclude users with no reviews and users outside the US. This will leave 10-15% of users sampled
def clean_userbooks(userbooks):
	newlist=[]
	for user in userbooks:
		if user!=None:
			if user['location']==None:
				user['location']=''
			# eliminate addresses that are obviously non US and users with no books
			if any(state in user['location'] for state in states) and len(user['books'])!=0:
				newlist.append(user)
	return newlist


# take a list of user dictionaries and output all cities mentioned + reviews by year + average score by year
def create_city_list(newlist):
	cities=[]
	city_dict={}
	all_total=0
	all_ratings=0
	cdall={2007:[0,0],2008:[0,0],2009:[0,0],2010:[0,0],2011:[0,0],2012:[0,0],2013:[0,0],2014:[0,0],2015:[0,0],2016:[0,0]}
	for user in newlist:
		cities.append(match_suburb(user['location']))
	for city in set(cities):
		print city
		# this is a dumb way to do this but list[0] will be # reviews, list[1] average review for that year
		cd={2007:[0,0],2008:[0,0],2009:[0,0],2010:[0,0],2011:[0,0],2012:[0,0],2013:[0,0],2014:[0,0],2015:[0,0],2016:[0,0]}
		total_city_rating=0
		total_reviews=0
		for user in newlist:
			if match_suburb(user['location'])==city:
				for book in user['books']:
					book=user['books'][book]
					# books rated 0 haven't actually been read/come from to-read list or similar
					if int(book['rating'])>0:
						try:
							cd[book['it was the summer of']][0]=cd[book['it was the summer of']][0]+1
							cd[book['it was the summer of']][1]=cd[book['it was the summer of']][1]+int(book['rating'])
							cdall[book['it was the summer of']][0]=cdall[book['it was the summer of']][0]+1
							cdall[book['it was the summer of']][1]=cdall[book['it was the summer of']][1]+int(book['rating'])
							total_city_rating=total_city_rating+int(book['rating'])
							total_reviews=total_reviews+1
							all_ratings=all_ratings+int(book['rating'])
							all_total=all_total+1
						except:
							pass
		for year in cd.keys():
			try:
				cd[year][1]=cd[year][1]/cd[year][0]
			except:
				pass
		try:
			city_dict[city]={'users':cities.count(city),'reviews':total_reviews,'avg_review':total_city_rating/total_reviews,'years':cd}
		except:
			pass
	for year in cdall.keys():
		try:
			cdall[year][1]=cdall[year][1]/cdall[year][0]
		except:
			pass
	city_dict['all']={'reviews':all_total,'avg_review':all_ratings/all_total,'years':cdall}
	return city_dict


# match a suburb/location string to its metro area
def match_suburb(city):
	for key in suburb_dict.keys():
		if city in suburb_dict[key]:
			return key
	return city


# take a list of user dictionaries and create a single list of all books reviewed
def create_book_list(newlist):
	books={}
	for user in newlist:
		for book in user['books'].keys():
			if book in books.keys():
				books[book]['reviews']=books[book]['reviews']+1
				books[book]['average']=books[book]['average']+int(user['books'][book]['rating'])
			if book not in books.keys() and int(user['books'][book]['rating'])>0:
				books[book]={'title':user['books'][book]['title'],'reviews':1,'average':int(user['books'][book]['rating'])}
	for book in books:
		books[book]['average']=books[book]['average']/books[book]['reviews']
	return books


# quick way to get a booklist
def create_quick_booklist(newlist):
	books=[]
	for user in newlist:
		for book in user['books'].keys():
			books.append(book)
	return books


# take a list of user dicts and assign a genre to each book
def get_genres(newlist):
	genres=[]
	booklist=create_quick_booklist(newlist)
	bookdict={}
	for book in booklist:
		print book
		bookdict[book]=[]
		r=requests.get('https://www.goodreads.com/book/show.xml?key='+key+'&id='+book)
		root=ET.fromstring(r.text.encode('ascii','ignore'))
		shelves=root.findall('book/popular_shelves/shelf')
		total_genre_votes=0
		for shelf in shelves:
			bookdict[book].append([shelf.get('name'),int(shelf.get('count'))])
			total_genre_votes=total_genre_votes+int(shelf.get('count'))
			genres.append(shelf.get('name'))
		for shelf in bookdict[book]:
			shelf[1]=shelf[1]/total_genre_votes
		time.sleep(1)
	genres=list(set(genres))
	for user in newlist:
		for book in user['books']:
			user['books'][book]['genres']=bookdict[book]
	return newlist


def genre_list(newlist):
	glist=[]
	for user in newlist:
		for book in user['books']:
			for g in user['books'][book]['genres']:
				glist.append(g[0])
	return list(set(glist))


# create a pandas data frame where the review is the unit of analysis
def create_pandas(newlist):
	biglist=[]
	for user in newlist:
		location=user['location']
		for book in user['books']:
			entry=user['books'][book]
			ident=book
			rating=int(entry['rating'])
			title=entry['title']
			summer=entry['it was the summer of']
			entry=[ident,title,summer,rating,location]
			glist=[g[0] for g in user['books'][book]['genres']]
			for genre in genres:
				if genre in glist:
					entry.append(1)
				else:
					entry.append(0)
			if rating>0:
				biglist.append(entry)
	print biglist
	return pd.DataFrame(biglist, columns=['ident','title','summer','rating','location','comics','cooking','classics','crime','fantasy','historical','horror','humor','mystery','romance','science-fiction','western','biography','autobiography','history','self-help','textbook'])


# get distinctive books by city and state and year
def distinctive_books(df):
	df.grouby()

















