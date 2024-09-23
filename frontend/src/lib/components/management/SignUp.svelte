<script lang="ts">
  import { onMount } from "svelte";
  import { checkSession } from "$lib/components/login/login";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";

  export let onClose;

  let user_id: string = "";
  let password: string = "";
  let role: string = "user";

  const handleRole = (event: Event) => {
    const target = event.target as HTMLSelectElement;
    if (target) {
      role = target.value;
    }
  };

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    const userData = { user_id, password, role };

    try {
      await new Promise((resolve, reject) => {
        fastapi("POST", "/auth/user", userData, resolve, reject);
      });

      Swal.fire(
        "Success!",
        "The user has been created successfully.",
        "success"
      );
      onClose();
    } catch (error: any) {
      Swal.fire(
        "Error!",
        error.detail || "There was an error creating the user.",
        "error"
      );
    }
  };

  onMount(async () => {
    await checkSession();
  });
</script>

<section
  class="bg-white rounded-lg p-8 flex flex-col justify-evenly items-center w-full h-full select-none"
>
  <span class="text-xl mb-3 4xl:text-2xl">Create User</span>
  <div class="w-full">
    <form
      on:submit|preventDefault={handleSubmit}
      class="w-full flex flex-col space-y-4 4xl:space-y-8"
    >
      <div>
        <label
          for="id"
          class="block text-xs font-medium text-gray-700 4xl:text-sm">ID</label
        >
        <input
          id="id"
          type="text"
          bind:value={user_id}
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 text-sm focus:border-indigo-500 4xl:text-base"
          required
        />
      </div>
      <div>
        <label
          for="password"
          class="block text-xs font-medium text-gray-700 4xl:text-sm"
          >Password</label
        >
        <input
          id="password"
          type="password"
          bind:value={password}
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 text-sm focus:border-indigo-500 4xl:text-base"
          required
        />
      </div>
      <div>
        <label
          for="role"
          class="block text-xs font-medium text-gray-700 4xl:text-sm"
          >Role</label
        >
        <select
          id="role"
          on:change={handleRole}
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 text-sm focus:border-indigo-500 4xl:text-base"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <div class="flex pt-4 space-x-4 justify-center w-full">
        <button
          type="submit"
          class="w-1/6 px-10 py-2 flex justify-center items-center bg-blue-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 4xl:text-base 4xl:px-12"
        >
          Create
        </button>
        <button
          type="button"
          on:click={onClose}
          class="px-10 py-2 w-1/6 flex justify-center items-center bg-gray-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 4xl:text-base 4xl:px-12"
        >
          Close
        </button>
      </div>
    </form>
  </div>
</section>
