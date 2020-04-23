testing:
	echo "➡️  $m"

git:
	git add .
	git commit -m "$m"
	git push -u origin master

heroku:
	heroku ps:exec
	ls -lha /app/
