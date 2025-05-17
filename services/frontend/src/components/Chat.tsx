import React, { useState } from 'react';
import { ChatMessage as ChatMessageType } from '../types/types';
import { ChatMessage } from './ChatMessage';

export const Chat: React.FC = () => {
    const [messages, setMessages] = useState<ChatMessageType[]>([]);
    const [input, setInput] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage: ChatMessageType = {
            id: Date.now().toString(),
            content: input,
            role: 'user',
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');

        // TODO: Implement API call to backend
    };

    return (
        <div className="chat-container">
            <div className="messages-container">
                {messages.map(message => (
                    <ChatMessage key={message.id} message={message} />
                ))}
            </div>
            <form onSubmit={handleSubmit} className="input-form">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};