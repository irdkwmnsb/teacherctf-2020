<!--START-->
    <div class="row justify-content-center pt-5">
        <div class="col">
            <span class="badge badge-secondary"><?php echo $row['id'] ?></span>
            <h3><?php echo $row['name'] ?></h3>
            <p class="text-muted"><?php echo $row['borough'] ?>, <?php echo $row['building_code'] ?>, <?php echo $row['address'] ?>, <?php echo $row['city'] ?>, <?php echo $row['zip'] ?>, <?php echo $row['state'] ?> <?php echo $row['phone'] ?></p>
        </div>
    </div>
    <div class="row">
        <div class="col-auto">
            <iframe
                    height="250"
                    frameborder="0" style="border:0"
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyCm16-AtPNows2kM4ZVKqq1auysVuXGHXE&q=<?php echo $row['lat'] ?>,<?php echo $row['lng'] ?>"
                    allowfullscreen>
            </iframe>
        </div>
        <?php if($row['student_enrollment']!=0) {?>
        <div class="col">
            <p class="h5">Всего <?php echo $row['student_enrollment'] ?> учеников</p>
            <canvas height="150" id="stud_<?php echo $row['id'] ?>"></canvas>
            <script>
                $(function () {
                    let config = {
                        type: 'pie',
                        data: {
                            datasets: [{
                                data: [<?php echo $row['percent_white'] ?>, <?php echo $row['percent_black'] ?>, <?php echo $row['percent_hisp'] ?>, <?php echo $row['percent_asian'] ?>],
                                backgroundColor: ["#ddd", "#fd7e14", "#dc3545", "#28a745",],
                            }], labels: ['Белые', 'Афорамериканцы', 'Латиноамериканец', 'Азиаты']
                        },
                        responsive: true,
                        maintainAspectRatio: false
                    };
                    let ctx = document.getElementById('stud_<?php echo $row['id']?>').getContext('2d');
                    let asd = new Chart(ctx, config);
                });
            </script>
        </div>
        <?php } else { ?>
        <div class="col">
            <h5 class="py-5 text-center">Информация отсутствует</h5>
        </div>
        <?php }?>
        <?php if($row['tested_percent']!=0) {?>
        <div class="col">
            <p><?php echo $row['tested_percent']?>% сдавали SAT<br>
                <span class="h5">Экзамен длился с <?php echo $row['start_time']?> до <?php echo $row['end_time']?></span>
            </p>
            <canvas height="130" id="res_<?php echo $row['id']?>"></canvas>
            <script>
                $(function () {
                    let config = {
                        type: 'bar',
                        data: {
                            datasets: [{
                                data: [<?php echo $row['avg_math']?>, <?php echo $row['avg_reading']?>, <?php echo $row['avg_writing']?>],
                                backgroundColor: ["#007bff", "#007bff", "#007bff"],
                            }], labels: ['Математика', 'Чтение', 'Письмо']
                        },
                        options: {
                            legend: {display: false},
                            scales: {yAxes: [{ticks: {suggestedMin: 200, suggestedMax: 800}}]}
                        },
                        responsive: true,
                        maintainAspectRatio: false
                    };
                    let ctx = document.getElementById('res_<?php echo $row['id']?>').getContext('2d');
                    let efg = new Chart(ctx, config);
                });
            </script>
        </div>
        <?php } else { ?>
        <div class="col">
            <h5 class="py-5 text-center">Информация отсутствует</h5>
        </div>
        <?php }?>
    </div>
    <!--END-->