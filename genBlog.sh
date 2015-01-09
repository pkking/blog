rm -rf pkking/*
pelican -s pelicanconf.py

if [ -n "$1" ];then
    git add -A 
    git commit -m"$1"
    git push gitcafe master
    cd pkking
    git add -A
    git commit -m"$1"
    git push origin gitcafe-pages
else
    git add -A 
    git commit -m"update"
    git push gitcafe master
    cd pkking
    git add -A
    git commit -m"update"
    git push origin gitcafe-pages
fi
