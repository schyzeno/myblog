from flask import Flask
app = Flask(__name__)
app.config.from_object('myblog.dfconfig')
import myblog.views
if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=5000
    )
