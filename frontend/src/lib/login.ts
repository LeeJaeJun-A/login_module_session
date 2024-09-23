import { writable, type Writable, get } from "svelte/store";
import fastapi from "./fastapi";

export const user_id: Writable<string> = writable("");
export const role: Writable<string> = writable("");

export function getUserId(): string {
  return get(user_id);
}

export function getRole(): string {
  return get(role);
}

export function setUserId(value: string): void {
  user_id.set(value);
}

export function setRole(value: string): void {
  role.set(value);
}

export async function logout(): Promise<void> {
  try {
    setUserId("");
    setRole("");

    await new Promise<{ message: string }>((resolve, reject) => {
      fastapi("POST", "/api/auth/login", {}, resolve, reject);
    });

    window.location.href = '/';
  } catch (error: any) {
    console.error(error); // need to change
  }
}
