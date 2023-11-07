import { chats } from '$lib/store';
import { get } from 'svelte/store';

export interface SimulationDataItem {
  'Time[ps]': number;
  'Etot/N[eV]': number;
}
export interface Chat {
  question: string;
  title: string;
  messages: ChatMessage[];
}

export interface ChatMessage {
  role: 'assistant' | 'user';
  content: string;
  type: 'info' | 'msg' | 'structures' | 'simulation' | 'simulation_chart';
  structures?: any[];
  timestamp: Date;
  simulationData?: any[];
}

export function syncChats(): void {
  const currentChats = get(chats);
  const filteredChats = currentChats.filter((c: Chat) => c.messages.length > 0);
  chats.set(filteredChats);
}

export function clearChats(): void {
  chats.set([
    {
      question: '',
      title: '',
      messages: []
    }
  ]);
  window.location.reload();
}
