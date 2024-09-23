import { writable, type Writable, get } from "svelte/store";
import fastapi from "../../fastapi";
import { goto } from "$app/navigation";

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
      fastapi("POST", "/auth/logout", {}, resolve, reject);
    });
  } catch (error: any) {
    console.error(error); // need to change
  } finally {
    goto("/login", {replaceState:true});
  }
}

export async function checkSession(): Promise<void> {
  try{
    const response = await new Promise<{ user_id: string, role:string }>((resolve, reject) => {
      fastapi("GET", "/auth/session", {}, resolve, reject);
    });

    if(!getUserId()){
      setUserId(response.user_id);
    }

    if(!getRole()){
      setRole(response.role);
    }
  }catch{
    logout();
  }
}