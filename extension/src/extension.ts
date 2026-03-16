import * as path from 'path';
import { ExtensionContext,  Uri } from "vscode";
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';

export function activate(context: ExtensionContext) {
	
	const serverPath = context.asAbsolutePath(path.join('src', 'server.py'));
	{}console.log(serverPath);
	console.log('actove');

	const pythonPath = path.resolve(context.extensionPath, '..', '.venv', 'Scripts', 'python.exe')
	// const pythonPath = context.asAbsolutePath(path.join('.venv', 'Scripts', 'python.exe'));
	console.log(pythonPath);

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

	const client = new LanguageClient('myLsp', 'hover-server', serverOptions, clientOptions);
	client.start();
}

