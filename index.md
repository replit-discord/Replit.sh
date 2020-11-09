# Replit.sh: Repl.it's Internal URL Shortener
## Preface
If you follow [@replit](https://twitter.com/replit) on Twitter, you may have realized some links showing up on our posts starting with the url [replit.sh](https://replit.sh). I have been working on it for almost two weeks now and have decided it is ready for public use. 

## Notes:
- This URL Shortener can only be run on Repl.it due to it using [Repl.it DB](https://docs.repl.it/misc/database).
- Users are managed with [Repl.it Auth](https://repl.it/talk/learn/Authenticating-users-with-Replit-Auth/23460), so keep that in mind.

## Getting Setup
1. Setting Up Your Repl
	1. Press the `run on repl.it` button below to clone the repository and install the packages:
[![Run on Repl.it](https://repl.it/badge/github/pieromqwerty/Replit.sh)](https://github.com/pieromqwerty/Replit.sh)
	2. After running your repl, go to to `line 11` in `main.py` and replace `https://replit.sh/` with the url your repl is being served to.
	3. Replace `Replit.sh` on `line 12` with the name of your site.
2. Setting Up Your Users
	1. Rename `sample.env` to `.env`, as it will be where your user ids are stored. 
	2. Head over to `https://[Your URL]/getid`, login with Repl.it, and then copy the user id you are given. 
	3. Paste the URL into the array in your `.env` file. 
		1. For example, if you are the only user and your id is `123456` then your `.env` file should look like `[123456]`. If you 
		2. If you wanted to add your friend who has id `654321`, your `.env` file would look like `[123456,654321]`.
3. Stop and Start the repl to complete your changes.

## Features
- Simple Login Through Repl.it:
![Login with Repl.it](http://static.piemadd.com/blogposts/replit.sh/login1.jpg)
![Login with Repl.it](http://static.piemadd.com/blogposts/replit.sh/login2.jpg)
- Dashboard of all links for a user:
![Dashboard](http://static.piemadd.com/blogposts/replit.sh/dash.jpg)
- Easy to use home-page:
![Homepage](http://static.piemadd.com/blogposts/replit.sh/home.jpg)
- Custom URLs:
![Custom URLs](http://static.piemadd.com/blogposts/replit.sh/custom.jpg)
- Editing URLs:
![Editing URLs](http://static.piemadd.com/blogposts/replit.sh/edit.jpg)
- Database I/O:
![Database I/O](http://static.piemadd.com/blogposts/replit.sh/dbio.jpg)
- Deleting URLs:
![Deleting URLs](http://static.piemadd.com/blogposts/replit.sh/delete.jpg)
