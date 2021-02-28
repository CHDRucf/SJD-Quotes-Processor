from flask import Flask, request, jsonify, abort, render_template, Response
from flaskext.mysql import MySQL
import pymysql
import json

application = Flask(__name__)

def add_matches(final):
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    quote_ids = []
    for item in final:
        quote_ids.append(item['quote_id'])

    
        
    if len(quote_ids) == 0:
        mycursor.close()
        db.close()
        return final
    
    if len(quote_ids) == 1:
        mycursor.execute("SELECT matches.quote_id, matches.rank, matches.score, matches.content, " +
                     "work_metadata.title, work_metadata.author, work_metadata.filepath, " +
                     "work_metadata.url, work_metadata.lccn, best_matches.match_id FROM `matches` LEFT JOIN `work_metadata` " + 
                     "ON work_metadata.id = matches.work_metadata_id " + 
                     "LEFT JOIN best_matches ON matches.id = best_matches.match_id " +
                     "WHERE matches.quote_id = %s", quote_ids[0])
    else:
        mycursor.execute("SELECT matches.quote_id, matches.rank, matches.score, matches.content, " +
                     "work_metadata.title, work_metadata.author, work_metadata.filepath, " +
                     "work_metadata.url, work_metadata.lccn, best_matches.match_id FROM `matches` LEFT JOIN `work_metadata` " + 
                     "ON work_metadata.id = matches.work_metadata_id " + 
                     "LEFT JOIN best_matches ON matches.id = best_matches.match_id " +
                     "WHERE matches.quote_id IN {}".format(tuple(quote_ids)))
        
    matches = mycursor.fetchall()
    matches = [{"quote_id": item[0], "rank": item[1], "score": item[2],
                 "content": item[3], "title": item[4], "author": item[5], 
                 "filepath": item[6], "url": item[7], "lccn": item[8], 
                 "best_match_id": item[9],} for item in matches]
    

    for x in final:
        quote_id = int(x['quote_id'])
        for y in matches:
            if quote_id == y['quote_id']:
                
                best_match = False;
                if y['best_match_id'] != None:
                    best_match = True
                
                match = {
                    "title": y['title'],
                    "author": y['author'],
                    "content": y['content'],
                    "rank": y['rank'],
                    "score": y['score'],
                    "filepath": y['filepath'],
                    "url": y['url'],
                    "lccn": y['lccn'],
                    "best_match": best_match
                }
                x['matches'].append(match)
              
    mycursor.close()
    db.close()
    return final

@application.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

@application.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'hello'})

@application.route('/login', methods=['GET','POST'])
def login():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_username = request.form.get('username')
    supplied_password = request.form.get('password')
    mycursor.execute("SELECT username, password FROM users WHERE username = %s AND password = %s", 
                     (supplied_username, supplied_password))
    
    result = mycursor.fetchall()
    mycursor.close()
    db.close()
    
    if len(result) == 1:
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'username or password is invalid'})

@application.route('/get_matches_by_title', methods=['POST'])
def get_matches_by_title():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_title = "%" + str(request.form.get('title')) + "%"
   
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id WHERE " +
                     "quote_metadata.title LIKE %s", supplied_title)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "matches": []} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(add_matches(final))
    
    
@application.route('/get_matches_by_author', methods=['GET', 'POST'])
def get_matches_by_author():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_author = "%" + str(request.form.get('author')) + "%"
   
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id WHERE " +
                     "quote_metadata.author LIKE %s", supplied_author)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "matches": []} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(add_matches(final))
    
@application.route('/get_matches_by_headword', methods=['GET', 'POST'])
def get_matches_by_headword():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_headword = "%" + str(request.form.get('headword')) + "%"
   
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id WHERE " +
                     "quote_metadata.headword LIKE %s", supplied_headword)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "matches": []} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(add_matches(final))

@application.route('/get_matches_by_random', methods=['POST'])
def get_matches_by_random():   
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_number = str(request.form.get('number'))

    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id " +
                     "ORDER BY RAND() LIMIT " + supplied_number)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "matches": []} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(add_matches(final))

@application.route('/unset_best_match', methods=['GET', 'POST'])
def unset_get_match():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_quote_id = request.form.get('quote_id')    
    supplied_match_id = request.form.get('match_id');
    mycursor.execute("DELETE FROM best_matches WHERE quote_id = %s AND match_id = %s",
                     supplied_quote_id, supplied_match_id)
    mycursor.close()
    db.close()
    
@application.route('/set_best_match', methods=['GET', 'POST'])
def set_get_match():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_quote_id = request.form.get('quote_id')
    supplied_match_id = request.form.get('match_id');
    mycursor.execute("INSERT INTO best_matches (quote_id, match_id) VALUES (%s, %s);",
                     supplied_quote_id, supplied_match_id)
    mycursor.close()
    db.close()
   
if __name__ == '__main__':
    application.run(host='localhost', port=5000)
