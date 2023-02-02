const express = require('express');
const fs = require('fs');

let app = express();

app.use(express.static('public'));
app.use(express.urlencoded({extended: false}));

app.set('/public/templates', __dirname + '/public/templates');
app.set('view engine', 'pug');

app.get('/', (req, res) => {
    res.render('Home');
});

app.post('/getData', (req, res) => {
    fs.readFile('./../activity_data/jsonData.json', 'utf8', (err, d) => {
        if (err) {
            console.error(err);
            return;
        }
        data = JSON.parse(d)
        
        newData = []
        for (const i in data.data) {
            let json = {};
            for (const y in data.data[i]) {
                json[data.columns[y]] = data.data[i][y];
            }
            newData.push(json);
        }
        res.send(newData);
    })
});

app.set('port', process.env.PORT || 7100);      //set port 6500

app.listen(app.get('port'), () => {
    console.log(`Listening on port ${app.get('port')}.`);
});