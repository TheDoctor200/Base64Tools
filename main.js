// main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);

ipcMain.handle('decode', async (event, inputText) => {
    let options = {
        scriptPath: path.join(__dirname, '/backend'),
        args: [JSON.stringify({ input: inputText })]
    };
    let result = await PythonShell.run('backend.py', options);
    let output = JSON.parse(result[0]);
    return output.decoded_text || output.error;
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
