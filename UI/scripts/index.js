const fs = require('fs');
const { exec } = require('child_process');
const { PythonShell } = require('python-shell');
const process = require('process');

const loginWindow = document.getElementById('loginWindow');
const mainWindow = document.getElementById('mainWindow');
const userShower = document.getElementById('userShower');
const rankShower = document.getElementById('rankShower');

const winrateShower = document.getElementById('winrateShower');
const winrateCanvas = document.getElementById('winrateCanvas');

const xhr = new XMLHttpRequest();
global.user = "";
global.score = 0;
global.opponent = "";
global.finishLogin = () => {
    userShower.innerText = cutString(user, 5) + "，登陆成功！";
    rankShower.innerText = "目前得分：" + score;
    loginWindow.style.display = "none";
    mainWindow.style.display = "block";
};

let winrateLst = []

function cutString(str, num) {
    if (str.length <= num + 1)
        return str;
    return str.substr(0, num) + "...";
}

function rateLst2Point(rateLst) {
    let pointsStr = ""
    for (let i = 0; i < rateLst.length; i++) {
        if (i != 0)
            pointsStr += " "
        pointsStr += i / (rateLst.length - 1) * 220 + "," + (135 - rateLst[i] / 100 * 135);
    }
    return pointsStr;
}

function formWinrateCurve() {
    winrateCanvas.innerHTML = "";
    let polyline = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    if (winrateLst.length == 1)
        polyline.setAttribute("points", rateLst2Point([winrateLst[0], winrateLst[0]]));
    else
        polyline.setAttribute("points", rateLst2Point(winrateLst));
    polyline.style = "fill:transparent;stroke:black;stroke-width:1"
    winrateCanvas.appendChild(polyline);
}

function getWinRate() {
    let val = "http://www.chessdb.cn/chessdb.php?action=" + "queryall" + "&board=rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
    xhr.open("POST", val, true);
    xhr.send();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let winrate = Number(xhr.responseText.split("|")[0].split(",")[4].split(":")[1]);
            if (winrate == NaN || winrate == undefined || winrate < 0 || winrate > 100) {
                winrate = 50.0;
                winrateShower.innerText = "未知";
            } else
                winrateShower.innerText = winrate + "%";
            winrateLst.push(winrate);
            formWinrateCurve();
        }
    }
}

let pymodel;

function getModels() {
    let models = fs.readdirSync('./models');
    let modelfile = models[Math.floor(Math.random() * models.length)];
    while (modelfile == "__pycache__")
        modelfile = models[Math.floor(Math.random() * models.length)];
    //opponent = modelfile.split('.')[0];
    opponent = "example"
    pymodel = new PythonShell("game.py", {
        mode: "text",
        args: [process.cwd(), opponent],
        pythonPath: "python3",
        pythonOptions: ["-u"],
        scriptPath: process.cwd() + "/UI/scripts",
    });
    pymodel.on('message', function(message) {
        jsonMessage = JSON.parse(message)
        if (jsonMessage.type == "signal") {
            if (jsonMessage.signal == "win" && jsonMessage.player == "user" || jsonMessage.signal == "lose" && jsonMessage.player == "ai")
                userwin();
            else if (jsonMessage.signal == "win" && jsonMessage.player == "ai" || jsonMessage.signal == "lose" && jsonMessage.player == "user")
                userlose();
        }
        console.log(jsonMessage);
        getWinRate();
    })
}

function userwin() {
    console.log("userwin")
}

function userlose() {
    console.log("userlose")
}

function step(index, actionx, actiony) {
    pymodel.send(index, actionx, actiony);
}

function startGame() {
    getModels();
}