from random import randrange
from datetime import datetime
from flask import Flask, request, jsonify, abort, render_template, Response, session, redirect, url_for, make_response
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import pymysql
import json
import gzip
import pandas as pd
import zipfile
import zlib
import os

application = Flask(__name__)
application.secret_key = "%#%$*&^*()&)*(^(^%$%$%(*&)(&"
CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
active_tokens = [] # user_id, token, date_time

def user_id_from_token(num):
    for x in active_tokens:
        if x[1] == num:
            return x[0]
    return None

def token_number_exists(num):
    for x in active_tokens:
        if x[1] == num:
            return True
            
    return False

def remove_token(num):
    for x in active_tokens:
        if x[1] == num:
            active_tokens.remove(x)

def add_token(user_id):
    num = randrange(1000000000)
    while token_number_exists(num):
        num = randrange(1000000000)
    active_tokens.append([user_id, num, datetime.utcnow().timestamp()])
    return format(num, "09")

def check_best_match_present(final):
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
        mycursor.execute("SELECT best_matches.quote_id FROM best_matches WHERE best_matches.quote_id = " + str(quote_ids[0]))
    else:
        mycursor.execute("SELECT best_matches.quote_id FROM best_matches WHERE best_matches.quote_id IN {}".format(tuple(quote_ids)))

    quote_ids_with_best_matches = mycursor.fetchall()
    
    for x in final:
        quote_id = int(x['quote_id'])
        if quote_id in quote_ids_with_best_matches:
            x['has_best_match'] = True
            
    mycursor.close()
    db.close()
    return final

# sample Flask endpoint
@application.route('/hello', methods=['GET'])
@cross_origin()
def hello():
    return jsonify({'message': 'hello'})

   
@application.route('/login', methods=['POST'])
@cross_origin()
def logintest():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_username = request.form.get('username')
    supplied_password = request.form.get('password')
    mycursor.execute("SELECT id, username, password FROM users WHERE username = %s AND password = %s", 
                     (supplied_username, supplied_password))
    
    result = mycursor.fetchall()
    mycursor.close()
    db.close()
    
    if len(result) == 1:
        return render_template("home.html", token = add_token(str(result[0][0])))
    else:
        return render_template("login.html")

@application.route('/home', methods=['POST'])
@cross_origin()
def home():
    supplied_token = request.form.get('token')
    if (supplied_token == None):
        return render_template("login.html")
    
    if (token_number_exists(int(supplied_token))):
       return render_template("home.html", token = supplied_token) 
    else:
       return render_template("login.html")
    
@application.route('/results', methods=['POST'])
@cross_origin()
def results():
    supplied_token = request.form.get('token')
    if (supplied_token == None):
        return render_template("login.html")
    
    if (token_number_exists(int(supplied_token))):
       return render_template("results.html", token = supplied_token) 
    else:
       return render_template("login.html")
   
@application.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    supplied_token = request.form.get('token')
    if (supplied_token == None):
        return render_template("login.html")
    remove_token(int(supplied_token))
    return render_template("login.html")

# this endpoint actually retrieves matches for a given quote
@application.route('/get_quote_matches', methods=['POST'])
@cross_origin()
def get_quote_matches():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_quote_id = str(request.form.get('quote_id'))
    supplied_min = str(request.form.get('tMin'))
    supplied_max = str(request.form.get('tMax'))
    supplied_corpus = str(request.form.get('searchCorpus'))
    
    # restrict by specified corpus if applicable
    corpus_restriction_string = ''
    if supplied_corpus == 'gut':
        corpus_restriction_string = "work_metadata.url LIKE 'https://www.gutenberg.org%'AND "
    elif supplied_corpus == 'hat':
        corpus_restriction_string = "work_metadata.url LIKE 'https://catalog.hathitrust.org%' AND "
    elif supplied_corpus == 'loc':
        corpus_restriction_string = "work_metadata.url LIKE 'https://www.loc.gov%' AND "
    elif supplied_corpus == 'lib':
        corpus_restriction_string = "work_metadata.url LIKE 'https://oll.libertyfund.org/' AND "
        
    min_max_string = 'matches.score >= ' + supplied_min + ' AND matches.score <= ' + supplied_max

    mycursor.execute("SELECT matches.id, matches.rank, matches.score, matches.content, " +
                 "work_metadata.id, work_metadata.title, work_metadata.author, work_metadata.filepath, " +
                 "work_metadata.url, work_metadata.lccn, best_matches.match_id FROM `matches` LEFT JOIN `work_metadata` " + 
                 "ON work_metadata.id = matches.work_metadata_id " + 
                 "LEFT JOIN best_matches ON matches.id = best_matches.match_id " +
                 "WHERE ((" + corpus_restriction_string + min_max_string + ") OR best_matches.match_id IS NOT NULL) AND "
                 + "matches.quote_id = " + supplied_quote_id + " ")
    
    matches = mycursor.fetchall()
    matches = [{"match_id": item[0], "rank": item[1], "score": item[2],
                 "content": item[3], "work_metadata_id": item[4], "title": item[5], "author": item[6], 
                 "filepath": item[7], "url": item[8], "lccn": item[9], 
                 "best_match": True if (item[10] != None) else False,} for item in matches]
                
    mycursor.close()
    db.close()
    return jsonify(matches)

''' 
All endpoints starting with "get_matches_by_" themselves only return the quotations themselves 
according to the search criteria.

Matches for each quotation can then finally be returned by calling "get_quote_matches" for that quotation.
'''

@application.route('/get_matches_by_title', methods=['POST'])
@cross_origin()
def get_matches_by_title():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_textFormat = str(request.form.get('textFormat'))
 
    supplied_title = '00000000'
    if supplied_textFormat == 'exact':
        supplied_title = str(request.form.get('title'))
    elif supplied_textFormat == 'startswith':
        supplied_title = str(request.form.get('title')) + "%"
    elif supplied_textFormat == 'contains':
        supplied_title = "%" + str(request.form.get('title')) + "%"
        
    supplied_condition = str(request.form.get('condition'))
   
    condition_string = ''
    if supplied_condition == 'onlybest':
        condition_string = 'best_matches.user_id IS NOT NULL AND '
    elif supplied_condition == 'nobest':
        condition_string = 'best_matches.user_id IS NULL AND '
    
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content, best_matches.user_id FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id " +
                     "LEFT JOIN `best_matches` ON quotes.id = best_matches.quote_id WHERE " +
                     condition_string + "quote_metadata.title LIKE %s", supplied_title)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "best_marked_by": item[6]} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(final)
    
    
@application.route('/get_matches_by_author', methods=['POST'])
@cross_origin()
def get_matches_by_author():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_textFormat = str(request.form.get('textFormat'))
 
    supplied_author = '00000000'
    if supplied_textFormat == 'exact':
        supplied_author = str(request.form.get('author'))
    elif supplied_textFormat == 'startswith':
        supplied_author = str(request.form.get('author')) + "%"
    elif supplied_textFormat == 'contains':
        supplied_author = "%" + str(request.form.get('author')) + "%"
    
    supplied_condition = str(request.form.get('condition'))
   
    condition_string = ''
    if supplied_condition == 'onlybest':
        condition_string = 'best_matches.user_id IS NOT NULL AND '
    elif supplied_condition == 'nobest':
        condition_string = 'best_matches.user_id IS NULL AND '
    
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content, best_matches.user_id FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id " +
                     "LEFT JOIN `best_matches` ON quotes.id = best_matches.quote_id WHERE " +
                     condition_string + "quote_metadata.author LIKE %s", supplied_author)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "best_marked_by": item[6]} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(final)
    
@application.route('/get_matches_by_headword', methods=['POST'])
@cross_origin()
def get_matches_by_headword():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_textFormat = str(request.form.get('textFormat'))
 
    supplied_headword = '00000000'
    if supplied_textFormat == 'exact':
        supplied_headword = str(request.form.get('headword'))
    elif supplied_textFormat == 'startswith':
        supplied_headword = str(request.form.get('headword')) + "%"
    elif supplied_textFormat == 'contains':
        supplied_headword = "%" + str(request.form.get('headword')) + "%"
    
    supplied_condition = str(request.form.get('condition'))
   
    condition_string = ''
    if supplied_condition == 'onlybest':
        condition_string = 'best_matches.user_id IS NOT NULL AND '
    elif supplied_condition == 'nobest':
        condition_string = 'best_matches.user_id IS NULL AND '
    
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content, best_matches.user_id FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id " +
                     "LEFT JOIN `best_matches` ON quotes.id = best_matches.quote_id WHERE " +
                     condition_string + "quote_metadata.headword LIKE %s", supplied_headword)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "best_marked_by": item[6]} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(final)

@application.route('/get_matches_by_random', methods=['POST'])
@cross_origin()
def get_matches_by_random():   
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_number = str(request.form.get('number'))
    supplied_condition = str(request.form.get('condition'))
   
    condition_string = ''
    if supplied_condition == 'onlybest':
        condition_string = 'WHERE best_matches.user_id IS NOT NULL '
    elif supplied_condition == 'nobest':
        condition_string = 'WHERE best_matches.user_id IS NULL '
    
    mycursor.execute("SELECT quote_metadata.quote_id, quote_metadata.author, quote_metadata.title, " + 
                     "quote_metadata.headword, quote_metadata.edition, quotes.content, best_matches.user_id FROM " +
                     "`quotes` LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id " +
                     "LEFT JOIN `best_matches` ON quotes.id = best_matches.quote_id " +
                     condition_string + "ORDER BY RAND() LIMIT " + supplied_number)
    quotes = mycursor.fetchall()    
    
    final = [{"quote_id": item[0], "author": item[1], "title": item[2],
                 "headword": item[3], "edition": item[4], "content": item[5], "best_marked_by": item[6]} for item in quotes]
            
    mycursor.close()
    db.close()
    
    return jsonify(final)

@application.route('/unset_best_match', methods=['POST'])
@cross_origin()
def unset_get_match():
    supplied_token = request.form.get('token')
    if (supplied_token == None):
        return render_template("login.html")
    if token_number_exists(int(supplied_token)) is False:
       return render_template("login.html")
   
    # delete the currently set best match
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_quote_id = request.form.get('quote_id')    
    supplied_match_id = request.form.get('match_id');
    mycursor.execute("DELETE FROM best_matches WHERE quote_id = %s AND match_id = %s",
                     (supplied_quote_id, supplied_match_id))
    db.commit()
    
    # reset the best match for the quotation to be the one with the highest rating
    mycursor.execute("SELECT id, work_metadata_id FROM `matches` WHERE quote_id = %s " + 
                     "ORDER BY score DESC LIMIT 1", supplied_quote_id)
    default_match = mycursor.fetchall()
    default_match_id = default_match[0][0]
    default_work_metadata_id = default_match[0][1]
    mycursor.execute("INSERT INTO best_matches (quote_id, match_id, work_metadata_id, user_id) VALUES (%s, %s, %s, %s);",
                     (supplied_quote_id, default_match_id, default_work_metadata_id, None))
    db.commit()
    mycursor.close()
    db.close()
    return jsonify({'message': 'success'})
    
@application.route('/set_best_match', methods=['POST'])
@cross_origin()
def set_get_match():
    supplied_token = request.form.get('token')
    if (supplied_token == None):
        return render_template("login.html")
    if token_number_exists(int(supplied_token)) is False:
       return render_template("login.html")
   
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_quote_id = request.form.get('quote_id')
    
    # unset previous best match
    mycursor.execute("DELETE FROM best_matches WHERE quote_id = " + supplied_quote_id)
    db.commit()
    
    # set the specified best match
    supplied_match_id = request.form.get('match_id');
    supplied_work_metadata_id = request.form.get('work_metadata_id');
    user_id = user_id_from_token(int(supplied_token))
    mycursor.execute("INSERT INTO best_matches (quote_id, match_id, work_metadata_id, user_id) VALUES (%s, %s, %s, %s);",
                     (supplied_quote_id, supplied_match_id, supplied_work_metadata_id, user_id))
    db.commit()
    mycursor.close()
    db.close()
    return jsonify({'message': 'success'})
   
@application.route('/export', methods=['POST'])
@cross_origin()
def export():
    db = pymysql.connect(host="chdr.cs.ucf.edu", user="sjd_quotes", password="SJDquotes2020", db="SJDquotes")
    mycursor = db.cursor()
    supplied_condition = str(request.form.get('condition'))
    supplied_min = str(request.form.get('tMin'))
    supplied_max = str(request.form.get('tMax'))
    supplied_token = str(request.form.get('token'))
    
    # token and timestamp microseconds ensures the correct file can be identified by the frontend to fulfill a user's request
    filename = 'public_html/exports/bestMatchesExport_' + str(supplied_token) + str(int(datetime.utcnow().timestamp() * 1000000))
    
    condition_string = ''
    if supplied_condition == 'onlybest':
        condition_string = 'AND best_matches.user_id IS NOT NULL '
    elif supplied_condition == 'nobest':
        condition_string = 'AND best_matches.user_id IS NULL '
        
    min_max_string = 'AND matches.score >= ' + supplied_min + ' AND matches.score <= ' + supplied_max
    
    mycursor.execute("SELECT quote_metadata.author, quote_metadata.title, " +
                     "quote_metadata.headword, quote_metadata.edition, quotes.content, matches.score, " + 
                     "matches.content, work_metadata.title, work_metadata.author, work_metadata.filepath, " + 
                     "work_metadata.url, work_metadata.lccn FROM `quotes` " +
                     "LEFT JOIN `quote_metadata` ON quotes.id = quote_metadata.quote_id LEFT JOIN " +
                     "`best_matches` ON quotes.id = best_matches.quote_id LEFT JOIN `matches` on " +
                     "best_matches.match_id = matches.id LEFT JOIN `work_metadata` on " +
                     "matches.work_metadata_id = work_metadata.id " +
                     "WHERE (best_matches.match_id IS NOT NULL) " + condition_string + min_max_string)
        
    results = mycursor.fetchall()    
    
    final = [{"author": item[0], "title": item[1], "headword": item[2], "edition": item[3], 
              "content": item[4], "sourceContent": item[6], "sourceTitle": item[7],
              "sourceAuthor": item[8], "sourceURL": item[10], "sourceLCCN": item[11]} for item in results]
            
    mycursor.close()
    db.close()
    
    # write JSON to file and zip
    writeFile =open(filename + ".json", 'w')
    writeFile.write(json.dumps(final))
    writeFile.close()
    zipfile.ZipFile(filename + ".zip", mode='w', compression=zipfile.ZIP_DEFLATED).write(filename + ".json", 
                    "bestMatchesExport_" + str(supplied_token) + str(int(datetime.utcnow().timestamp() * 1000000)) + ".json")
   
    os.remove(filename + ".json")
    return jsonify({'filepath': str(os.getcwd()) + '/' + filename + ".zip"})

@application.route('/get_active_tokens', methods=['GET'])
@cross_origin()
def get_active_tokens():
    return json.dumps(active_tokens)

@application.route('/delete_old_tokens')
@cross_origin()
def delete_old_tokens():
    for x in active_tokens:
        if datetime.utcnow().timestamp() - x[2] >= 86400:
            active_tokens.remove(x)    
    
    return jsonify({'message': 'success'})
    
if __name__ == '__main__':
    application.run(host='localhost', port=5000)
