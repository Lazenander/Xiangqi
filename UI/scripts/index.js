const fs = require('fs');
const { exec } = require('child_process');
const { PythonShell } = require('python-shell');
const process = require('process');

const loginWindow = document.getElementById('loginWindow');
const mainWindow = document.getElementById('mainWindow');
const gamingWindow = document.getElementById('gamingWindow');

const userDisplayer = document.getElementById('userDisplayer');
const rankDisplayer = document.getElementById('rankDisplayer');

const winrateDisplayer = document.getElementById('winrateDisplayer');
const winrateCanvas = document.getElementById('winrateCanvas');

const opponentName = document.getElementById('opponentName');

const boardDisplayer = document.getElementById('boardDisplayer');
const actionSpaceDisplayer = document.getElementById('actionSpaceDisplayer');

const xhr = new XMLHttpRequest();

global.user = "";
global.score = 0;
global.opponent = "";
global.finishLogin = () => {
    userDisplayer.innerText = cutString(user, 5) + "，登陆成功！";
    rankDisplayer.innerText = "目前得分：" + score;
    loginWindow.style.display = "none";
    mainWindow.style.display = "block";
    gamingWindow.style.display = "none";
};

let winrateLst = [];
let userSide = "";

let selectedPiece = -1;
let actionSpaces = [];

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
    polyline.style = "fill:transparent;stroke:red;stroke-width:1"
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
                winrateDisplayer.innerText = "未知";
            } else
                winrateDisplayer.innerText = winrate + "%";
            winrateLst.push(winrate);
            formWinrateCurve();
        }
    }
}

let pymodel;

function getModels() {
    let models = fs.readdirSync('./models');
    let modelfile = models[Math.floor(Math.random() * models.length)];
    while (modelfile == "__pycache__" || modelfile == "modules")
        modelfile = models[Math.floor(Math.random() * models.length)];
    //opponent = modelfile.split('.')[0];
    opponent = "example";
    opponentName.innerText = opponent;
    userSide = Math.random() > 0.5 ? "black" : "red";
    console.log(userSide);
    pymodel = new PythonShell("game.py", {
        mode: "text",
        args: [process.cwd(), opponent, userSide],
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
        } else if (jsonMessage.type == "board") {
            renderBoard(jsonMessage.state);
            actionSpaces = jsonMessage.actionSpace;
        }
        getWinRate();
    })
}

function userwin() {
    console.log("userwin")
    clearGame();
}

function userlose() {
    console.log("userlose")
    clearGame();
}

function clearGame() {
    winrateLst = [];
    winrateCanvas.innerHTML = "";
    mainWindow.style.display = "block";
    gamingWindow.style.display = "none";
}

function step(index, actionx, actiony) {
    pymodel.send("" + index + " " + actionx + " " + actiony);
}

function startGame() {
    mainWindow.style.display = "none";
    gamingWindow.style.display = "block";
    getModels();
}

function formChess(index, x, y) {
    let piece = document.createElement("div");
    piece.classList.add("piece");
    piece.id = "piece" + index;
    piece.style.zIndex = 100;
    piece.style.left = x * 70 - 31 + "px";
    if (userSide == "black")
        piece.style.top = y * 70 - 31 + "px";
    else
        piece.style.top = 630 - y * 70 + 39 - 70 + "px";
    let p = document.createElement("p");
    if (index < 16)
        p.style.color = "red";
    else
        p.style.color = "black";
    switch (index) {
        case 0:
            p.innerText = "帥";
            break;
        case 1:
            p.innerText = "仕";
            break;
        case 2:
            p.innerText = "仕";
            break;
        case 3:
            p.innerText = "相";
            break;
        case 4:
            p.innerText = "相";
            break;
        case 5:
            p.innerText = "馬";
            break;
        case 6:
            p.innerText = "馬";
            break;
        case 7:
            p.innerText = "車";
            break;
        case 8:
            p.innerText = "車";
            break;
        case 9:
            p.innerText = "炮";
            break;
        case 10:
            p.innerText = "炮";
            break;
        case 11:
            p.innerText = "兵";
            break;
        case 12:
            p.innerText = "兵";
            break;
        case 13:
            p.innerText = "兵";
            break;
        case 14:
            p.innerText = "兵";
            break;
        case 15:
            p.innerText = "兵";
            break;
        case 16:
            p.innerText = "將";
            break;
        case 17:
            p.innerText = "士";
            break;
        case 18:
            p.innerText = "士";
            break;
        case 19:
            p.innerText = "象";
            break;
        case 20:
            p.innerText = "象";
            break;
        case 21:
            p.innerText = "馬";
            break;
        case 22:
            p.innerText = "馬";
            break;
        case 23:
            p.innerText = "車";
            break;
        case 24:
            p.innerText = "車";
            break;
        case 25:
            p.innerText = "炮";
            break;
        case 26:
            p.innerText = "炮";
            break;
        case 27:
            p.innerText = "卒";
            break;
        case 28:
            p.innerText = "卒";
            break;
        case 29:
            p.innerText = "卒";
            break;
        case 30:
            p.innerText = "卒";
            break;
        case 31:
            p.innerText = "卒";
            break;
    }
    piece.appendChild(p);
    piece.onclick = function() {
        console.log(index)
        if (userSide == "red" && index >= 16)
            return;
        if (userSide == "black" && index < 16)
            return;
        if (selectedPiece != -1)
            document.getElementById("piece" + selectedPiece).classList.remove("selectedPiece");
        if (selectedPiece == index) {
            actionSpaceDisplayer.innerText = "";
            selectedPiece = -1;
            return;
        }
        selectedPiece = index;
        console.log(actionSpaces, index)
        piece.classList.add("selectedPiece");
        actionSpaceDisplayer.innerText = "";
        if (index < 16) {
            console.log(actionSpaces[index])
            renderActionSpace(index, x, y, actionSpaces[index]);
        } else {
            console.log(actionSpaces[index - 16])
            renderActionSpace(index, x, y, actionSpaces[index - 16]);
        }
    }
    return piece;
}

function renderActionSpace(index, x, y, actionSpace) {
    console.log(actionSpace)
    for (let i = 0; i < actionSpace.length; i++) {
        let actionSpaceDiv = document.createElement("div");
        let newX, newY;
        if (userSide == "red") {
            newX = x + actionSpace[i][0];
            newY = y + actionSpace[i][1];
        } else {
            newX = x - actionSpace[i][0];
            newY = y - actionSpace[i][1];
        }
        actionSpaceDiv.style.zIndex = 101;
        actionSpaceDiv.style.left = newX * 70 - 5 + "px";
        if (userSide == "black")
            actionSpaceDiv.style.top = newY * 70 - 5 + "px";
        else
            actionSpaceDiv.style.top = 630 - newY * 70 - 5 + "px";
        actionSpaceDiv.classList.add("actionSpaceDot");
        actionSpaceDiv.id = "actionSpace|" + newX + "|" + newY;
        actionSpaceDiv.onclick = () => {
            console.log(index, actionSpace[i][0], actionSpace[i][1])
            if (index >= 16)
                step(index - 16, actionSpace[i][0], actionSpace[i][1]);
            else
                step(index, actionSpace[i][0], actionSpace[i][1]);
            selectedPiece = -1;
        }
        actionSpaceDisplayer.append(actionSpaceDiv);
    }
}

function renderBoard(board) {
    boardDisplayer.innerHTML = "";
    actionSpaceDisplayer.innerHTML = "";
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            if (board[i][j] == -1)
                continue;
            boardDisplayer.appendChild(formChess(Number(board[i][j]), i, j));
        }
    }
}