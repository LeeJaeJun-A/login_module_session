<script lang="ts">
  import { goto } from "$app/navigation";
  import fastapi from "$lib/fastapi";
  import { getRole, setRole, setUserId } from "$lib/login";
  import "izitoast/dist/css/iziToast.min.css";
  import { onDestroy, onMount } from "svelte";

  const modes = ["ems/dashboards", "rcs"];

  let user_id: string = "";
  let password: string = "";
  let mode: string = modes[0];

  async function signInClicked(event: Event) {
    event.preventDefault();

    const iziToast = await import("izitoast").then((module) => module.default);

    if (!user_id || !password) {
      iziToast.error({
        title: "Error",
        message: "All fields are required.",
      });
      return;
    }

    const params = {
      user_id: user_id,
      password: password,
    };

    try {
      const response = await new Promise<{
        message: string;
        role: string;
      }>((resolve, reject) => {
        fastapi("POST", "/auth/login", params, resolve, reject);
      });

      setUserId(user_id);
      setRole(response.role);

      if (getRole() === "admin") {
        goto("/management");
      } else {
        goto(`/home`);
      }
    } catch (error: any) {
      if (
        error.detail &&
        error.detail.includes("Invalid user_id or password")
      ) {
        iziToast.error({
          title: "Login Failed",
          message: "Invalid user_id or password. Please try again.",
        });
      } else if (error.message) {
        iziToast.error({
          title: "Error",
          message: error.message,
        });
      } else {
        iziToast.error({
          title: "Error",
          message: "An unknown error occurred. Please try again.",
        });
      }
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      event.preventDefault();
      signInClicked(new Event("submit") as SubmitEvent);
    }
  }

  onMount(() => {
    if (typeof window !== "undefined") {
      document.addEventListener("keydown", handleKeyDown);
    }
  });

  onDestroy(() => {
    if (typeof window !== "undefined") {
      document.removeEventListener("keydown", handleKeyDown);
    }
  });
</script>

<div class="w-5/12 h-full border rounded-l-3xl bg-gray-50 flex flex-col p-14">
  <form class="flex-1 flex flex-col justify-center">
    <p class="text-2xl 4xl:text-4xl font-bold mb-4 4xl:mb-12 text-gray-800">
      Log In
    </p>
    <div class="mb-3 4xl:mb-6">
      <label
        for="user_id"
        class="block text-xs 4xl:text-lg font-medium text-gray-700 mb-2"
        >ID</label
      >
      <input
        type="user_id"
        id="user_id"
        class="w-full p-2 4xl:p-3 border rounded-lg text-xs 4xl:text-base focus:outline-none focus:ring-0 focus:border-black"
        bind:value={user_id}
        required
        placeholder="Enter your user_id"
      />
    </div>
    <div class="mb-6">
      <label
        for="password"
        class="block text-xs 4xl:text-lg font-medium text-gray-700 mb-2"
        >Password</label
      >
      <input
        type="password"
        id="password"
        class="w-full p-2 4xl:p-3 border rounded-lg text-xs 4xl:text-base focus:outline-none focus:ring-0 focus:border-black"
        required
        bind:value={password}
        placeholder="Enter your password"
      />
    </div>
    <button
      type="button"
      class="w-full bg-green-500 text-white text-xs 4xl:text-base py-2 4xl:py-3 4xl:mt-6 rounded-lg hover:bg-green-700 transition duration-300 ease-in-out focus:outline-none focus:ring-0 focus:border-black"
      on:click={signInClicked}
    >
      Sign In
    </button>
  </form>
</div>
