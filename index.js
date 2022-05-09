const { app, BrowserWindow } = require('electron')
const path = require('path')

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 800,
        minWidth: 800,
        minHeight: 800,
        maxWidth: 800,
        maxHeight: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
    })

    win.loadFile('./UI/html/index.html')
    win.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow()
        }
    })
})

app.on('window-all-closed', () => {
    app.quit();
})