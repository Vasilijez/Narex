import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';
import * as vscode from 'vscode';
import * as path from 'path';

export async function activate(context: vscode.ExtensionContext) {
	
	// Get Python path from the environment by
	// leveraging Python VSCode extension context awareness.
	const pythonExt = vscode.extensions.getExtension('ms-python.python');
    if (!pythonExt) {
        vscode.window.showErrorMessage("Please install the Python extension.");
        return;
    }
    await pythonExt.activate();
    const api: any = pythonExt.exports;

    const pythonPath = api.settings.getExecutionDetails().execCommand[0];

    const serverPath = context.asAbsolutePath(path.join('src', 'server.py'));

	console.log("python path is ", pythonPath);
	console.log("server path is ", serverPath);

    const serverOptions: ServerOptions = {
        command: pythonPath,
        args: [serverPath],
    };

	const clientOptions: LanguageClientOptions = {
		documentSelector: [{
			scheme: 'file',
			language: 'narex_dsl'
		}]
	};
	
    const client = new LanguageClient('myLsp', 'Narex LSP', serverOptions, clientOptions);
    await client.start();
}
