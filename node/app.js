const express = require("express")
const app = express()

app.get("/", (req, res ) => {
    res.send("Root")
})


app.get("/api/android/:lat/:long", (req, res) => {
    console.log("placeholder")
})

const port = process.env.PORT || 3000
app.listen(port, () => console.log(`listening on port ${port}...`))
