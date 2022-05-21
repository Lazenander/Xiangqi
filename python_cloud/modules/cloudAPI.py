import requests

def queryall(fen):
    url = "http://www.chessdb.cn/chessdb.php?action=queryall&board=" + fen
    retstr = requests.post(url).text
    if retstr == "invalid board" or retstr == "unknown" or retstr == "checkmate" or retstr == "stalemate":
        return retstr
    retstr = retstr.split('\x00')[0]
    movestrs = retstr.split('|')
    moves = {}
    for movestr in movestrs:
        newmove = {
            "move": "",
            "score": 0,
            "rank": 0,
            "note": "",
            "winrate": 0.0,
        }
        tmpstr = movestr.split(',')
        newmove["move"] = tmpstr[0].split(':')[1]
        newmove["score"] = int(tmpstr[1].split(':')[1])
        newmove["rank"] = int(tmpstr[2].split(':')[1])
        newmove["note"] = tmpstr[3].split(':')[1]
        newmove["winrate"] = float(tmpstr[4].split(':')[1])
        moves[newmove["move"]] = newmove
    return moves

def queryrule(fen, pastmoves):
    paststr = ""
    for i in range(len(pastmoves)):
        if i > 0:
            paststr += "|"
        paststr += pastmoves[len(pastmoves) - i - 1]
    url = "http://www.chessdb.cn/chessdb.php?action=queryrule&board=" + fen + "&movelist=" + paststr
    retstr = requests.post(url).text.split('\x00')[0]
    if retstr == "invalid board" or retstr == "invalid movelist" or retstr == "checkmate" or retstr == "stalemate":
        return retstr
    movestrs = retstr.split('|')
    moves = {}
    for movestr in movestrs:
        newmove = {
            "move": "",
            "rule": ""
        }
        tmpstr = movestr.split(',')
        newmove["move"] = tmpstr[0].split(':')[1]
        newmove["rule"] = tmpstr[1].split(':')[1]
        moves[newmove["move"]] = newmove
    return moves