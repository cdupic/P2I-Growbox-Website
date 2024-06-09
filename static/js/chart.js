const DateTime = luxon.DateTime;
const tz_offset = DateTime.local().offset;

function correctTimezoneForField(field, zone){
    if(field === null) return;

    let date = field.getAttribute('data-value')
    field.value = DateTime.fromSQL(date, {zone: 'utc'}).setZone(zone).toISODate();
}

document.addEventListener('DOMContentLoaded', function(){
    correctTimezoneForField(document.getElementById('from_date'), 'local')
    correctTimezoneForField(document.getElementById('to_date'), 'local')
})

const getUnit = (is_sensor, type) => {
    if(is_sensor){
        switch(type){
            case "temperature":
                return "°C";
            case "soil_humidity":
                return "%HR";
            case "light":
                return "lx";
            case "air_humidity":
                return "%HR";
            case "water_level":
                return "mm";
            case "O2":
                return "%";
            default:
                return "";
        }
    }else{
        switch(type){
            case "temperature":
                return "°C";
            case "soil_humidity":
                return "s";
            case "light":
                return "lx";
            case "air_humidity":
                return "%HR";
            case "water_level":
                return "mm";
            case "O2":
                return "%";
            default:
                return "";
        }
    }
}

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

window.configureChart = (el_id, dates, measures, targets, gh_serial, is_sensor, type, id, from_date, to_date,
                         data_analysed_O2_night=null, data_analysed_O2_day=null) => {
    console.log("Configuring chart from", from_date, "to", to_date, "with", dates.length, "points")


    if(from_date === undefined){
        from_date = DateTime.fromHTTP(dates[0], {zone: 'utc'})
    }else{
        // from_date = DateTime.fromSQL(from_date, {zone: 'utc'}).minus({minutes: tz_offset}).toHTTP()
        from_date = DateTime.fromSQL(from_date, {zone: 'utc'});
    }
    if(to_date === undefined){
        to_date = DateTime.fromHTTP(dates[dates.length - 1], {zone: 'utc'});
    }else{
        if(to_date.endsWith('23:59:59+00:00')){
            // to_date = DateTime.fromSQL(to_date, {zone: 'utc'}).minus({minutes: tz_offset}).toHTTP();
            to_date = DateTime.fromSQL(to_date, {zone: 'utc'});
        }else{
            console.log("Correcting date", to_date, "to", DateTime.fromSQL(to_date, {zone: 'utc'}))
            to_date = DateTime.fromSQL(to_date, {zone: 'utc'});
        }
    }
    console.log("Corrected dates. New dates are from", from_date, "to", to_date)

    const hour_scope = Math.ceil(Math.abs(from_date.ts - to_date.ts) / 1000 / 60 / 60);
    let unit = 'minute';
    if(hour_scope > 24 * 365 * 4){ // > 4 years
        unit = 'year'
    }else if(hour_scope > 24 * 265 * 2){ // > 2 years
        unit = 'quarter'
    }else if(hour_scope > 24 * 30 * 4){ // > 4 month
        unit = 'month'
    }else if(hour_scope > 24 * 4){ // > 4 day
        unit = 'day'
    }else if(hour_scope > 12){ // > 12 hours
        unit = 'hour'
    }

    console.log("Unit is", unit, "hour scope is", from_date.x, "=", hour_scope, "hours")

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

    function getAnnotation(date, min, avg, max, label){
        return {
            type: 'box',
            xMin: date,
            xMax: date,
            yMin: min,
            yMax: max,
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            borderWidth: 1,
            borderColor: 'rgb(255, 99, 132)',
            label: {
                enabled: true,
                content: label,
                position: 'top'
            }
        }
    }
    if(!data_analysed_O2_night){
        data_analysed_O2_night = {
            dates: []
        }
    }
    if(!data_analysed_O2_day){
        data_analysed_O2_day = {
            dates: []
        }
    }

    const config = {
        type: "line",
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Minimum de jour',
                    data: data_analysed_O2_day.dates.map((date, index) =>
                        ({x: date, y: data_analysed_O2_day.min_values[index]})),
                    borderColor: '#00ade3',
                    backgroundColor: '#00ade3',
                    pointStyle: 'line',
                    pointRadius: 10,
                    borderWidth: 2,
                    hoverRadius: 10,
                    hoverBorderWidth: 3,
                    showLine: false,
                    type: 'scatter'
                }, {
                    label: 'Moyenne de jour',
                    data: data_analysed_O2_day.dates.map((date, index) =>
                        ({x: date, y: data_analysed_O2_day.avg_values[index]})),
                    borderColor: '#e38100',
                    backgroundColor: '#e38100',
                    pointStyle: 'line',
                    pointRadius: 10,
                    borderWidth: 2,
                    hoverRadius: 10,
                    hoverBorderWidth: 3,
                    showLine: false,
                    type: 'scatter'
                }, {
                    label: 'Maximum de jour',
                    data: data_analysed_O2_day.dates.map((date, index) =>
                        ({x: date, y: data_analysed_O2_day.max_values[index]})),
                    borderColor: '#e30000',
                    backgroundColor: '#e30000',
                    pointStyle: 'line',
                    pointRadius: 10,
                    borderWidth: 2,
                    hoverRadius: 10,
                    hoverBorderWidth: 3,
                    showLine: false,
                    type: 'scatter'
                },
                {
                    label: 'Minimum de nuit',
                    data: data_analysed_O2_night.dates.map((date, index) =>
                        ({x: date, y: data_analysed_O2_night.min_values[index]})),
                    borderColor: '#00ade3',
                    backgroundColor: '#00ade3',
                    pointStyle: 'line',
                    pointRadius: 10,
                    borderWidth: 2,
                    hoverRadius: 10,
                    hoverBorderWidth: 3,
                    showLine: false,
                    type: 'scatter'
                }, {
                    label: 'Moyenne de nuit',
                    data: data_analysed_O2_night.dates.map((date, index) =>
                        ({x: date, y: data_analysed_O2_night.avg_values[index]})),
                    borderColor: '#e38100',
                    backgroundColor: '#e38100',
                    pointStyle: 'line',
                    pointRadius: 10,
                    borderWidth: 2,
                    hoverRadius: 10,
                    hoverBorderWidth: 3,
                    showLine: false,
                    type: 'scatter'
                }, {
                    label: 'Maximum de nuit',
                    data: data_analysed_O2_night.dates.map((date, index) =>
                        ({x: date, y: data_analysed_O2_night.max_values[index]})),
                    borderColor: '#e30000',
                    backgroundColor: '#e30000',
                    pointStyle: 'line',
                    pointRadius: 10,
                    borderWidth: 2,
                    hoverRadius: 10,
                    hoverBorderWidth: 3,
                    showLine: false,
                    type: 'scatter'
                },
                {
                    label: '',
                    "data": measures,
                    backgroundColor: "rgba(178, 218, 30, 0.08)",
                    borderColor: "rgba(178, 218, 30, 1)",
                    borderWidth: 2,
                    tension: 0,
                    pointStyle: false,
                    stepped: false,
                    fill: true,
                }
            ]
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
                    min: from_date.toHTTP(),
                    max: to_date.toHTTP(),
                    time: {
                        tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
                        unit: unit,
                        displayFormats: {
                            minute: 'HH:mm',
                            hour: "dd/MM HH'h'",
                            day: 'dd LLL',
                            month: 'LLL yyyy',
                            quarter: 'LLL yyyy',
                            year: 'yyyy'
                        },
                        parser: function(datetext){
                            return DateTime.fromHTTP(datetext, {zone: 'utc'});
                        }
                    },
                    adapters: {
                        date: {
                            locale: 'fr'
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
                        },
                        label: function(context){
                            console.log(context)
                            if(context.dataset.label){
                                return context.dataset.label + ' : ' + context.raw.y + getUnit(is_sensor, type);
                            }else{
                                return context.formattedValue + getUnit(is_sensor, type);
                            }
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
