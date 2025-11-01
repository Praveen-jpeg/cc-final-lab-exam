from flask import Flask, request, render_template_string, redirect, url_for
import datetime

# AWS App Runner and Elastic Beanstalk look for this 'application' variable
application = Flask(__name__)

# --- HTML Template ---
# We'll use a single base template to keep our app in one file.
# The {{ content | safe }} part is where we'll inject our page content.
base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Lab App</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; 
            background-color: #f4f4f9; 
            margin: 0; 
            padding: 20px; 
        }
        .container { 
            max-width: 600px; 
            margin: 20px auto; 
            padding: 20px; 
            background-color: #ffffff; 
            border-radius: 8px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
        }
        h1 { color: #333; }
        p { line-height: 1.6; color: #555; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .form-group { margin-bottom: 15px; }
        .form-group label { 
            display: block; 
            margin-bottom: 5px; 
            font-weight: 600; 
        }
        .form-group input, 
        .form-group textarea { 
            width: 95%; 
            padding: 10px; 
            border: 1px solid #ccc; 
            border-radius: 4px; 
            font-size: 16px;
        }
        .btn { 
            display: inline-block; 
            padding: 12px 18px; 
            background-color: #007bff; 
            color: #ffffff; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: 600;
        }
        .btn:hover { background-color: #0056b3; }
        .time { color: #555; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        {{ content | safe }}
    </div>
</body>
</html>
"""

# --- Application Routes ---

# Route 1: Home Page (Dynamic Time)
@application.route('/')
def home():
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(ist)
    time_str = now.strftime("%Y-%m-%d %H:%M:%S IST")
    
    # This is the HTML content for the home page
    home_content = f"""
    <h1>Welcome to the Lab Exam App!</h1>
    <p>This is a dynamic web application showing the current server time.</p>
    <p class="time">
        <strong>Current Server Time:</strong> 
        <span id="ist-time">{time_str}</span>
    </p>
    <script>
        // Get the initial time string from the server
        let timeString = "{time_str}";
        // Parse it into a JS Date object (adjust for IST offset)
        let initialDate = new Date();
        // The server gives IST, so let's re-parse it
        let parts = timeString.split(' ');
        let dateParts = parts[0].split('-');
        let timeParts = parts[1].split(':');
        // JS Date: new Date(year, month-1, day, hour, minute, second)
        initialDate = new Date(
            Number(dateParts[0]), 
            Number(dateParts[1])-1, 
            Number(dateParts[2]), 
            Number(timeParts[0]), 
            Number(timeParts[1]), 
            Number(timeParts[2])
        );

        function pad(n) { return n < 10 ? '0' + n : n; }

        function updateISTTime() {
            initialDate.setSeconds(initialDate.getSeconds() + 1);
            let y = initialDate.getFullYear();
            let m = pad(initialDate.getMonth()+1);
            let d = pad(initialDate.getDate());
            let h = pad(initialDate.getHours());
            let min = pad(initialDate.getMinutes());
            let s = pad(initialDate.getSeconds());
            document.getElementById('ist-time').textContent = `${y}-${m}-${d} ${h}:${min}:${s} IST`;
        }
        setInterval(updateISTTime, 1000);
    </script>
    <hr>
    <p>Please provide your student feedback:</p>
    <a href="/feedback" class="btn">Go to Feedback Form</a>
"""
    # We render the base template and inject our home_content into it
    return render_template_string(base_template, content=home_content)

# Route 2: Feedback Form (Handles GET and POST)
@application.route('/feedback', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        # --- THIS IS THE DYNAMIC PART ---
        # The server processes the incoming data from the form
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['feedback']
        
        # In a real app, you would save this to a database.
        # For this lab, we just print it to the server logs...
        print(f"Received feedback from {name} ({email}): {feedback_text}")
        
        # ...and redirect to a "Thank You" page, passing the name.
        return redirect(url_for('thank_you', name=name))
    
    # This is the GET request part: just show the form
    form_content = """
        <h1>Student Feedback Form</h1>
        <p>Please fill out the form below.</p>
        
        <!-- The form will POST to this same URL (/feedback) -->
        <form method="POST" action="/feedback">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="feedback">Feedback or Comments:</label>
                <textarea id="feedback" name="feedback" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn">Submit Feedback</button>
        </form>
        <br>
        <a href="/">Back to Home</a>
    """
    return render_template_string(base_template, content=form_content)

# Route 3: Thank You Page
@application.route('/thankyou')
def thank_you():
    # --- THIS IS ALSO DYNAMIC ---
    # It reads the 'name' from the URL query to personalize the page
    name = request.args.get('name', 'Student') # Default to 'Student'
    
    thank_you_content = f"""
        <h1>Thank You, {name}!</h1>
        <p>Your feedback has been received.</p>
        <a href="/">Return to Home Page</a>
    """
    return render_template_string(base_template, content=thank_you_content)

# This is for running the app locally (optional)
if __name__ == '__main__':
    application.run(debug=True)

