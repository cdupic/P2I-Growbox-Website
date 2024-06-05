const getFrenchName = (is_sensor, type) => {
    if(is_sensor){
        switch(type){
            case "temperature":
                return "Température (°C)";
            case "soil_humidity":
                return "Humidité du sol (%HR)";
            case "light":
                return "Luminosité (lx)";
            case "air_humidity":
                return "Humidité de l'air (%HR)";
            case "water_level":
                return "Niveau d'eau (mm)";
            case "O2":
                return "O2 (%)";
            default:
                return "Inconnu";
        }
    }else{
        switch(type){
            case "temperature":
                return "Chauffage/Climatisation";
            case "soil_humidity":
                return "Arrosage (s)";
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
    min_val = Math.floor(min_val)
    if(type === 'O2'){
        return Math.min(min_val, 15);
    }
    return Math.min(min_val, 0);
}

const getYMax = (max_val, type) => {
    max_val = Math.ceil(max_val)
    if(type === 'soil_humidity' || type === 'air_humidity'){
        return 100;
    }
    if(type === 'light'){
        return Math.max(5000, max_val + 100);
    }
    if(type === 'temperature'){
        return Math.max(max_val + 5, 35);
    }
    if(type === 'water_level'){
        return Math.max(max_val, 35);
    }
    if(type === 'O2'){
        return Math.max(max_val, 25);
    }
    return max_val;
}

window.configureChart = (el_id, dates, measures, targets, gh_serial, is_sensor, type, id, from_date, to_date) => {
    if(from_date === undefined){
        from_date = dates[0];
    }
    if(to_date === undefined){
        to_date = dates[dates.length - 1];
    }

    dates = dates.map((date) => newUTCDate(date));

    console.log(targets)

    const hour_Scope = Math.ceil((new Date(to_date) - new Date(from_date)) / (1000 * 60 * 60));
    let unit = 'minute'
    if(hour_Scope > 24 * 365 * 4){ // > 4 years
        unit = 'year'
    }else if(hour_Scope > 24 * 265 * 2){ // > 2 years
        unit = 'quarter'
    }else if(hour_Scope > 24 * 30 * 4){ // > 4 month
        unit = 'month'
    }else if(hour_Scope > 24 * 4){ // > 4 day
        unit = 'day'
    }else if(hour_Scope > 12){ // > 12 hours
        unit = 'hour'
    }

    let yMin = Math.min(...measures);
    let yMax = Math.max(...measures);

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
                "data": measures,
                backgroundColor: "rgba(178, 218, 30, 0.08)",
                borderColor: "rgba(178, 218, 30, 1)",
                borderWidth: 2,
                tension: 0,
                pointStyle: false,
                stepped: true,
                fill: true,
            }]
        },
        options: {
            locale: 'fr-FR',
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
                    min: newUTCDate(from_date),
                    max: newUTCDate(to_date, 0),
                    time: {
                        tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
                        unit: unit,
                        displayFormats: {
                            minute: 'HH:mm',
                            hour: "dd '-' H'h'",
                            day: 'dd LLL',
                            month: 'LLL yyyy',
                            quarter: 'LLL yyyy',
                            year: 'yyyy'
                        },
                    },
                    adapters: {
                        date: {
                            locale: 'fr',
                            zone: 'UTC+1'
                        }
                    },
                    title: {
                        display: false,
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context){
                            const date = new Date(context[0].parsed.x);
                            const formatter = new Intl.DateTimeFormat('fr-FR', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit',
                                second: '2-digit'
                            });
                            return formatter.format(date);
                        }
                    }
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

const newUTCDate = (text, shift_minutes = 0) => {
    const date = new Date(text);
    date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    if(shift_minutes !== 0) date.setMinutes(date.getMinutes() + shift_minutes);
    return date;
}
