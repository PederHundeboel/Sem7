const mgrs = require("./mgrs/mgrs")
const express = require("express")
const app = express()

app.get("/", (req, res ) => {
    res.send("Root")
})


app.get("/api/android/:lat/:long", (req, res) => {
    let militaryGrid = mgrs.forward([parseInt(req.params.long),parseInt( req.params.lat)], 5)
    const jsonM = JSON.parse(`{"grid":"${militaryGrid}"}`)
    res.send(jsonM)
    console.log("Sent mgrs back", jsonM)
})
const port = process.env.PORT || 3000
app.listen(port, () => console.log(`listening on port ${port}...`))
