from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")

def main():
    return render_template ('template.html', notifications = notifications, alarms = alarms, title = title, image = image )


notifications = [{"title": "This is a title", "content": "This is the content"}]
alarms = 




title = "Daily Alarm Clock"


if __name__ == "__main__":
    app.run()
