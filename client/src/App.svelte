<script>
	import SvelteTable from "svelte-table";
	export let name;
  	const rows = [
    	
  	];
  	const columns = [

	];
</script>

<main>
	<strong>General Roll Information</strong>
	<h1>Hello {name}!</h1>
	<h2>Svelte Stuff</h2>
	<h3>color</h3>
	<SvelteTable columns="{columns}" rows="{rows}"></SvelteTable>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #FF7F7F;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	h2 {
		color: #90EE90;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	h3 {
		color: #FFFFE0;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>