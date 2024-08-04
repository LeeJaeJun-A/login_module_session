<script lang="ts">
    import { onMount } from "svelte";
    import { getId } from "$lib/store";
    import { initializeSession } from "$lib/auth";
    import { get } from "svelte/store";
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
  
      const authorizer: string | null = getId();
      const userData = { id: user_id, password, role, authorizer };
  
      try {
        await new Promise((resolve, reject) => {
          fastapi("POST", "/users", userData, resolve, reject);
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
        await initializeSession();
    });
  </script>
  
  <section
    class="bg-white shadow-md rounded-lg p-8 flex flex-col justify-center items-center w-full max-w-md mx-auto mt-8"
  >
    <div class="w-full">
      <form
        on:submit|preventDefault={handleSubmit}
        class="flex flex-col space-y-4"
      >
        <div>
          <label for="id" class="block text-sm font-medium text-gray-700"
            >ID</label
          >
          <input
            id="id"
            type="text"
            bind:value={user_id}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700"
            >Password</label
          >
          <input
            id="password"
            type="password"
            bind:value={password}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label for="role" class="block text-sm font-medium text-gray-700"
            >Role</label
          >
          <select
            id="role"
            on:change={handleRole}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div class="mt-6 flex space-x-4 justify-center w-full">
          <button
            type="submit"
            class="px-4 py-2 w-1/6 flex justify-center items-center bg-blue-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Create
          </button>
          <button
            type="button"
            on:click={onClose}
            class="px-4 py-2 w-1/6 flex justify-center items-center bg-gray-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Close
          </button>
        </div>
      </form>
    </div>
  </section>
  