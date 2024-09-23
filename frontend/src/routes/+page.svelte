<script lang="ts">
  import { checkSession } from "$lib/components/login/login";
  import Loading from "$lib/components/loading/Loading.svelte";
  import { onMount } from "svelte";
  import RuleList from "$lib/components/rule_list/RuleList.svelte";

  let loading = true;

  onMount(async () => {
    loading = true;
    await checkSession();
    setTimeout(() => {
      loading = false;
    }, 500);
  });
</script>

{#if loading}
  <Loading />
{:else}
  <RuleList />
{/if}
