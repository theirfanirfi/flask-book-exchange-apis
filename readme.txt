for running this application, the following requirements must be fulfilled:

1. install python3 (and pip3)
2. install Flask via Pip(3)
3. install all the required modules by running the follwoing command in the application directory:

    pip3 install -r requirements.txt

4. create a mysql database with name "cms"
5. The username and password to the database connection are set as:
        root:root
        if the username and password are different it must be entered in the config file

6. export the variables mentioned in the export_vars.sh file
7. migrate the models to database by running the following commands
    Flask db init
    Flask db migrate -m "initial migration"
    Flask db upgrade
all the models will be migrated.

