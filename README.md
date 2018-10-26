Website Monitor
===============

"When hosted monitoring is either *too expensive* or *too complicated*."

Say you have a hundred or more websites and you want to receive
a Slack notification when one of them goes down;
and another notification when it comes back up.

Website Monitor does exactly this, and is configured by a single YAML file.


The Competition
---------------

If you are flush with both cash and patience, you might want to skip
this and head on over to [site24x7.com](https://site24x7.com).
Otherwise, read on.


Status Code and Expected Text
-----------------------------

Website monitor checks two things. First, it checks that the status
code of the GET request is 200. Second, it checks that the expected_text
that you specified in the YAML file is contained in the returned html.


Requirements
------------

  * Python 3.6 or later (because f-strings)
  * Read/Write access to the observations/ directory.


Installation
------------

    git clone git@github.com:jackdesert/website-monitor
    cd website-monitor
    pyenv local 3.6.6 # Choose any version 3.6 or later
    python -m pip install bs4 pyyaml lxml


Configuration
-------------

Make a config file:

    cd website-monitor/config
    cp sites.yml-EXAMPLE sites.yml
    vi sites.yml

Change the `webhook_url` to one provided by Slack.

Remove the example sites and enter your own sites. For each site, be sure
to put a word or phrase that Website Monitor should expect in the body of the
response.


Running from Command Line
-------------------------

    cd website-monitor/lib
    python website_monitor.py


Running as a Daemon
-------------------

Once you have this up and running, you will probably want to set it up
to run as a daemon. A systemd unit file is provided.

    cd /lib/systemd/system
    sudo ln -s /path/to/site-monitor/config/site-monitor.service
    sudo systemctl enable site-monitor.service
    sudo systemctl start site-monitor.service


Running Tests
-------------

    cd website-monitor/lib
    python3 -m unittest discover -s ../test


Backlog
-------

* Simple web page that shows the current status of all the monitors
  - green on the left; red on the right
* Only allow one thread to print to screen at a time.
* Fix so that messages written to the system journal show up immediately,
  instead of delayed and all in a group


Icebox
------

* Include status code with DOWN messages
* Included any exceptions raised with DOWN messages
monitor
=======

Getting Started
---------------

- Change directory into your newly created project.

    cd monitor

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools requests pyaml mock lxml

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
