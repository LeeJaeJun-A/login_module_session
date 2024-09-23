<script lang="ts">
  import Login from "$lib/components/login/Login.svelte";
</script>

<main class="flex h-screen w-screen justify-center items-center">
  <div
    class="flex shadow-lg rounded-3xl overflow-hidden"
    style="width: 60%; height:70%"
  >
    <Login />
    <div
      class="w-7/12 h-full border rounded-r-3xl flex justify-center items-center bg-white relative"
    >
      <img src="/logo.png" class="select-none" alt="Logo" />
    </div>
  </div>
</main>
