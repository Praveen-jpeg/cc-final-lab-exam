from flask import Flask
import datetime

# AWS looks for a variable named 'application' by default.
application = Flask(__name__)

@application.route('/')
def hello():
    # Generate dynamic content by getting the current time
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # This is the HTML that will be sent to the browser
    return f"""
    <div style='font-family: Arial, sans-serif; text-align: center; margin-top: 50px;'>
        <h1>Hello from AWS App Runner!</h1>
        <p>This is a dynamic web application running as a managed service.</p>
        <p><strong>Current Server Time:</strong> {time_str}</p>
    </div>
    """

# This is for running the app locally (optional)
if __name__ == '__main__':
    application.run(debug=True)

