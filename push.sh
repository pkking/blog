pelican -s pelicanconf.py content -o output
git add .
git commit -m"update"
git push
cd output
git add . 
git commit -m "Update"
git push
cd ..
