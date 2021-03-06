
<?php
include_once(dirname(__FILE__) . '/DBC.php');

	//Database connection information
	$dbinfo = array( 
		'provider' => 'sqlsrv',
		'host' => 'localhost\\SQLEXPRESS', 
		'user' => 'rmsapp',
		'password' => 'ss1RMSpw@wb02',
		'db'   => 'rms'
    );



//Open the PDO Connection
try {
    $dbconn = new DBC($dbinfo);
}
catch (Exception $ex) {
    echo '<p>Error creating database connection: ' . $ex->getMessage() . '</p>';
    echo '</html>';
    exit();
}

$result = $dbconn->query('SELECT * FROM roll ORDER BY roll_num DESC');
?>
<!-- Draft of RMS Kaiser Website -->

<!DOCTYPE html>
<html lang = "en">
<head>
	<link href = "style.css" rel="stylesheet" type="text/css" >
	
	<title>RMS Home</title>

</head>
<body>
	<header> 
	<!-- Help icon and links -->
	<div id="helpOption">
		<a href="helpPage.html">Help</a>
		<a href="helpPage.html"><img src="helpBtn.png" height="60" width="60" class = "helpBtn" alt="Help Button" /></a>
	</div>
	<!-- Main Kaiser logo and page navigation links -->
		<img src="logo.png" alt="Kaiser Aluminium Logo"/> 
		<p style="text-align: center">
		<strong>Home Roll Management Page</strong>  |  <a href="chocksMenu.php">Chocks and Bearings </a>  |  <a href="notifications.html">Notification Settings</a>
		</p>
	</header>

	<main>
		<br>
		<br>
	<!-- big table with links to roll data and lots of data
		will need to activate filtering feature
		maybe a search bar sort of thing?-->
	<div>
	<table class = "center">
	<caption><strong>General Roll Information</strong>   
	<!-- seach bar to look for any value in the roll table -->
	<input type = "text" id = "filter_input" onkeyup ="searchFunction()" placeholder = "Search" title="Type in desired table value ">
		<tr>
			<th><strong>Roll ID</strong></th>
			<th><strong>Status</strong></th> <!-- Will automatically determine red or green for not in use or in use-->
			<th><strong>Current Diameter</strong></th>
			<th><strong>Starting Diameter</strong></th>
			<th><strong>Mill</strong></th>
			<th><strong>Roll Type</strong></th>
			<th><strong>Manufacured Date</strong></th>
		</tr>
		<!-- Below are all just currently space fillers to show desired future look -->
		<tr>
			<?php
				foreach ($result as $key => $rows) {
				
			 ?>
					<tr>
						<td><?php echo '<a href="rollData.php?roll_number=' . $rows['roll_num'] . '">' . $rows['roll_num'] . '</a>';?></td>
						<td><?php echo $rows['status'];?></td>
						<td><?php echo $rows['starting_diameter'];?></td>
						<td><?php echo $rows['current_diameter'];?></td>
						<td><?php echo $rows['mill'];?></td>
						<td><?php echo $rows['roll_type'];?></td>
						<td><?php echo $rows['manufactured_date'];?></td>
					</tr>
            <?php
                }
             ?>		
	</table>
	</div>
	</main>
<script>
	//Filtering function for the search function to look through entire table for the value
	function searchFunction() {
    let tabel, filter, input, tr, td, i;
    input = document.getElementById("filter_input");
    filter = input.value.toUpperCase();
    tabel = document.getElementById("roll_table");
    tr = document.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        if (tr[i].textContent.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
			}
		}
	}
	
</script>
</body>
</html>
