medlem
==========

[![Build Status](https://img.shields.io/travis/mozilla/medlem/master.svg)](https://travis-ci.org/mozilla/medlem)

[![Coverage status](https://img.shields.io/coveralls/mozilla/medlem/master.svg)](https://coveralls.io/r/mozilla/medlem)

About the project
-----------------

This project aims to set up a server for HTTP interfacing with LDAP.

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
