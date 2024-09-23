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
  import { writable } from "svelte/store";
  import fastapi from "$lib/fastapi";
  import SignUp from "$lib/components/management/SignUp.svelte";

  export let userid: string = "";

  type User = {
    user_id: string;
    role: string;
    created_at: string;
  };

  let users: User[] = [];
  let searchQuery: string = "";
  let filterRole: string = "all";
  let showCreateUser = writable(false);

  function closeModal() {
    showCreateUser.set(false);
    fetchUsers();
  }

  const handleSearch = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target) {
      searchQuery = target.value;
    }
  };

  const handleFilterRole = (event: Event) => {
    const target = event.target as HTMLSelectElement;
    if (target) {
      filterRole = target.value;
    }
  };

  async function handleDeleteUser(userId: string) {
    const result = await Swal.fire({
      title: "Are you sure?",
      text: "This action is irreversible!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes",
      cancelButtonText: "No",
    });

    if (userId === userid) {
      Swal.fire("Error!", "You can't delete yourself.", "error");
      return;
    }

    if (result.isConfirmed) {
      try {
        await deleteUser(userId);
        users = users.filter((user) => user.user_id !== userId);
        Swal.fire("Deleted!", "The user has been deleted.", "success");
      } catch (error: any) {
        if (error.detail === "Unable to delete root administrator account.") {
          Swal.fire("Error!", `${error.detail}`, "error");
        } else {
          Swal.fire("Error!", "There was an error deleting the user.", "error");
        }
      }
    }
  }

  async function deleteUser(userId: string) {
    return new Promise<void>((resolve, reject) => {
      fastapi(
        "DELETE",
        `/auth/user`,
        { user_id: userId },
        resolve,
        reject
      );
    });
  }

  async function fetchUsers() {
    try {
      users = await new Promise((resolve, reject) => {
        fastapi("GET", "/auth/user", {}, resolve, reject);
      });

      console.log(users);
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

  $: filteredUsers = users.filter((user) => {
    const matchesQuery = user.user_id
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesRole = filterRole === "all" || user.role === filterRole;
    return matchesQuery && matchesRole;
  });
</script>

<section
  class="flex flex-1 flex-col w-full items-center overflow-hidden relative min-h-screen"
>
  <div class="h-full w-full p-6 flex flex-col">
    <p class="text-2xl font-bold mb-3 select-none">User Management</p>
    <div class="flex justify-between items-center w-full h-12 mb-2 select-none">
      <div class="flex items-center w-full h-full space-x-2">
        <div class="relative w-96">
          <div
            class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none"
          >
            <svg
              class="w-4 h-4 text-gray-500"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 20"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
              />
            </svg>
          </div>
          <input
            type="text"
            id="table-search"
            on:input={handleSearch}
            class="block ps-10 text-sm h-full w-full text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-1 focus:ring-black focus:border-black"
            placeholder="Search by ID"
          />
        </div>
        <select
          on:change={handleFilterRole}
          class="text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 h-9 focus:outline-none focus:ring-1 focus:ring-black focus:border-black"
        >
          <option value="all">All Roles</option>
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <div class="flex items-center h-full justify-center p-2">
        <button
          on:click={() => {
            $showCreateUser = true;
          }}
          class="px-2 py-1.5 4xl:px-3"
        >
          <svg
            class="w-6 h-6 text-gray-800 4xl:w-8 4xl:h-8"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              fill-rule="evenodd"
              d="M9 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H7Zm8-1a1 1 0 0 1 1-1h1v-1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0v-1h-1a1 1 0 0 1-1-1Z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>
    <Table shadow>
      <TableHead class="text-center text-sm select-none bg-gray-300">
        <TableHeadCell>ID</TableHeadCell>
        <TableHeadCell>Role</TableHeadCell>
        <TableHeadCell>Creation</TableHeadCell>
        <TableHeadCell>Actions</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y select-none">
        {#each filteredUsers as user}
          <TableBodyRow class="text-center text-sm">
            <TableBodyCell>{user.user_id}</TableBodyCell>
            <TableBodyCell>{user.role}</TableBodyCell>
            <TableBodyCell
              >{new Date(user.created_at).toLocaleString()}</TableBodyCell
            >
            <TableBodyCell>
              <button
                class="text-white hover:bg-red-600 select-none bg-red-500 py-1 px-2 rounded-lg"
                on:click={() => handleDeleteUser(user.user_id)}
              >
                Delete
              </button>
            </TableBodyCell>
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
  {#if $showCreateUser}
    <div
      class="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-20"
    >
      <div
        class="min-h-96 overflow-auto bg-white rounded-lg shadow-lg"
        style="width: 33%; max-width:600px; height: 40%"
      >
        <SignUp onClose={closeModal} />
      </div>
    </div>
  {/if}
</section>
