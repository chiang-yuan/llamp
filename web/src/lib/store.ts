import { writable, type Writable, derived} from 'svelte/store';

function createSyncedStore(key: string, initialValue: string): Writable<string> {
	if (typeof localStorage === 'undefined') return writable('');
    return writable(initialValue);
}

export const mpAPIKey = createSyncedStore('mpAPIKey', '');
export const OpenAiAPIKey = createSyncedStore('OpenAiAPIKey', '');
export const keyNotSet = derived(
  [mpAPIKey, OpenAiAPIKey],
  ([mpAPIKey, OpenAiAPIKey]) => mpAPIKey === '' || OpenAiAPIKey === ''
);