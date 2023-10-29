export interface Chat {
  question: string;
  title: string;
  messages: ChatMessage[];
}

export interface ChatMessage {
  role: 'assistant' | 'user';
  content: string;
  type: 'info' | 'msg' | 'structures' | 'simulation' | 'simulation_chart';
  structures?: [];
  timestamp: Date;
  simulationData?: [];
}

export function syncChats(chats: Chat[]): void {
  // Only sync chats that have content
  if (!chats) return;
  const chatsToSync = chats.filter((chat) => chat.messages.length > 0);
  localStorage.setItem('chats', JSON.stringify(chatsToSync));
}
