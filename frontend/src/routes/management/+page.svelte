<script lang="ts">
  import { checkSession, getRole } from "$lib/login";
  import { onMount } from "svelte";

  onMount(async ()=>{
    await checkSession();
    if(getRole() != "admin"){
        window.location.href = '/';
    }
    
  });
</script>

<main>
    admin page
</main>