from bottle import mako_view as view
from bottle import Bottle, route, run, template, redirect, request, get, static_file
import sqlite3
import os
#github test
app = Bottle()
dbname = "tcbf_beer_taste.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
graph_setting = {'graph_size_x':600, 'graph_size_y':600}


@app.get('/static/css/<filename:path>')
def css(filename):
    return static_file(filename, root=STATIC_DIR + '/css')

@app.get('/static/js/<filename:path>')
def css(filename):
    return static_file(filename, root=STATIC_DIR + '/js')

@app.get('/static/img/<filename:path>')
def css(filename):
    return static_file(filename, root=STATIC_DIR + '/img')


@app.route('/home')
@view('home')
def home():
	print "home"
	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	select_beers = "select * from beer"
	select_breweries = "select * from brewery"
#	select_beers = "select * from beer inner join brewery on beer.brewery_id = brewery.id"
	c.execute(select_beers)
	beer_list=[]
	for beer in c.fetchall():
		beer_list.append({
			"beer_id":beer[0],
			"beer_name":beer[1],
			"beer_style":beer[2],
			"beer_description":beer[3],
			"beer_ibu":beer[4],
			"beer_abv":beer[5],
			"brewery_id":beer[6]
		})

	c.execute(select_breweries)
	brewery_list=[]
	for brewery in c.fetchall():
		brewery_list.append({
			"brewery_id":brewery[0],
			"brewery_name":brewery[1],
			"brewery_logo":brewery[2],
			"brewery_prefecture":brewery[3],
			"brewery_description":brewery[4],
			"brewery_active":brewery[5]
		})
	conn.close()

#	print beer_list
#	print {'beer_list':beer_list, 'brewery_list':brewery_list}
	return {'beer_list':beer_list, 'brewery_list':brewery_list}

@app.route('/show_comment/:beer_id')
@view('show_comment')
def show_comment(beer_id):
	print "show_comment"
	beer_info = select_beer(beer_id)
	comment_list = select_comments(beer_id)
	if len(comment_list)==0:
	    average_point ={}
	else:
	    average_point = get_average_point(comment_list)

	return {'beer_info':beer_info, 'comment_list':comment_list, 'graph_setting':graph_setting, 'average_point':average_point}

@app.route('/create_comment/:beer_id')
@view('create_comment')
def create_comment(beer_id):
	print "create_comment"
	beer_info = select_beer(beer_id)
	comment_list = select_comments(beer_id)
	return {'beer_info':beer_info, 'comment_list':comment_list, 'graph_setting':graph_setting}

@app.route('/add_comment', method="POST")
@view('comment_added')
def add_comment():
	print "add_comment"
	beer_id = request.forms.getunicode("beer_id")
	comment_user_name = request.forms.getunicode("comment_user_name")
	comment = request.forms.getunicode("comment")
	x = request.forms.getunicode("x")
	y = request.forms.getunicode("y")
	new_comment = {
		"comment_user_name":comment_user_name,
		"comment_x":x,
		"comment_y":y,
		"comment_comment":comment,
		"beer_id":beer_id
	}
	if x!="" and y!="":
		print "add_comment"
		add(new_comment)

	beer_info = select_beer(beer_id)
	comment_list = select_comments(beer_id)
	if len(comment_list)==0:
	    average_point ={}
	else:
	    average_point = get_average_point(comment_list)
	return {'beer_info':beer_info, 'comment_list':comment_list, 'graph_setting':graph_setting, 'average_point':average_point}


@app.route('/twitter')
@view('twitter')
def twitter():
	return

@app.route('/instagram')
@view('instagram')
def instagram():
	return

@app.route('/facebook')
@view('facebook')
def facebook():
	return

@app.route('/info')
@view('info')
def info():
	return

@app.route('/news')
@view('news')
def news():
	return

@app.route('/search', method="POST")
@view('search_list')
def search_list():

	#just a sample code
	keyword = request.forms.getunicode("keyword")
#	result_lists = [keyword, 'sample1', 'sample2']
	results_list = search(keyword)
	return {'results_list':results_list}

def search(keyword):
#	result_lists = [keyword, 'result1']
	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	select_all = "select * from sample_tariff"
	c.execute(select_all)
	results_list=[]
	for result in c.fetchall():
		results_list.append({
			"id": result[0],
			"name": result[1]
		})
	conn.close()
	return results_list

def select_beer(beer_id):
	select_beer = "select * from beer inner join brewery on beer.brewery_id = brewery.id where beer.id = " + beer_id
	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	c.execute(select_beer)
	beer_info={}
	for beer in c.fetchall():
		beer_info={
			"beer_id":beer[0],
			"beer_name":beer[1],
			"beer_style":beer[2],
			"beer_description":beer[3],
			"beer_ibu":beer[4],
			"beer_abv":beer[5],
			"brewery_id":beer[6],
			"brewery_id":beer[7],
			"brewery_name":beer[8],
			"brewery_logo":beer[9],
			"brewery_prefecture":beer[10],
			"brewery_description":beer[11],
			"brewery_active":beer[12]
		}
	conn.close()
	return beer_info

def select_comments(beer_id):
	select_comments = "select * from taste_note where beer_id = " + beer_id
	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	c.execute(select_comments)
	comment_list=[]
	for comment in c.fetchall():
		comment_list.append({
			"comment_id":comment[0],
			"comment_user_name":comment[1],
			"comment_x":comment[2],
			"comment_y":comment[3],
			"comment_comment":comment[4],
			"beer_id":comment[5]
		})
	conn.close()
	return comment_list

def add(new_comment):
#	insert_taste_note = "INSERT INTO Taste_note(user_name, x, y, comment, beer_id) VALUES('" + new_comment["comment_user_name"] + "', " + new_comment["comment_x"] + ", " + new_comment["comment_y"] + ", '" + new_comment["comment_comment"] + "', " + new_comment["beer_id"] + ") "
	sql = "INSERT INTO Taste_note(user_name, x, y, comment, beer_id) VALUES (?,?,?,?,?)"
	taste_note = (new_comment["comment_user_name"], new_comment["comment_x"], new_comment["comment_y"], new_comment["comment_comment"], new_comment["beer_id"])

	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	c.execute(sql, taste_note)
	conn.commit()
	conn.close()
	print "added"
	print taste_note
	return

def get_average_point(comment_list):
    x_list = []
    y_list = []
    for comment in comment_list:
        x_list.append(comment["comment_x"])
        y_list.append(comment["comment_y"])
    average_x = sum(x_list) / len(x_list)
    average_y = sum(y_list) / len(y_list)
    print x_list
    print average_x
    print y_list
    print average_y
    return {'average_x':average_x, 'average_y':average_y}

def validate_user(user_info):
    return 0

"""
@app.route('/hello/:names')
@view('hello')
def index(names):
	return {'name':names}
"""
if __name__=="__main__":
	run(app=app,host="localhost",port='8080')
