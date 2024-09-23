<script lang="ts">
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
  } from "flowbite-svelte";
  import { onMount } from "svelte";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";
  import { updateLockedUserCount } from "$lib/components/management/management";
  type User = {
    user_id: string;
    role: string;
    last_failed_login: string;
  };

  let locked_users: User[] = [];

  async function unlockUser(userId: string) {
    try {
      await new Promise<void>((resolve, reject) => {
        fastapi(
          "POST",
          `/auth/user/unlock`,
          { user_id: userId },
          resolve,
          reject
        );
      });

      await updateLockedUserCount();

      locked_users = locked_users.filter((user) => user.user_id !== userId);
      Swal.fire("Unlocked!", "The user has been unlocked", "success");
    } catch {
      Swal.fire("Error!", "There was an error unlock the user", "error");
    }
  }

  async function fetchUsers() {
    try {
      locked_users = await new Promise((resolve, reject) => {
        fastapi("GET", "/auth/user/locked", {}, resolve, reject);
      });
    } catch (error) {
      let errorMessage = "An unknown error occurred";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      Swal.fire({
        icon: "error",
        title: "Error",
        text: errorMessage,
      });
    }
  }

  onMount(fetchUsers);
</script>

<section
  class="flex flex-1 flex-col w-full items-center overflow-hidden relative min-h-screen"
>
  <div class="h-full w-full p-6 flex flex-col">
    <p class="text-2xl font-bold mb-3 select-none">Lock Management</p>
    <Table shadow>
      <TableHead class="text-center text-sm select-none bg-gray-300">
        <TableHeadCell>ID</TableHeadCell>
        <TableHeadCell>Role</TableHeadCell>
        <TableHeadCell>Locked At</TableHeadCell>
        <TableHeadCell>Actions</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y select-none">
        {#each locked_users as user}
          <TableBodyRow class="text-center text-sm">
            <TableBodyCell>{user.user_id}</TableBodyCell>
            <TableBodyCell>{user.role}</TableBodyCell>
            <TableBodyCell
              >{new Date(
                user.last_failed_login
              ).toLocaleString()}</TableBodyCell
            >
            <TableBodyCell>
              <button
                class="text-white hover:bg-green-600 select-none bg-green-500 py-1 px-2 rounded-lg"
                on:click={() => unlockUser(user.user_id)}
              >
                Unlock
              </button>
            </TableBodyCell>
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
</section>
