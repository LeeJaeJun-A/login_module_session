<script lang="ts">
  import { initializeSession } from "$lib/auth";
  import { onMount } from "svelte";
  import { getRole } from "$lib/store";
  import NavBar from "$lib/components/NavBar.svelte";

  let role: string | null = null;

  onMount(async () => {
    await initializeSession();
    role = getRole();
  });
</script>

<NavBar {role} />
<main class="bg-gray-100" style="height: 94vh">
  <h1>This is Two</h1>
</main>
