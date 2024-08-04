<script lang="ts">
  import {
    Sidebar,
    SidebarWrapper,
    SidebarItem,
    SidebarGroup,
  } from "flowbite-svelte";
  import { UserSolid } from "flowbite-svelte-icons";
  import { initializeSession } from "$lib/auth";
  import { getId, setMode } from "$lib/store";
  import { onMount } from "svelte";


  let id : string | null = null;

  async function clickUserManagement() {
    await initializeSession();
    setMode("UserManagement");
  }

  async function clickLockManagement() {
    await initializeSession();
    setMode("LockManagement");
  }
  
  onMount(async () => {
    id = getId();
  });
</script>

<section class="h-full min-w-64" style="width: 15vw">
  <Sidebar class="h-full w-full">
    <SidebarWrapper class="h-full w-full">
      <SidebarGroup>
        <h1 class="text-lg font-bold mb-4 text-center text-black 4xl:text-2xl 4xl:mb-6 4xl:mt-2">
          Welcome {id}
        </h1>
        <hr class="border-gray-600" />
        <SidebarItem label="User Management" class="4xl:text-xl" on:click={clickUserManagement}>
          <svelte:fragment slot="icon">
            <UserSolid
              class="w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900"
            />
          </svelte:fragment>
        </SidebarItem>
        <SidebarItem label="Lock Management" class="4xl:text-xl" on:click={clickLockManagement}>
          <svelte:fragment slot="icon">
            <svg
              class="w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M8 10V7a4 4 0 1 1 8 0v3h1a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h1Zm2-3a2 2 0 1 1 4 0v3h-4V7Zm2 6a1 1 0 0 1 1 1v3a1 1 0 1 1-2 0v-3a1 1 0 0 1 1-1Z"
                clip-rule="evenodd"
              />
            </svg>
          </svelte:fragment>
        </SidebarItem>
      </SidebarGroup>
    </SidebarWrapper>
  </Sidebar>
</section>
