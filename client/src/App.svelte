<script>
	import { onMount } from "svelte";
	import { each } from "svelte/internal";

	let dataObject = {};
	let displayData = [{"Loading...":"Loading..."}];
	let headers = ["Loading..."];
	let currentDate = new Date();

	onMount(async () => {
		const response = await fetch("./data");
		let data = [];
		
		if (response.status === 200) {
      		console.log("Data Retrieved");
			dataObject = await response.json();
			for (var key in dataObject){
				data.push(dataObject[key]);
			}
			headers = Object.keys(dataObject[0]).sort();
			displayData = data;
		} else {
      		// Otherwise check the error
			console.log("Error Retrieving Data");
      		throw new Error(response.status);
    	}
	});

	console.log(currentDate);
	
</script> 

<main>
	<strong>General Roll Information</strong>
	
	<table class = "center" style="width:60%">
		<thead>
			<tr>
				{#each headers as header}
					<th> { header } </th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each displayData as roll}
				<tr>
					{#each headers as header}
						<td> { roll[header] } </td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table> 
</main>

<style>
	main {
		text-align: center;
		max-width: 240px;
		margin: 0 auto;
	}

	table, th, td {
 	 border:1px solid black;
 	 margin-left: auto; 
 	 margin-right: auto;
	}

	.btn-link {
    border: none;
    outline: none;
    background: none;
    cursor: pointer;
    color: #0000EE;
    padding: 0;
    text-decoration: underline;
    font-family: inherit;
    font-size: inherit;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>