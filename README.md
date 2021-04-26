# Brightwheel Email Server API Demo

Hello!  Welcome to the Brightwheel Email Server API.  This API provides an easy way
to direct email traffic to one of two 3rd-party email services; namely, Sendgrid and
Snailgun.

## Getting Started

To get started using the API, first `git clone` this repository.  Then, make sure
that you have Python 3.6 or greater installed on your computer (this will also ensure
that you have `venv`).  You will also need `pip` to start this project (if you don't
have it, you can get it here: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Next, navigate to the directory you just created and enter the following commands in your terminal:

```
python3 -m venv ENV
source ENV/bin/activate
```

This will start the virtual environment, which is important to keep the versions of
your libraries accounted for.  Next, type this command in the terminal:

```
pip install -r requirements.txt
```

This will install the project requirements, of which there are the following:
1. aiohttp (to support Sanic)
2. beautifulsoup4 (for HTML parsing and plain text generation)
3. requests (for HTTP)
4. sanic (for the main service)
5. sanic-testing (for testing)

At this point, you are ready to go!

## Using the API

To continue using the API, from within the project directory (if you are following
this tutorial, you should be exactly there), type the following command:

```
python api.py
```

This will start the Sanic server running on localhost.  To see the server running,
you can navigate to this url in your browser: http://127.0.0.1:8000/

To invoke the relevant endpoints in the service, open another window or tab in your
command line, and enter the following command, providing your API Key for the relevant
service, as well as an email body in JSON format:

```
python bwemail.py -b '{"to": "susan@abcpreschool.org", "to_name": "Miss Susan", "from": "noreply@mybrightwheel.com", "from_name": "brightwheel", "subject": "Your Weekly Report", "body": "<h1>Weekly Report</h1><p>You saved 10 hours this week!</p>"}' -k "YOUR_API_KEY_IN_QUOTES"
```

The module `bwemail.py` (for "Brightwheel Email") is used to parse arguments on the command line.  The argument `-b` corresponds with the body of JSON, and the argument `-k` corresponds with your API Key.

Additionally, feel free to run the test suite, in the `sanity_check.py` file, by entering the following command:

```
python sanity_check.py
```

Also, you can change the targeted 3rd-party service in the file `config.py` by adjusting the
`EMAIL_SERVICE_PROVIDER` variable.


## High-Level Engineering and Design

The Data API was developed using the Sanic microframework in Python.  I used Python because it is a language
I am familiar with, and I knew about the server technology Sanic, as well.  Sanic is similar to Flask, another
well-known microframework, but has support for asynchronous calls, which I judged would be useful
given the specifications.  Python in general is quick to develop (another reason I elected to use it here), but
has some trouble, usually, with concurrency.  Sanic, I believe, helps deal with this.  In fact, it was used here for the following
reasons:

1. **Sanic is a lightweight solution** which seemed to match the relatively-light requirements
set forth in the problem description.
2. **Sanic is highly extensible and customizable,** which seemed to fit the open-ended
nature of the problem description.
3. **Sanic has the flexibility** to support different kinds of data solutions, if the decision
was made in the future to persist data.  I chose not to use a datastore here, because it wasn't necessary
given the specifications (this service is only meant to re-direct data, not necessarily store it.  It would
be more expensive, in dollars, if we did!).  However, Sanic works well with a relational solution,
as well as a more highly-available NoSQL solution (which could be appropriate for JSON email
data, as shown here.)
4. **Sanic supports fast, asynchronous calls** for Python 3.6+.  This seemed to work well with the
scale of the problem.  The service would need to support millions or tens of millions (or even
more!) emails, and any support that the service can use in making calls asynchronously would be
beneficial.

It is worthwhile to note a couple of things:
1. Even though Sanic is a fast, asynchronous and light microframework, this type of server would
benefit from a message queueing technology, to scale up performance even further.  There are a
number of cloud solutions and technologies to solve for this.
2. The service does represent a "single point of failure" in the sense that even if either Sendgrid or
Snailgun goes down, there is still the possibility that this service itself could go offline (hopefully no one trips over the power cord).  
To mitigate this risk, we could introduce some redundancy into our architecture, if we perceive this to be a risk.
3. Importantly, in developing this project, I took a short-cut by including the relevant API keys in the code
base itself.  **This is a major security issue!!**  Given the time constraint and the fact that the APIs are very
likely to be for practice, I decided that this would be a safe choice.  However, it is very important to note
that if this were the real thing, we would need to use Amazon's Key Management Store (KMS), Gitlab/Github's secure
environment variables support, or another such solution.  I did choose to use argument parsing on the command
line as much as possible, to keep API Keys out of the code base, although I was blocked when trying to write unit tests
in this way.
4. I could have organized the code a little bit better.  In a real production app, we would have directories for
"tests", "configurations" and the like.  It turned out that Python's imports seem to have changed with the latest
version of Python 3, and I didn't have the time to investigate why certain module imports were failing.  Since
the service rests on only six files, I thought that it wouldn't be too unorganized to include everything in one
directory, although, in production this would look very different.
5. In writing the data schema, I elected to use a different key attribute than the word "from", which makes sense
given an email, but is actually a protected word in the Python language!  Therefore, additional logic needed to be
written when validating fields, which I've included in the file `utils.py`.

## TODOs: Getting It In Production

There are a number of action items to consider before moving this application into production.  Here are some of those line-items:

1. **Unit/Integration Tests -** the Email API comes with a file where even more unit tests and integration tests could be written.  There are a number of test cases to write before this app would be
safely ready for a production environment.

2. **Security -** Will the emails passing through the Email API have PII in them?  Is there a risk of some nefarious sniffing around the Email Service?  We could, and should, certainly
weigh all possible security risks before moving this into production.

3. **Environment Configurations -** the Email API is only configured to work on a local machine at this
time, and would need additional configuration to be supported in different environments.

4. **Containerization -** currently, the Email API has no support for containerization, although it could benefit from this technology.

5. **CI/CD -** in production, is there an established continuous deployment or integration testing pipeline, with its own configurations that need to be part of the Email API?

That's it!!  I hope you enjoyed reading through this; I had a very fun time writing these docs and developing this service.
