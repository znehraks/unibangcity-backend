const mysql = require("mysql");

const con = mysql.createConnection({
  host: process.env.HOST,
  user: process.env.USER,
  password: process.env.PASSWORD,
  database: process.env.DATABASE,
  port: process.env.DATABASEPORT,
  SSL: Boolean(process.env.SSL),
});
console.log("connected");
module.exports = con;
