<script>
	import { onMount } from "svelte";
	import SvelteTable from "svelte-table";
	let dataObject = {};
	let data = [];
	let headers = [];
	let sortedData = data;
	const tableHeaders = Object.keys(personData[0])
	// console.log(tableHeaders)
	
	let selectedHeader = "id";
	let ascendingOrder = true;
	

	onMount(async () => {
		const response = await fetch("./data");
		
		if (response.status === 200) {
      		console.log("Data Retrieved");
		} else {
      		// Otherwise check the error
      		throw new Error(response.status);
    	}

		dataObject = await response.json();
		for (var key in dataObject){
			data.push(dataObject[key]);
		}
		headers = Object.keys(dataObject[0]);
		console.log(data);
	});

	// SORT BY NUMBER
	const sortByNumber = (colHeader) => {
		sortedPersonData = sortedPersonData.sort((obj1, obj2) => {
			return ascendingOrder ? Number(obj1[colHeader]) - Number(obj2[colHeader])
			: Number(obj2[colHeader]) - Number(obj1[colHeader])
		});
		selectedHeader = colHeader;
	}
	
	// SORT BY STRINGs
	const sortByString = (colHeader) => {
		sortedPersonData = sortedPersonData.sort((obj1, obj2) => {
			if (obj1[colHeader] < obj2[colHeader]) {
					return -1;
			} else if (obj1[colHeader] > obj2[colHeader]) {
				return 1;
			}
			return 0; //string code values are equal		
		});
		if (!ascendingOrder) {
			sortedPersonData = sortedPersonData.reverse()
		}
		selectedHeader = colHeader;
	}

	const rows = data;
	const columns = headers;
	
</script> 

<main>
	<strong>General Roll Information</strong>
	<h1>Hello {headers}!</h1>
	<h2>JSON OUT: {data[0]["Roll ID"]}</h2>
	<h3>color</h3>
	
	<table id="rollTable">

		<tr>
			{#each headers as header}
				<th class:highlighted={selectedHeader === header} on:click={() => (header === "id" || header === "age" ) ? sortByNumber(header) : sortByString(header)}>
					{header.replace("_", " ")}
				{#if header === selectedHeader}	
					<span class="order-icon" on:click={() => ascendingOrder = !ascendingOrder}>
						{@html ascendingOrder ? "&#9661;" : "&#9651;"}
					</span>		
				{/if}	
			</th>	
			{:else}
				
			{/each}
			
	  	</tr>

		<tr>


		</tr>

	</table> 
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