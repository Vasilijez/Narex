import { CloseAction, ErrorAction, LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function activate(context: vscode.ExtensionContext) {
	
	// Get Python path from the environment by
	// leveraging VSCode, Microsoft, Python extension context awareness.
	const pythonExt = vscode.extensions.getExtension('ms-python.python');
    if (!pythonExt) {
        const msg = "Please install the Python extension on VSCode marketplace.";
        suggestSolution(msg);
        return;
    }
    await pythonExt.activate();
    const api = pythonExt.exports;

    const uri = vscode.workspace.workspaceFolders?.[0].uri;
    const env = await api.environments.getActiveEnvironmentPath(uri);
    const pythonPath = env.path;

    vscode.window.showInformationMessage(`Selected Python: ${pythonPath}`);

    if (!pythonPath || !fs.existsSync(pythonPath)) {
        const msg = "No Python interpreter selected. Please select correct Python in VSCode.";
        suggestSolution(msg);
        return;
    }

    const serverPath = context.asAbsolutePath(path.join('src', 'server.py'));

    if (!fs.existsSync(serverPath)) {
        const msg = "LSP script (server.py) is missing from the extension folder.";
        suggestSolution(msg);
        return;
    }

    // Check whether all Python dependencies exist
    try {
        const { execSync } = require('child_process');
        execSync(`"${pythonPath}" "${serverPath}"`, { timeout: 40000 });
    } catch (e) {
        const msg = "Python dependencies are missing. Install them and select correct Python in VSCode.";
        suggestSolution(msg);
        return;
    }

    const serverOptions: ServerOptions = {
        command: pythonPath,
        args: [serverPath],
    };

	const clientOptions: LanguageClientOptions = {
		documentSelector: [{
			scheme: 'file',
			language: 'narex_dsl'
		}],
        errorHandler: {
            error: () => ({ action: ErrorAction.Shutdown }),
            closed: () => ({ action: CloseAction.DoNotRestart })
        }
	};
	
    const client = new LanguageClient('myLsp', 'Narex LSP', serverOptions, clientOptions);
    try {
        await client.start();
    } catch (error) {
        suggestSolution(error);
    }
}

export async function suggestSolution(error: unknown) {
    let detail: string;

    if (typeof error === 'string') {
        detail = error;
    } else if (error instanceof Error) {
        detail = error.message;
    } else {
        detail = "An unexpected error occurred";
    }

    const message = `Narex Extension Error: ${detail}`;
    const action = "View Setup Instructions";

    vscode.window.showErrorMessage(message, action).then(selection => {
        if (selection === action) {
            vscode.env.openExternal(vscode.Uri.parse('https://github.com/Vasilijez/Narex#getting-started'));
        }
    });
}