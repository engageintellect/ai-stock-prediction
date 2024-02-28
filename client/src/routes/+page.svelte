<script lang="ts">
	import { goto } from '$app/navigation';

	let inputValue = '';

	function handleSubmit(event: any) {
		event.preventDefault(); // Prevent default form submission behavior
		const searchQuery = inputValue.trim();
		if (searchQuery) {
			goto(`/ticker/${encodeURIComponent(searchQuery)}`);
		}
	}
</script>

<div class="mx-auto flex w-full max-w-lg flex-col items-center justify-center">
	<div class="my-5 text-7xl">Stonk AI</div>
	<div class="font-thin">
		Labore id consectetur proident id ipsum magna consectetur ut sunt officia et non. Nostrud veniam
	</div>

	<form on:submit={handleSubmit} class="w-full">
		<label class="input input-bordered my-5 flex w-full items-center gap-2">
			<input type="text" class="w-full grow" placeholder="Search" bind:value={inputValue} />
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 16 16"
				fill="currentColor"
				class="h-4 w-4 opacity-70"
			>
				<path
					fill-rule="evenodd"
					d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
					clip-rule="evenodd"
				/>
			</svg>
		</label>
		<button type="submit" class="btn btn-primary w-full">Search</button>
	</form>
</div>
