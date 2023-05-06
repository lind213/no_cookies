from flask import Flask
from flask import (Blueprint, render_template, request)
import csv
import re
import sqlite3
from sys import platform
import random
import string
from datetime import datetime

# Create a Flask blueprint
bp = Blueprint('moja', __name__)

# Selects the correct database file depending on the platform
if platform == "linux" or platform == "linux2":
    db_path = '<file_path>'
    tegn_liste = '<file_path>'
    tegn_name = '<file_path>'
elif platform == "darwin":
    db_path = '<file_path>'
    tegn_liste = '<file_path>'
    tegn_name = '<file_path>'

# Creates a list of the sign names
sign_names = [ ]
with open(tegn_name, 'r') as csvfile:
    lineread = csv.reader(csvfile)
    for row in lineread:
        sign_names.append(row)

# Creates a list of the signs
filmene = [ ]
with open(tegn_liste, 'r') as csvfile:
    linereader = csv.reader(csvfile)
    for row in linereader:
        filmene.append(row[0])

#  Creates a list of the signs without the numbers
film_n = [ ]
for i in filmene:
    k = 1
    for j in sign_names:
        if i == j[1] and k == 1:
            film_n.append(j[0])
            k += 1
        else:
            pass

# Creates a list of the signs without file extensions
filmene_clean = [ ]
for i in filmene:
    cleannames = re.sub('\W+','', i)
    names = cleannames[:-3]
    filmene_clean.append(names)

# creates names of columns for the database
bkg_col = ['age', 'gender', 'hs', 'col', 'univ', 'other', 'lower', 'upper', 'middle', 'agets', 'region']

# Function to get the id number of the last row in the database
def get_id():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    a = 0
    for row in cur.execute('SELECT * FROM partinfo2;'):
        a += 1
    con.close()
    return a

# Function to add a new row to the database
def check_id(ide):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT partid FROM partinfo2 WHERE partid = ?;", (ide,))
    results = cur.fetchall()
    con.close()
    results = results[0][0]
    return results

# Function to get the long id from the database
def longer_id():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT id_string FROM partinfo2;")
    results = cur.fetchall()
    con.close()
    make_list = [ ]
    for i in results:
        make_list.append(i[0])
    return make_list

# Function to insert responses  to the database
def sql_update(the_film_list, ide, s_p, r_c):
    con = sqlite3.connect(db_path)
    secure_list = [ ]
    for i in filmene_clean:
        if i in the_film_list:
            secure_list.append(i)
    cur = con.cursor()
    if len(secure_list) == 4:
        a = secure_list[0]
        b = secure_list[1]
        c = secure_list[2]
        d = secure_list[3]
        sql = f"""
        UPDATE partinfo2
        SET {a} = 'yes', {b} = 'yes', {c} = 'yes', {d} = 'yes'
        WHERE id_string = ?;
        """
    elif len(secure_list) == 3:
        a = secure_list[0]
        b = secure_list[1]
        c = secure_list[2]
        sql = f"""
        UPDATE partinfo2
        SET  {a} = 'yes', {b} = 'yes', {c} = 'yes'
        WHERE id_string = ?;"""
    elif len(secure_list) == 2:   
        a = secure_list[0]
        b = secure_list[1]
        sql = f"""
        UPDATE partinfo2
        SET  {a} = 'yes', {b} = 'yes'
        WHERE id_string = ?;"""
    elif len(secure_list) == 1:
        a = secure_list[0]
        sql = f"""
        UPDATE partinfo2
        SET  {a} = 'yes'
        WHERE id_string = ?;"""
    else:
        sql = "SELECT partid FROM partinfo2 WHERE id_string = ?;"
    cur.execute(sql, (ide,))
    if s_p == 'pagetwo':
        cur.execute("UPDATE partinfo2 SET 'two_c' = ? WHERE id_string = ?;", (r_c, ide))
    elif s_p == 'pagethree':
        cur.execute("UPDATE partinfo2 SET 'three_c' = ? WHERE id_string = ?;", (r_c, ide))
    elif s_p == 'pagefour':
        cur.execute("UPDATE partinfo2 SET 'four_c' = ? WHERE id_string = ?;", (r_c, ide))
    elif s_p == 'pagefive':
        cur.execute("UPDATE partinfo2 SET 'five_c' = ? WHERE id_string = ?;", (r_c, ide))
    elif s_p == 'pagesix':
        cur.execute("UPDATE partinfo2 SET 'six_c' = ? WHERE id_string = ?;", (r_c, ide))
    elif s_p == 'pageseven':
        cur.execute("UPDATE partinfo2 SET 'seven_c' = ? WHERE id_string = ?;", (r_c, ide))
    elif s_p == 'pageeight':
        cur.execute("UPDATE partinfo2 SET 'eight_c' = ? WHERE id_string = ?;", (r_c, ide))
    else:
        pass
    con.commit()
    con.close()
    return secure_list

# Function to insert page visited to the database
def add_page(page, ide):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(f"UPDATE partinfo2 SET {page} = ? WHERE id_string = ?;", (page, ide))
    con.commit()
    con.close()

# Function to get the correct page to display
def get_pages(ide):
    the_results = [ ]
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT pagezero FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_0 = cur.fetchall()
    the_results.append(results_0[0][0])
    cur.execute("SELECT pageone FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_1 = cur.fetchall()
    the_results.append(results_1[0][0])
    cur.execute("SELECT pagetwo FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_2 = cur.fetchall()
    the_results.append(results_2[0][0])
    cur.execute("SELECT pagethree FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_3 = cur.fetchall()
    the_results.append(results_3[0][0])
    cur.execute("SELECT pagefour FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_4 = cur.fetchall()
    the_results.append(results_4[0][0])
    cur.execute("SELECT pagefive FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_5 = cur.fetchall()
    the_results.append(results_5[0][0])
    cur.execute("SELECT pagesix FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_6 = cur.fetchall()
    the_results.append(results_6[0][0])
    cur.execute("SELECT pageseven FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_7 = cur.fetchall()
    the_results.append(results_7[0][0])
    cur.execute("SELECT pageeight FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_8 = cur.fetchall()
    the_results.append(results_8[0][0])
    cur.execute("SELECT pagenine FROM partinfo2 WHERE id_string = ?;", (ide,))
    results_9 = cur.fetchall()
    the_results.append(results_9[0][0])
    con.close()
    null = None
    remove_null = list(filter(null, the_results))
    return_this = [i for i in remove_null if i!='no']
    return return_this

# Function to remove last page visited to the database
def remove_page(page, ide):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(f"UPDATE partinfo2 SET {page} = NULL WHERE id_string = ?;", (ide,))
    con.commit()
    con.close()

# Function to get the number of rows in the database
def ip_rows(ip_num):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    row_num = cur.execute(f"SELECT COUNT(*) FROM partinfo2 WHERE an_ip = ?;", (ip_num,)).fetchone()[0]
    con.close()
    return row_num

# Function to display the welcome page and register the long id
@bp.route('/welcome')
def start_her():
    get_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr) 
    anon_ip = re.match(".*(?=\.)", get_ip)
    get_time = datetime.now()
    characters = string.ascii_letters + string.digits
    long_id = ''.join(random.choice(characters) for i in range(20)) 
    get_ip_count = ip_rows(anon_ip.group(0))
    if get_ip_count > 200:
        return "Please wait while the webpage is loading..."
    else:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("INSERT INTO partinfo2('id_string') VALUES(?)", (long_id,))
        cur.execute("UPDATE partinfo2 SET 'pagezero' = 'pagezero' WHERE id_string = ?;", (long_id,))
        cur.execute("UPDATE partinfo2 SET 'tid' = ?, 'an_ip' = ? WHERE id_string = ?;", (get_time, anon_ip.group(0), long_id))
        con.commit()
        con.close()

        return render_template('tegn_temp/welcome.html', long_id = long_id)

# Function to display the last page
@bp.route('/end', methods = ['POST', 'GET'])
def final():
    if request.method == 'POST':
        dict_post = { }
        for keys, values in request.form.items():
            dict_post[keys] = values
        content = dict_post['review']
        ide = dict_post['partid']
        turn = dict_post['submitted']
        pages = get_pages(ide)
        try:
            sql_ide = check_id(ide)
        except:
            return render_template('tegn_temp/again.html', ide = 1000, turn = 10)
        if str(sql_ide) == ide and len(pages) == 8 and turn == str(8):
            add_page('pagenine', ide)
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("SELECT comment FROM partinfo2 WHERE partid = ?;", (ide,))
            cur.execute("UPDATE partinfo2 SET 'comment' = ? WHERE partid = ?;", (content, ide))
            con.commit()
            con.close()
            ide = 10000
            return render_template('tegn_temp/thanks.html', ide = ide)
        else:
            return render_template('tegn_temp/again.html', ide = 1000, turn = 10)

    else:
        message = "PLEASE RESPOND TO ALL THE QUESTIONS BEFORE CONTINUING"
        ide = int(get_id())+1
        turn = 1
        return render_template('tegn_temp/survey2.html', message = message, ide = ide)

# Function to display the multipage survey with films
@bp.route('/tegnspm', methods = ['POST', 'GET'])
def survey3():
    if request.method == 'POST':
        key_list = [ ]
        dict_post = { }
        for keys, values in request.form.items():
            dict_post[keys] = values
            key_list.append(keys)
        try:
            key_list.remove('review')
        except:
            pass
        only_films = key_list[:-2]
        clean_films = [ ]
        for i in only_films:
            cleanup = re.sub('\W+','', i)
            name = cleanup[:-3]
            clean_films.append(name)
        try:
            turn = dict_post['sb']
        except:
            pass
        try:
            rev_com = dict_post['review']
        except:
            rev_com = "comments not working"

        long_id = dict_post['otan']
        if 'submit' in clean_films:
            clean_films.remove('submit')
        the_long_id = longer_id()
        pages = get_pages(long_id)

        if long_id in the_long_id and pages[-1] == 'pageone' and turn == '2':
            sec_page = 'pagetwo'
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            films = filmene[4:8]
            film_ns = film_n[4:8]
            turn = 3
            return render_template('tegn_temp/next3.html', long_id = long_id, films = films, film_ns = film_ns, turn = turn)
        elif long_id in the_long_id and pages[-1] == 'pagetwo' and turn == '3':
            sec_page = 'pagethree'
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            films = filmene[8:12]
            film_ns = film_n[8:12]
            turn = 4
            return render_template('tegn_temp/next3.html', long_id = long_id, films = films, film_ns = film_ns, turn = turn)
        elif long_id in the_long_id and pages[-1] == 'pagethree' and turn == '4':
            sec_page = 'pagefour'   
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            films = filmene[12:16]
            film_ns = film_n[12:16]
            turn = 5
            return render_template('tegn_temp/next3.html', long_id = long_id, films = films, film_ns = film_ns, turn = turn)
        elif long_id in the_long_id and pages[-1] == 'pagefour' and turn == '5':
            sec_page = 'pagefive'
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            films = filmene[16:20]
            film_ns = film_n[16:20]
            turn = 6
            return render_template('tegn_temp/next3.html', long_id = long_id, films = films, film_ns = film_ns, turn = turn)
        elif long_id in the_long_id and pages[-1] == 'pagefive' and turn == '6':
            sec_page = 'pagesix'
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            films = filmene[20:24]
            film_ns = film_n[20:24]
            turn = 7
            return render_template('tegn_temp/next3.html', long_id = long_id, films = films, film_ns = film_ns, turn = turn)
        elif long_id in the_long_id and pages[-1] == 'pagesix' and turn == '7':
            sec_page = 'pageseven'
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            films = filmene[24:28]
            film_ns = film_n[24:28]
            turn = 8
            return render_template('tegn_temp/next3.html', long_id = long_id, films = films, film_ns = film_ns, turn = turn)
        elif long_id in the_long_id and pages[-1] == 'pageseven' and turn == '8':
            sec_page = 'pageeight'
            sql_update(clean_films, long_id, sec_page, rev_com)
            add_page(sec_page, long_id)
            turn = 9
            return render_template('tegn_temp/thanks.html')
       
        else:
            turn = len(pages) - 1
            if len(pages) == 2:
                remove_page('pageone', long_id)
            elif len(pages) == 3:
                remove_page('pagetwo', long_id)
            elif len(pages) == 4:
                remove_page('pagethree', long_id)
            elif len(pages) == 5:
                remove_page('pagefour', long_id)
            elif len(pages) == 6:
                remove_page('pagefive', long_id)
            elif len(pages) == 7:
                remove_page('pagesix', long_id)
            elif len(pages) == 8:
                remove_page('pageseven', long_id)
            else:
                remove_page('pageeight', long_id)
            return render_template('tegn_temp/again.html', long_id = long_id, turn = turn)

    else:
        message = "PLEASE RESPOND TO ALL THE QUESTIONS BEFORE CONTINUING"
        ide = int(get_id())+1
        turn = 1
        return render_template('tegn_temp/survey2.html', message = message, ide = ide)

# Function to display the background survey
@bp.route('/tegnid2', methods = ['POST', 'GET'])
def survey2():
    if request.method == 'POST':
        dict_post = { }
        clean_data = [ ]
        for keys, values in request.form.items():
            dict_post[keys] = values
            clean_data.append(keys)
        long_id = dict_post['otan']
        try:
            pages = get_pages(long_id)
        except:
            return pages
        try:
            turn = dict_post['sb']
        except:
            return "cant get sb"
        try:
            first = dict_post['fs']
        except:
            first = 'mt'
        the_long_id = longer_id()
        if long_id in the_long_id and pages[-1] == 'pagezero' and turn == '0':
            message = "PLEASE RESPOND TO ALL THE QUESTIONS BEFORE CONTINUING"
            turn = 1
            return render_template('tegn_temp/survey2.html', turn = turn, message = message, long_id = long_id)
        elif first == 'ls' and pages[-1] == 'pagezero' and turn == '1':
            films = filmene[:4]
            film_ns = film_n[:4]
            turn = 2
            sec_page = 'pageone'
            add_page(sec_page, long_id)
            return render_template('tegn_temp/next3.html', films = films, film_ns = film_ns, turn = turn, long_id = long_id)
        elif long_id in the_long_id and pages[-1] == 'pagezero' and turn == '1':
            if "age" and "gender" and ("hs" or "col" or "univ" or "other") and ("lower" or "upper" or "middle") and "agets" and "region" in clean_data:
                ide = int(get_id())+1
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                cur.execute("UPDATE partinfo2 SET 'partid' = ? WHERE id_string = ?;", (ide, long_id))                
                con.commit()
                for keys, values in dict_post.items():
                    for i in bkg_col:
                        if i == keys:
                            cur.execute(f"UPDATE partinfo2 SET {i} = ? WHERE id_string = ?;", (values, long_id))
            
                cur.execute("UPDATE partinfo2 SET 'pageone' = 'pageone' WHERE id_string = ?;", (long_id,))
                con.commit()
                con.close()

                films = filmene[:4]
                film_ns = film_n[:4]
                turn = 2
                return render_template('tegn_temp/next3.html', films = films, film_ns = film_ns, ide = ide, turn = turn, long_id = long_id)
            else:
                message = "PLEASE RESPOND TO ALL THE QUESTIONS BEFORE CONTINUING"
                return render_template('tegn_temp/survey2.html', message = message, long_id = long_id, turn = turn)
        else:
            turn = len(pages) - 1
            if len(pages) == 2:
                films = filmene[:4]
                remove_page('pageone', long_id)
                return render_template('tegn_temp/again2.html', long_id = long_id, turn = turn)
            elif len(pages) == 3:
                remove_page('pagetwo', long_id)
            elif len(pages) == 4:
                remove_page('pagethree', long_id)
            elif len(pages) == 5:
                remove_page('pagefour', long_id)
            elif len(pages) == 6:
                remove_page('pagefive', long_id)
            elif len(pages) == 7:
                remove_page('pagesix', long_id)
            elif len(pages) == 8:
                remove_page('pageseven', long_id)
            else:
                remove_page('pageeight', long_id)
            return render_template('tegn_temp/again.html', long_id = long_id, turn = turn)

    else:
        return("Not a valid page")

