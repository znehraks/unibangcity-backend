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

app.post("/recommendation", bodyParser, (req, res) => {
  let data = "";
  console.log(req.body);
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
      console.log(dataToSend.toString("utf8"));
      data += dataToSend;
    });
    result.stderr.on("data", (dataToSend) => {
      res.json({
        success: false,
        err_code: -1,
        err_msg: "불러오기에 실패했습니다. 다시 시도해주세요!",
      });
    });
    result.on("close", (code) => {
      if (code !== 0) {
        console.log(`child process close all stdio with code ${code}`);
      }
      res.json({ success: true, data: data });
    });
  } catch (e) {
    console.log(e);
    res.json({
      success: false,
      err_code: -2,
      err_msg: "오류가 발생했습니다.",
    });
  }
});

app.post("/recommendation/add", (req, res) => {
  let sql = `INSERT INTO diy_reco_history(user_no, w_1st, w_2nd, w_3rd, w1, w2, w3, w4, w5, total_w, Q1, Q2, Q3, Q4, Q5, univ_lat, univ_lon, T_set ) values (${req.body.user_no}, ${req.body.w_1st}, ${req.body.w_2nd}, ${req.body.w_3rd}, ${req.body.w1}, ${req.body.w2}, ${req.body.w3}, ${req.body.w4}, ${req.body.w5}, ${req.body.total_w},'${req.body.Q1}', ${req.body.Q2},'${req.body.Q3}','${req.body.Q4}','${req.body.Q5}',${req.body.univ_lat},${req.body.univ_lon}, '${req.body.T_set};
  ')`;

  connection.query(sql, (err, rows) => {
    res.send(rows);
    console.log(err);
  });
});

app.post("/recommendation/add_eval", (req, res) => {
  let sql = `INSERT INTO evaluation(evaluation_category_no, univ_name, T_set, rank01_score, rank02_score, rank03_score, rank04_score, rank05_score) values (${req.body.evaluation_category_no}, '${req.body.univ_name}', '${req.body.T_set}', ${req.body.rank01_score}, ${req.body.rank02_score}, ${req.body.rank03_score}, ${req.body.rank04_score}, ${req.body.rank05_score})`;

  connection.query(sql, (err, rows) => {
    res.send(rows);
    console.log(err);
  });
});

//특정 유저 정보 불러오기
app.get("/user", (req, res) => {
  try {
    const { code } = authenticateJWT(req.headers.authorization);
    const sql = `SELECT * FROM user LEFT JOIN board ON user.user_code = board.user_code WHERE user.user_code = ${code};`;
    connection.query(sql, (err, data, fields) => {
      if (err) throw err;
      res.send(data);
    });
  } catch (e) {
    res.send({ success: false });
  }
});

//회원가입하기
app.post("/user/create", bodyParser, async (req, res) => {
  console.log(req.body);
  const hashedPassword = await bcrypt.hash(req.body.user_password, 10);
  const sql = `INSERT INTO user(user_email, user_id, user_password) VALUES('${req.body.user_email}','${req.body.user_id}','${hashedPassword}')`;
  connection.query(sql, (err, data, fields) => {
    if (err) throw err;
    res.send(data);
  });
});

//로그인하기
app.post("/user/login", bodyParser, async (req, res) => {
  const sql = `SELECT * FROM user WHERE user_id = '${req.body.user_id}'`;
  connection.query(sql, (err, data) => {
    if (err) {
      console.log(err);
      res.send({
        success: false,
        err_code: -1,
        err_msg: "예기치 못한 오류가 발생했습니다.",
      });
    }
    if (data.length === 0) {
      res.send({
        success: false,
        err_code: 1,
        err_msg: "가입되지 않은 아이디입니다.",
      });
      return;
    }
    bcrypt.compare(
      req.body.user_password,
      data[0].user_password,
      (err, compareRes) => {
        if (err) {
          console.log(err);
          res.send({
            success: false,
            err_code: -1,
            err_msg: "예기치 못한 오류가 발생했습니다.",
          });
        }
        if (compareRes) {
          const token = jwt.sign(
            { code: data[0].user_code, user_id: data[0].user_id },
            process.env.SECRET_KEY
          );
          res.send({ success: true, token });
        } else {
          res.send({
            success: false,
            err_code: 2,
            err_msg: "비밀번호가 틀립니다.",
          });
        }
      }
    );
  });
});

app.get("/user/me", (req, res) => {
  try {
    const user = authenticateJWT(req.headers.authorization);
    res.send(user);
  } catch (err) {
    console.log(err);
    res.send({ success: false });
  }
});
app.listen(process.env.PORT, () => {
  console.log(`listening on PORT: ${process.env.PORT}`);
});
