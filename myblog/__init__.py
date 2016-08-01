from flask import Flask
app = Flask(__name__)
app.config.from_object('myblog.dfconfig')
import myblog.views
