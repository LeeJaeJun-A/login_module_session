<script lang="ts">
  import { goto } from "$app/navigation";
  import Loading from "$lib/components/loading/Loading.svelte";
  import {
    getRole,
    getUserId,
    setRole,
    setUserId,
  } from "$lib/components/login/login";
  import Login from "$lib/components/login/Login.svelte";
  import fastapi from "$lib/fastapi";
  import { onMount } from "svelte";

  let loading = true;

  onMount(async () => {
    try {
      const response = await new Promise<{ user_id: string; role: string }>(
        (resolve, reject) => {
          fastapi("GET", "/auth/session", {}, resolve, reject);
        }
      );

      if (!getUserId()) {
        setUserId(response.user_id);
      }

      if (!getRole()) {
        setRole(response.role);
      }

      if (response.role === "user") {
        goto(`/`, {replaceState:true});
      } else if (response.role === "admin") {
        goto("/management", {replaceState:true});
      }
    } catch {
      loading = false;
    }
  });
</script>

{#if loading}
  <Loading />
{:else}
  <main class="flex h-screen w-screen justify-center items-center">
    <div
      class="flex shadow-lg rounded-3xl overflow-hidden"
      style="width: 60%; height:70%"
    >
      <Login />
      <div
        class="w-7/12 h-full border rounded-r-3xl flex justify-center items-center bg-white relative text-6xl font-bold"
      >
        <!-- <img src="/logo.png" class="select-none" alt="Logo" /> -->
        RMS
      </div>
    </div>
  </main>
{/if}
