import { writable, type Writable, derived } from 'svelte/store';
import { localStorageStore } from '@skeletonlabs/skeleton';
import type { Chat } from '$lib/chatUtils';

export const mpAPIKey: Writable<string> = localStorageStore('mpAPIKey', '');
export const OpenAiAPIKey: Writable<string> = localStorageStore('openAiAPIKey', '');
export const OpenAiOrg: Writable<string> = localStorageStore('openAiOrg', '');
export const chats: Writable<Chat[]> = localStorageStore('chats', [
  {
    question: '',
    title: '',
    messages: [],
  }
]);
export const currentChatIndex: Writable<number> = writable(0);
export const showAlpha = writable(true);

export const keyNotSet = derived(
  [mpAPIKey, OpenAiAPIKey],
  ([mpAPIKey, OpenAiAPIKey]) => mpAPIKey === '' || OpenAiAPIKey === ''
);

export const current_chat_id = writable<string | undefined>(undefined);
