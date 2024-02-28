<script>
	import '../app.pcss';
	import Nav from '$lib/components/Nav.svelte';
</script>

<div>
	<Nav />
	<div class="p-4 sm:p-6">
		<div class="mx-auto max-w-3xl">
			<slot />
		</div>
	</div>
</div>
