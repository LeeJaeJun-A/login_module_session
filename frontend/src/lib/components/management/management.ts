import { get, writable, type Writable } from "svelte/store";
import { role } from "../login/login";

export const options = ["UserManagement", "LockManagement"];
export const mode: Writable<string> = writable(options[0]);

export function getMode(): string {
  return get(mode);
}

export function setMode(value: string): void {
  console.log(value);
  mode.set(value);
}
