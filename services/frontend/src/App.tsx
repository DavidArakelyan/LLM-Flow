import React from 'react';
import { Chat } from './components/Chat';

function App() {
    return (
        <div className="app">
            <header className="app-header">
                <h1>LLM Flow Chat</h1>
            </header>
            <main>
                <Chat />
            </main>
        </div>
    );
}

export default App;