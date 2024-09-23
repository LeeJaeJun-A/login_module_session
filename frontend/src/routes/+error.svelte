<script lang="ts">
  import { page } from "$app/stores";

  import NotFound from "$lib/components/error/NotFound.svelte";
  import Maintenance from "$lib/components/error/Maintenance.svelte";
  import ServerError from "$lib/components/error/ServerError.svelte";
  import UnknownServerError from "$lib/components/error/UnknownServerError.svelte";

  // const pages = {
  // 	400: Maintenance,
  // 	404: NotFound,
  // 	500: ServerError
  // };

  type ErrorPages = {
    [key: number]: typeof Maintenance | typeof NotFound | typeof ServerError;
  };

  const pages: ErrorPages = {
    400: Maintenance,
    404: NotFound,
    500: ServerError,
  };
  const status = +$page.status;
  const index = Object.keys(pages)
    .map((x) => +x)
    .reduce((p, c) => (p < status ? c : p));
  const component = pages[index] || UnknownServerError;
</script>

<svelte:component this={component}></svelte:component>
