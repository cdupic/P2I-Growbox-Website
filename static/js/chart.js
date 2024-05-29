window.configureChart = (el_id, dates, measures, target, gh_serial, is_sensor, type, id) => {

    const canvas = document.getElementById(el_id);
    const lineChart = new Chart(canvas, {
        type : "line",
        data : {
            labels : dates,
            datasets : [{
                label : `Serre ${gh_serial}, mesure du capteur ${id} : ${type}`,
                data : measures,
                backgroundColor : "rgba(75, 192, 192, 0.2)",
                borderColor : "rgba(178, 218, 30, 1)",
                borderWidth : 1
            },
                {
                    label : "Valeur cible ",
                    data : target,
                    backgroundColor : "rgba(153, 102, 255, 0.2)",
                    borderColor : "rgba(153, 102, 255, 1)",
                    borderWidth : 1
                }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}
