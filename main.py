#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

def style_error(message):
    return "<span style='color: red;'> " + message + "</span>"

def build_page(postVars):
    username_label = "<label>Username:</label>"
    username_input = "<input type='text' name='username' value='" + postVars.username + "' />"
    username_error = style_error(postVars.username_error)

    password_label = "<label>Password:</label>"
    password_input = "<input type='password' name='password' value='" + postVars.password + "' />"
    password_error = style_error(postVars.password_error)

    ver_pwd_label = "<label>Verify Password:</label>"
    ver_pwd_input = "<input type='password' name='ver_pwd' />"
    ver_pwd_error = style_error(postVars.ver_pwd_error)

    email_label = "<label>Email(optional):</label>"
    email_input = "<input type='text' name='email' value='" + postVars.email + "' />"
    email_error = style_error(postVars.email_error)

    submit = "<input type='submit' />"

    form = ("<form method='post'>" +
            "<table>" +
            "<tr>" +
            "<td>" + username_label + "</td><td>" + username_input + username_error + "</td>" +
            "</tr><tr>" +
            "<td>" + password_label + "</td><td>" + password_input + password_error + "</td>" +
            "</tr><tr>" +
            "<td>" + ver_pwd_label + "</td><td>" + ver_pwd_input + ver_pwd_error + "</td>" +
            "</tr><tr>" +
            "<td>" + email_label + "</td><td>" + email_input + email_error + "</td>" +
            "</tr>" +
            "</table>" +
            submit +
            "</form>")

    header = "<h1>User Signup</h1>"

    return header + form

class PostVars:
    def __init__(self):
        self.username = ""
        self.username_error = ""
        self.password = ""
        self.password_error = ""
        self.ver_pwd = ""
        self.ver_pwd_error = ""
        self.email = ""
        self.email_error = ""

class SignupHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page(PostVars())
        self.response.write(content)

    def post(self):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        form_is_valid = True

        postVars = PostVars()
        postVars.username = self.request.get("username")

        if not USER_RE.match(postVars.username):
            postVars.username_error = "Please enter a username between 3 and 20 letters, numbers, underscors, or hyphens."
            form_is_valid = False

        postVars.password = self.request.get("password")

        if not PASSWORD_RE.match(postVars.password):
            postVars.password_error = "Passwords must be between 3 and 20 characters."
            form_is_valid = False

        postVars.ver_pwd = self.request.get("ver_pwd")

        if form_is_valid and postVars.password != postVars.ver_pwd:
            postVars.ver_pwd_error = "Verify password does not match above password."
            form_is_valid = False

        postVars.email = self.request.get("email")

        if postVars.email != "" and not EMAIL_RE.match(postVars.email):
            postVars.email_error = "Please enter a valid email address."
            form_is_valid = False

        if (form_is_valid):
            self.redirect("/welcome?name=" + postVars.username)
        else:
            content = build_page(postVars)
            self.response.write(content)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("name")
        content = "<h1>Welcome, " + username + "!</h1>"

        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
