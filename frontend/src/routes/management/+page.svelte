<script lang="ts">
  import {
    checkSession,
    getRole,
    getUserId,
    logout,
  } from "$lib/components/login/login";
  import { mode, options } from "$lib/components/management/management";
  import { onMount } from "svelte";
  import Loading from "$lib/components/loading/Loading.svelte";
  import UserManagement from "$lib/components/management/UserManagement.svelte";
  import LockManagement from "$lib/components/management/LockManagement.svelte";
  import SideBar from "$lib/components/management/SideBar.svelte";

  let loading = true;
  let userid: string = "";

  onMount(async () => {
    await checkSession();
    if (getRole() != "admin") {
      logout();
    } else {
      userid = getUserId();
      setTimeout(() => {
        loading = false;
      }, 500);
    }
  });
</script>

{#if loading}
  <Loading />
{:else}
  <div class="min-w-screen min-h-screen flex flex-col">
    <div class="flex flex-1">
      <div class="w-64">
        <SideBar {userid} />
      </div>
      <div class="flex-1">
        {#if $mode === options[0]}
          <UserManagement {userid} />
        {:else if $mode === options[1]}
          <LockManagement />
        {/if}
      </div>
    </div>
  </div>
{/if}
