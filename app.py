# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'