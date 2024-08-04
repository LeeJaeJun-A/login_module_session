<script lang="ts">
  import { type Writable, writable } from "svelte/store";
  import { EyeOutline, EyeSlashOutline } from "flowbite-svelte-icons";
  import { goto } from "$app/navigation";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";

  let id: Writable<string> = writable("");
  let password: string = "";
  let showPassword: boolean = false;

  async function handleLogin(event: Event) {
    event.preventDefault();
    if ($id && password) {
      const params = { id: $id, password: password };
      fastapi(
        "POST",
        "/token",
        params,
        (data) => {
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);

          Swal.fire({
            icon: "success",
            title: "Login Successful",
            timer: 1000,
            showConfirmButton: false,
          }).then(() => {
            goto("/home");
          });
        },
        (error) => {
          if (error.detail === "User not found.") {
            Swal.fire({
              icon: "error",
              title: "Login Failed",
              text: `${error.detail} Please check your ID.`,
            });
            return;
          }

          if (error.remaining_attempts === 0) {
            if (error.detail === "Incorrect ID or password") {
              Swal.fire({
                icon: "error",
                title: "Login Failed",
                text: `${error.detail}. This account is locked.`,
              });
              return;
            }
            Swal.fire({
              icon: "error",
              title: "Login Failed",
              text: `${error.detail}`,
            });
            return;
          }

          Swal.fire({
            icon: "error",
            title: "Login Failed",
            text: `${error.detail} (Remaining attempts: ${error.remaining_attempts})`,
          });
        }
      );
    }
  }

  function togglePasswordVisibility() {
    showPassword = !showPassword;
  }

  function handlePassword(event: Event) {
    const target = event.target as HTMLInputElement;
    password = target?.value || "";
  }
</script>

<div class="w-full h-full flex flex-col items-center justify-center">
  <div class="min-h-80 w-1/3 h-1/2 bg-white rounded-lg shadow">
    <div
      class="flex flex-col justify-center items-center p-8 h-full w-full 4xl:p-12"
    >
      <div class="flex justify-center items-center flex-row w-full h-1/6">
        <img
          class="w-8 h-8 mr-2 4xl:w-12 4xl:h-12 4xl:mr-3"
          src="/favicon.png"
          alt="logo"
        />
        <h1
          class="text-2xl font-bold leading-tight tracking-tight text-gray-900 4xl:text-5xl"
        >
          Title
        </h1>
      </div>
      <form
        class="space-y-4 w-full h-5/6 4xl:space-y-8 flex flex-col justify-center"
        action="#"
        on:submit|preventDefault={handleLogin}
      >
        <div>
          <label
            for="id"
            class="block mb-2 text-sm font-medium text-gray-900 4xl:text-2xl 4xl:mb-4"
            >ID</label
          >
          <input
            type="text"
            name="id"
            id="id"
            bind:value={$id}
            class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 4xl:text-2xl 4xl:p-4 4xl:mb-4"
            placeholder="Enter your ID"
            autocomplete="username"
            required
          />
        </div>
        <div>
          <label
            for="password"
            class="block mb-2 text-sm font-medium text-gray-900 4xl:text-2xl 4xl:mb-4"
            >Password</label
          >
          <div class="relative">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              id="password"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 4xl:text-2xl 4xl:p-4 4xl:mb-8"
              required
              autocomplete="current-password"
              on:input={handlePassword}
            />
            <button
              type="button"
              class="absolute inset-y-0 right-3 flex items-center text-sm 4xl:text-xl"
              on:click={togglePasswordVisibility}
            >
              {#if showPassword}
                <EyeOutline
                  class="h-5 w-5 text-gray-500 4xl:h-8 4xl:w-8"
                  aria-hidden="true"
                />
              {:else}
                <EyeSlashOutline
                  class="h-5 w-5 text-gray-500  4xl:h-8 4xl:w-8"
                  aria-hidden="true"
                />
              {/if}
            </button>
          </div>
        </div>
        <button
          type="submit"
          class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center 4xl:text-2xl 4xl:px-8 4xl:py-4"
          >Sign in</button
        >
      </form>
    </div>
  </div>
</div>
