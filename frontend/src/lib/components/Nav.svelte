<script lang="ts">
    import { logout } from "$lib/components/login/login";
</script>

<nav class="bg-main p-4 select-none">
  <div class="flex justify-between items-center w-full">
    <div class="flex items-center space-x-4">
      <a href="/" class="flex items-center">
        <span
          class="self-center text-white ml-1 whitespace-nowrap text-2xl font-bold"
          >RMS</span
        >
      </a>
    </div>
    <div class="flex space-x-4">
        <a
          href="/"
          class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-105 hover:bg-indigo-900"
          >Rules</a
        >
        <button
          on:click={logout}
          class="text-white px-3 py-2 rounded transition duration-300 ease-in-out transform hover:scale-105 hover:bg-indigo-900"
          >Logout</button
        >
    </div>
  </div>
</nav>