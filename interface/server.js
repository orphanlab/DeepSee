const path = require("path");
const express = require("express");
const app = express();
const port = 8080;

// For all GET requests, send back index.html
// so that PathLocationStrategy can be used
app.use(express.static(path.join(__dirname, "dist")));

// Send the index.html whatever the request is.
app.get("*", (req, res) => {
  res.sendFile(path.resolve(__dirname, "dist", "index.html"));
});

// spin up the server
app.listen(process.env.PORT || port, () => {
  console.log(`Express serving at http://0.0.0.0:${port}`);
});
