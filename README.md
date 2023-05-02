# no_cookies
Flask survey without cookies, browser fingerprinting, or login<br /><br />

The [blueprint](https://flask.palletsprojects.com/en/2.3.x/blueprints/) file, [moja.py](https://github.com/lind213/no_cookies/blob/main/moja.py), for the Flask web framework, is the main script of a multipage survey that does not rely on cookies or browser fingerprinting. Users are tracked through HTTP POST requests instead. This survey asks users across multiple pages whether they’ve seen a set of short clips before (yes/no question).<br /><br />
On the introductory page, a user is assigned a string of 20 random ASCII characters. This string is stored in a SQL database and included in a hidden input in a POST form on all subsequent webpages, using [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) HTML templates. The subsequent pages use the POST form to return the string and other data to the Flask server. The user is identified each time by searching the SQL database for the string received through POST. To prevent multiple POST requests from the same webpage (e.g., if the user presses the back button and answers questions on the previous page again), the user's navigation is tracked and recorded in the SQL database.<br /><br />
The code was used once for a pilot study and may be improved. No license is attached.<br /><br />
The SQL database comprises columns representing various participant data, such as an unique 20 character id string, pages visited, and more. Additionally, it includes a dedicated column for each short film clip featured in the survey. Within these film columns, cells either contain "no" or are left blank, which implies "yes." To create these film columns, a Python script iterated through a list of film names, referred to as "movies," and modified the SQL database accordingly:<br />

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
