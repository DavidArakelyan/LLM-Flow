import React from 'react';
import { ChatMessage as ChatMessageType } from '../types/types';

interface Props {
    message: ChatMessageType;
}

export const ChatMessage: React.FC<Props> = ({ message }) => {
    return (
        <div className={`chat-message ${message.role}`}>
            <div className="message-content">{message.content}</div>
            <div className="message-timestamp">
                {message.timestamp.toLocaleTimeString()}
            </div>
        </div>
    );
};