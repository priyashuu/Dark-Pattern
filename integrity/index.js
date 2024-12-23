var express = require("express");
var bodyParser = require("body-parser");
var mongoose = require("mongoose");
var cors = require("cors"); // Added for CORS support

const app = express();

app.use(cors()); // Enable CORS
app.use(bodyParser.json());
app.use(express.static('public'));
app.use(bodyParser.urlencoded({
    extended: true
}));

mongoose.connect('mongodb://localhost:27017/mydb', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log("Connected to Database");
}).catch((err) => {
    console.error("Error in Connecting to Database:", err);
});

var db = mongoose.connection;

db.on('error', () => console.log("Error in Connecting to Database"));
db.once('open', () => console.log("Connected to Database"));

// User schema
var userSchema = new mongoose.Schema({
    name: String,
    email: String,
    phno: String,
    password: String
});

var User = mongoose.model('User', userSchema);

// Sign-up endpoint
app.post("/sign_up", (req, res) => {
    var name = req.body.logname;
    var email = req.body.logemail;
    var phno = req.body.logphno;
    var password = req.body.logpass;

    var newUser = new User({
        name: name,
        email: email,
        phno: phno,
        password: password
    });

    newUser.save((err) => {
        if (err) {
            console.error(err);
            return res.redirect('signup_failed.html');
        }
        console.log("Record Inserted Successfully");
        return res.redirect('signup_success.html');
    });
});

// Login endpoint
app.post("/login", (req, res) => {
    var email = req.body.logemail;
    var password = req.body.logpass;

    User.findOne({ email: email, password: password }, (err, user) => {
        if (err) {
            throw err;
        }

        if (user) {
            console.log("Login Successful");
            return res.redirect('login_success.html');
        } else {
            console.log("Login Failed");
            return res.redirect('login_failed.html');
        }
    });
});

app.get("/", (req, res) => {
    res.set({
        "Access-Control-Allow-Origin": '*'
    });
    return res.redirect('loginindex.html');
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Listening on PORT ${3000}`);
});
