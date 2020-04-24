<?php
    $host = 'mysql';
    $db   = 'app';
    $user = 'root';
    $pass = 'susekere';
    $charset = 'utf8';
    $dsn = "mysql:host=$host;dbname=$db;charset=$charset";
    $opt = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ];
    $pdo = new PDO($dsn, $user, $pass, $opt);

	$query = 'SELECT * FROM scores ORDER BY RAND() LIMIT 10';
	if(isset($_GET['query'])) {
	    $name = $_GET['query'];
	    $query = 'SELECT * FROM scores WHERE name LIKE \'%'.$name.'%\' ORDER BY RAND() LIMIT 10';
	}
	$data = $pdo->query($query);
?>
<head>
    <meta charset="UTF-8">
    <title>Students quite literate</title>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
</head>
<body>
<nav class="navbar navbar-dark navbar-expand bg-dark">
    <div class="container">
        <a class="navbar-brand" href="/">Students quite literate</a>
    </div>
</nav>

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-5">
            <form>
                <div class="form-group">
                    <label for="query"><h2>Запрос</h2></label>
                    <input type="text" class="form-control" name="query" id="query">
                </div>
                <button type="submit" class="btn btn-primary">Получить</button>
            </form>
        </div>
    </div>
    <?php
    foreach ($data as $row) {
        include "template.php";
    }
    ?>
</div>
</body>