<script lang="ts">
  export let role;
  import { logout } from "$lib/auth";
</script>

<nav
  class="px-2 bg-primary-800 w-full flex justify-center items-center"
  style="height: 6vh;"
>
  <div class="flex justify-between items-center w-full">
    <div class="flex items-center">
      <a
        href="/home"
        class="flex justify-center items-center text-white px-3 rounded transition duration-300 ease-in-out transform hover:scale-105"
        ><img class="w-7 h-7 mr-1  4xl:w-12 4xl:h-12" src="/favicon.png" alt="logo" />
        <span
          class="self-center text-white whitespace-nowrap text-2xl font-bold  4xl:text-4xl"
          >Title</span
        ></a
      >
    </div>
    <div class="flex space-x-4 4xl:space-x-8">
      <a
        href="/one"
        class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-110 4xl:text-2xl"
        >One</a
      >
      <a
        href="/two"
        class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-110 4xl:text-2xl"
        >Two</a
      >
      <a
        href="/three"
        class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-110 4xl:text-2xl"
        >Three</a
      >
      {#if role === "admin"}
        <a
          href="/setting"
          class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-110 4xl:text-2xl"
          >Setting</a
        >
      {/if}
      <button
        type="button"
        class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-110 4xl:text-2xl"
        on:click={logout}
      >
        Logout
      </button>
    </div>
  </div>
</nav>
