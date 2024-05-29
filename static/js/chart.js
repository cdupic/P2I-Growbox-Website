const getFrenchName = (is_sensor, type) => {
    if(is_sensor){
        switch(type){
            case "temperature":
                return "Température";
            case "soil_humidity":
                return "Humidité du sol";
            case "light":
                return "Luminosité";
            case "air_humidity":
                return "Humidité de l'air";
            case "water_level":
                return "Niveau d'eau";
            case "O2":
                return "O2";
            default:
                return "Inconnu";
        }
    }else{
        switch(type){
            case "temperature":
                return "Chauffage/Climatisation";
            case "soil_humidity":
                return "Arroseur";
            case "light":
                return "Vélux";
            case "air_humidity":
                return "Humidificateur";
            case "water_level":
                return "Robinet";
            case "O2":
                return "Ouverture";
            default:
                return "Inconnu";
        }
    }

}

const getYMin = (min_val, type) => {
    if(type === 'temperature'){
        return Math.min(min_val - 5, 0);
    }
    return Math.min(min_val, 0);
}

const getYMax = (max_val, type) => {
    if(type === 'soil_humidity' || type === 'air_humidity' || type === 'O2'){
        return 100;
    }
    if(type === 'light'){
        return Math.max(5000, max_val+100);
    }
    if(type === 'temperature'){
        return Math.max(max_val + 5, 35);
    }
    if(type === 'water_level'){
        return Math.max(max_val, 35);
    }
    return max_val;
}

window.configureChart = (el_id, dates, measures, targets, gh_serial, is_sensor, type, id) => {

    let yMin = Math.min(...measures);
    let yMax = Math.max(...measures);

    dates = dates.map(date => new Date(date));

    let annotations = {}
    const target = targets[type];
    if(target !== undefined){
        annotations.line1 = {
            type: 'line',
            yMin: target,
            yMax: target,
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 2,
        }
    }

    const config = {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                data: measures,
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderColor: "rgba(178, 218, 30, 1)",
                borderWidth: 1,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    min: getYMin(yMin, type),
                    max: getYMax(yMax, type),
                    title: {
                        display: true,
                        text: getFrenchName(is_sensor, type)
                    }
                },
                x: {
                    type: 'time',
                    time: {
                        tooltipFormat: 'DD T'
                    },
                    title: {
                        display: true,
                        text: "Date"
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                annotation: {
                    annotations
                }
            }
        }
    };

    const canvas = document.getElementById(el_id);
    new Chart(canvas, config);
}
