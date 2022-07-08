'''
BSD 3-Clause License

Copyright (c) 2022, Ethan Dalool aka voussoir
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import os

'''
bot.py template for PRAW4

This file will be imported by all bots, and provides a standard way to log in.

You should never place this file in a git repository or any place where it will
get shared.

The requirements for this file are:

1   A function `anonymous` with no arguments, which returns a `praw.Reddit`
    instance that has a Useragent but is otherwise anonymous / unauthenticated.
    This will be used in bots that need to make requests but don't need any
    permissions.

2   A function `login` with optional parameter `r`, which returns an
    authenticated Reddit instance.
    If `r` is provided, authenticate it.
    If not, create one using `anonymous` and authenticate that.
    Either way, return the instance when finished.

The exact workings of these functions, and the existence of any other variables
and functions are up to you.

I suggest placing this file in a private directory and adding that directory to
your `PYTHONPATH` environment variable. This makes it importable from anywhere.

However, you may place it in your default Python library. An easy way to find
this is by importing a standard library module and checking its location:
>>> import os
>>> os
<module 'os' from 'C:\\Python36\\lib\\os.py'>

But placing the file in the standard library means you will have to copy it over
when you upgrade Python.

If you need multiple separate bots, I would suggest creating copies of this file
with different names, and then using `import specialbot as bot` within the
application, so that the rest of the interface can stay the same.
'''

# The USERAGENT is a short description of why you're using reddit's API.
# You can make it as simple as "/u/myusername's bot for /r/mysubreddit".
# It should include your username so that reddit can contact you if there
# is a problem.
USERAGENT = os.environ.get('USERAGENT')

# CONTACT_INFO can be your reddit username, or your email address, or any other
# means of contacting you. This is used for some bot programs but not all.
CONTACT_INFO = os.environ.get('CONTACT_INFO')

# It's time to get your OAuth credentials.
#  1. Go to https://old.reddit.com/prefs/apps
#  2. Click create a new app
#  3. Give it any name you want
#  4. Choose "script" type
#  5. Description and About URI can be blank
#  6. Put "http://localhost:8080" as the Redirect URI
#  7. Now that you have created your app, write down the app ID (which appears
#     under its name), the secret, and the URI (http://localhost:8080) in the
#     variables below:
APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
APP_URI = os.environ.get('APP_URI')
#  8. Go to https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html#obtaining-refresh-tokens
#  9. Copy that script and save it to a .py file on your computer
# 10. The instructions at the top of the script tell you to run two "EXPORT"
#     commands before running the script. This only works on Unix. If you are on
#     Windows, or simply don't want to bother with environment variables, ignore
#     that part of the instructions and instead add `client_id='XXXX'` and
#     `client_secret='XXXX'` into the praw.Reddit constructor that you see on
#     line 40 of that script. When I say XXXX I mean the values you just wrote
#     down.
# 11. Run the script on your command line `python obtain_refresh_token.py`
# 12. Write down the refresh token that it gives you:
APP_REFRESH = os.environ.get('APP_REFRESH')

################################################################################

import praw

def anonymous():
    r = praw.Reddit(
        user_agent=USERAGENT,
        client_id=APP_ID,
        client_secret=APP_SECRET,
    )
    return r

def login(r=None):
    new_r = praw.Reddit(
        user_agent=USERAGENT,
        client_id=APP_ID,
        client_secret=APP_SECRET,
        refresh_token=APP_REFRESH,
    )
    if r:
        r.__dict__.clear()
        r.__dict__.update(new_r.__dict__)
    return new_r
