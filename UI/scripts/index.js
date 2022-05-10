const xhr = new XMLHttpRequest();

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