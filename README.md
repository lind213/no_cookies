# no_cookies
Flask survey without cookies, browser fingerprinting, or login<br /><br />

The [blueprint](https://flask.palletsprojects.com/en/2.3.x/blueprints/) file, [moja.py](https://github.com/lind213/no_cookies/blob/main/moja.py), for the Flask web framework, is the main script of a multipage survey that does not rely on cookies or browser fingerprinting. Users are tracked through HTTP POST requests instead. This survey asks users across multiple pages whether they’ve seen a set of short clips before (yes/no question).<br /><br />
On the introductory page, a user is assigned a string of 20 random ASCII characters. This string is stored in a SQL database and included in a hidden input in a POST form on all subsequent webpages, using [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) HTML templates. The subsequent pages use the POST form to return the string and other data to the Flask server. The user is identified each time by searching the SQL database for the string received through POST. To prevent multiple POST requests from the same webpage (e.g., if the user presses the back button and answers questions on the previous page again), the user's navigation is tracked and recorded in the SQL database.<br /><br />
The code was used once for a pilot study and may be improved. No license is attached.<br /><br />
The SQL database consists of columns for the participant’s unique string, pages visited, and so on, but also includes one column for each short clip (film) included in the survey. The cells in these film columns contain either “no” or are blank (indicating "yes"). The film columns were created in Python by iterating through a list of film names (the list named “movies” below) and altering the SQL database:<br />

```
con = sqlite3.connect("<file_path>")
cur = con.cursor()
for i in movies:
	#removing “.mp4” from the end
	clean_word = re.sub('\W+','', i)
	name = clean_word[:-3]
	sql = f"ALTER TABLE partinfo2 ADD {name} VARCHAR;"
	cur.execute(sql)
con.commit()
con.close()
```
