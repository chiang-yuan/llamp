import { writable, type Writable, derived } from 'svelte/store';
import { localStorageStore } from '@skeletonlabs/skeleton';

export const mpAPIKey: Writable<string> = localStorageStore('mpAPIKey', '');
export const OpenAiAPIKey: Writable<string> = localStorageStore('openAiAPIKey', '');

export const keyNotSet = derived(
  [mpAPIKey, OpenAiAPIKey],
  ([mpAPIKey, OpenAiAPIKey]) => mpAPIKey === '' || OpenAiAPIKey === ''
);
