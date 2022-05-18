const loginWindow = document.getElementById('loginWindow');
const mainWindow = document.getElementById('mainWindow');
const userShower = document.getElementById('userShower');

const xhr = new XMLHttpRequest();
global.user = "";
global.finishLogin = () => {
    console.log(user);
    userShower.innerText = cutString(user, 6) + "，";
    loginWindow.style.display = "none";
    mainWindow.style.display = "block";
};

function cutString(str, num) {
    if (str.length <= num + 1)
        return str;
    return str.substr(0, num) + "...";
}

function getWinRate() {
    let val = "http://www.chessdb.cn/chessdb.php?action=" + "queryall" + "&board=rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
    xhr.open("POST", val, true);
    xhr.send();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText)
        }
    }
}