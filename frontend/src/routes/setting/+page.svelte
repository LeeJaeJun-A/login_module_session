<script lang="ts">
  import { initializeSession } from "$lib/auth";
  import { onMount } from "svelte";
  import { getRole, mode, setMode } from "$lib/store";
  import NavBar from "$lib/components/NavBar.svelte";
  import SideBar from "$lib/components/SideBar.svelte";
  import UserManagement from "$lib/components/UserManagement.svelte";
  import LockManagement from "$lib/components/LockManagement.svelte";

  let role: string | null = null;
  
  onMount(async () => {
    await initializeSession();
    role = getRole();
    setMode("UserManagement");
  });

  $: current_mode = $mode;
</script>

<NavBar {role} />
<main class="flex flex-col bg-gray-100" style="height: 94vh">
  <div class="flex flex-1 overflow-hidden h-full">
    <SideBar/>
    <div class="flex-1 overflow-auto h-full">
      {#if current_mode === "UserManagement"}
        <UserManagement />
      {:else if current_mode === "LockManagement"}
        <LockManagement />
      {/if}
    </div>
  </div>
</main>
