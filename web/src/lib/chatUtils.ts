export interface Chat {
    question: string;
    title: string;
    messages: ChatMessage[];
}

export interface ChatMessage {
    role: 'assistant' | 'user';
    content: string;
    type: 'info' | 'msg';
}

export function syncChats(chats: Chat[]): void {
    // Only sync chats that have content
    const chatsToSync = chats.filter((chat) => chat.messages.length > 0);
    localStorage.setItem('chats', JSON.stringify(chatsToSync));
}