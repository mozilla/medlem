medlem
==========

[![Build Status](https://img.shields.io/travis/mozilla/medlem/master.svg)](https://travis-ci.org/mozilla/medlem)

[![Coverage status](https://img.shields.io/coveralls/mozilla/medlem/master.svg)](https://coveralls.io/r/mozilla/medlem)

About the project
-----------------

**THIS PROJECT IS IN PROTOTYPAL STAGES**

This project aims to set up a server for HTTP interfacing with LDAP.
Two core feature areas:

1) Be able to ask simple questions in HTTP GET and get a simple JSON response.
   For example "Is example@example.org still an employee of Example inc?"

2) If changes to membership happens, notify, by HTTP POST those who are
concerned to know this.

About the name
--------------

"medlem" means "member" in Swedish. Calling it just "member" would be too
common that it doesn't make for a good project name.

Also, LDAP it very depends on LDAP to get its source of truth. But that
might change in some future. At that point, the questions are still about
"membership".

Run the tests
-------------

To run the tests:

    python manage.py test

If you want to run the full suite, with flake8 and coverage, you may use
[tox](https://testrun.org/tox/latest/). This will run the tests the same way
they are run by [travis](https://travis-ci.org)):

    pip install tox
    tox

The `.travis.yml` file will also run [coveralls](https://coveralls.io) by
default.

If you want to benefit from Travis and Coveralls, you will need to activate
them both for your project.

Oh, and you might want to change the "Build Status" and "Coverage Status" links
at the top of this file to point to your own travis and coveralls accounts.



Heroku
------

(INSTRUCTIONS ARE NOT TESTED)

1. heroku create
2. heroku config:set DEBUG=False ALLOWED_HOSTS=<foobar>.herokuapp.com, SECRET_KEY=something_secret
   DATABASE_URL gets populated by heroku once you setup a database.
3. git push heroku master
