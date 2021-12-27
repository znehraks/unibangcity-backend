require("dotenv").config();
const express = require("express");
const bodyParser = require("body-parser").json();
const cors = require("cors");
const spawn = require("child_process").spawn;
const app = express();

const corsOptions = {
  origin: "*",
  credentials: true,
};
app.use(cors(corsOptions));

app.post("/", bodyParser, (req, res) => {
  const result = spawn("python", [
    __dirname + "\\python_code\\cal_weight.py",
    req.body.univ_name,
    req.body.univ_lon,
    req.body.univ_lat,
    req.body.limit_dist,
    req.body.first_weight,
    req.body.second_weight,
    req.body.third_weight,
    req.body.w1,
    req.body.w2,
    req.body.w3,
    req.body.w4,
    req.body.w5,
  ]);
  result.stdout.on("data", (data) => {
    console.log(data.toString("utf8"));
    res.json({ success: true, data: data.toString("utf8").trim() });
  });
  result.stderr.on("data", (data) => {
    console.log(data.toString());
    res.json({
      success: false,
      err_code: -1,
      err_msg: "불러오기에 실패했습니다. 다시 시도해주세요!",
    });
  });
});

app.listen(process.env.PORT, () => {
  console.log(`listening on PORT: ${process.env.PORT}`);
});
