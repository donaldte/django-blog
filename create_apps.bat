@echo off
set target_directory=my_blog_saas

set apps=("likes" )

for %%a in %apps% do (
    python manage.py startapp %%a
    echo Created app: %%a

    move %%a %target_directory%
    echo Moved %%a to %target_directory%
)
