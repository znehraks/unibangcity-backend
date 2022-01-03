require("dotenv").config();
const express = require("express");
const bodyParser = require("body-parser").json();
const cors = require("cors");
const spawn = require("child_process").spawn;
const app = express();
const connection = require("./connection");

const corsOptions = {
  origin: "*",
  credentials: true,
};
app.use(cors(corsOptions));

app.post("/recommendation", bodyParser, (req, res) => {
  let data = "";
  try {
    const result = spawn("python", [
      __dirname + "\\python_code\\cal_weight.py",
      req.body.Q1Answer,
      req.body.univ_lon,
      req.body.univ_lat,
      req.body.Q2Answer,
      req.body.Q3Answer,
      req.body.Q4Answer,
      req.body.Q5Answer,
    ]);
    result.stdout.on("data", (dataToSend) => {
      // console.log(dataToSend.toString("utf8"));
      data += dataToSend;
    });
    result.on("close", (code) => {
      if (code !== 0) {
        console.log(`child process close all stdio with code ${code}`);
      }
      res.json({ success: true, data: data });
      return;
    });
    result.stderr.on("data", (dataToSend) => {
      res.json({
        success: false,
        err_code: -1,
        err_msg: "불러오기에 실패했습니다. 다시 시도해주세요!",
        err_content: dataToSend,
      });
      return;
    });
  } catch (e) {
    console.log(e);
    res.json({
      success: false,
      err_code: -2,
      err_msg: "오류가 발생했습니다.",
    });
    return;
  }
});

app.post("/recommendation/create", bodyParser, (req, res) => {
  console.log(req.body);
  const sql = `INSERT INTO recommendation_result( univ_name, univ_lat, univ_lon, scrapper_code, rank01_T, rank02_T, rank03_T, rank04_T, rank05_T, avg_T) VALUES('${req.body.univ_name}', ${req.body.univ_lat}, ${req.body.univ_lon}, '${req.body.scrapper_code}', '${req.body.rank01_T}', '${req.body.rank02_T}', '${req.body.rank03_T}', '${req.body.rank04_T}', '${req.body.rank05_T}', '${req.body.avg_T}')`;
  connection.query(sql, (err, data, fields) => {
    if (err) {
      res.send({
        success: false,
        err_msg: "오류가 발생했습니다",
        err_code: -3,
      });
    }
    res.send({ success: true });
  });
});

app.listen(process.env.PORT, () => {
  console.log(`listening on PORT: ${process.env.PORT}`);
});
