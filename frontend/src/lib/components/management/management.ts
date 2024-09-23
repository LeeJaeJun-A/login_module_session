import { get, writable, type Writable } from "svelte/store";
import fastapi from "$lib/fastapi";

export const options = ["UserManagement", "LockManagement"];
export const mode: Writable<string> = writable(options[0]);
export const locked_user_count: Writable<number> = writable(0);

export function getMode(): string {
  return get(mode);
}

export function setMode(value: string): void {
  mode.set(value);
}

export async function updateLockedUserCount(): Promise<void> {
  const response = await new Promise<number>((resolve, reject) => {
    fastapi("GET", "/auth/user/locked/count", {}, resolve, reject);
  });
  locked_user_count.set(response);
}