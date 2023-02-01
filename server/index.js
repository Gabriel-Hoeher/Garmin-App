const express = require('express');

let app = express();

app.use(express.static('public'));
app.use(express.urlencoded({extended: false}));

app.set('/public/templates', __dirname + '/public/templates');
app.set('view engine', 'pug');

app.get('/', (req, res) => {
    res.render('Hi');
});



app.set('port', process.env.PORT || 7100);      //set port 6500

app.listen(app.get('port'), () => {
    console.log(`Listening on port ${app.get('port')}.`);
});