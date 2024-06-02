let addPlantsInput = [];
let removeAssociationIds = [];


function createElementFromHTML(htmlString){
    const div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    return div.firstChild;
}


const toDisplayDate = (localDate) => {
    console.log(localDate);
    const day = String(localDate.getDate()).padStart(2, '0');
    const month = String(localDate.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    const year = String(localDate.getFullYear()).slice(-2); // Get last two digits of the year

    return `${day}/${month}/${year}`;
}

function removePlant(associationId) {
    const row = document.querySelector(`tr[data-association-id="${associationId}"]`);
    if (row) {
        row.remove();
        removeAssociationIds.push(associationId);
        updateHiddenInputs();
    }
}

function removeNewPlant(plantId){
    const element = document.querySelector(`ul.currentPlants li[data-plant-id="${plantId}"]`);
    addPlantsInput = addPlantsInput.filter(np => !np.startsWith(plantId + ':'));
    updateHiddenInputs();
}


function updateHiddenInputs() {
    document.getElementById('addPlantsInput').value = addPlantsInput.join(',');
    document.getElementById('removeAssociationsInput').value = removeAssociationIds.join(',');
}


const addPlant = (plant_id) => {
    const count = document.getElementById('newPlantCount').value;
    const currentPlants = document.getElementById('currentPlants');
    const [plant_name, temperature, soil_humidity, air_humidity, light, o2] = window.available_plants[plant_id];
    const start_date_local = new Date();

    const element = `
            <li class="association" data-plant-id="${plant_id}">
                <div class="controls">
                    <p>
                        <span><span>×</span>${count}</span>&nbsp;
                        ${plant_name}&nbsp;
                        <span>(${toDisplayDate(start_date_local)})</span>
                    </p>
    
                    <button type="button" onclick="removeNewPlant(${plant_id})">Retirer</button>
                </div>
                <div class="config">
                    <p>
                        Temp&#x202F;: ${temperature}°C,
                        Sol HR&#x202F;: ${soil_humidity}%,
                        Air HR&#x202F;: ${air_humidity}%,
                        Lux&#x202F;: ${light},
                        O2&#x202F;: ${o2}%
                    </p>
                </div>
            </li>`

    currentPlants.innerHTML += element;

}

const updateSearchPlants = (searchValue) => {
    const plantList = document.getElementById('plant-results');
    const filteredPlants = Object.keys(window.available_plants).filter((id) => {
        return window.available_plants[id][0].toLowerCase().includes(searchValue)
    });

    plantList.innerHTML = '';
    filteredPlants.forEach((id) => {
        const [plant_name, temperature, soil_humidity, air_humidity, light, o2] = window.available_plants[id];
        const element = createElementFromHTML(`
            <li data-plant-id="${id}">
                <div role="button">
                    <p>${plant_name}</p>
                </div>
                <div>
                    <p>
                        Temp&#x202F;: ${temperature}°C,
                        Sol HR&#x202F;: ${soil_humidity}%,
                        Air HR&#x202F;: ${air_humidity}%,
                        Lux&#x202F;: ${light},
                        O2&#x202F;: ${o2}%
                    </p>
                </div>
            </li>`)

        element.addEventListener('click', function(){
            const plantInput = document.getElementById('newPlantInput');
            plantInput.value = plant_name;
            plantInput.setAttribute('data-plant-id', id);
            plantList.innerHTML = '';
        });

        plantList.appendChild(element);
    });

    if(filteredPlants.length === 0){
        plantList.innerHTML = '<li><p>Aucune plante trouvée</p></li>';
    }

}

document.addEventListener("DOMContentLoaded", function() {

    const currentPlants = document.getElementById('currentPlants');

    Object.keys(window.current_plants).forEach((association_id) => {
        const [plant_id, count, start_date] = window.current_plants[association_id];
        const [plant_name, temperature, soil_humidity, air_humidity, light, o2] = window.available_plants[plant_id];


        console.log(window.current_plants, start_date)
        const start_date_utc = new Date(start_date);
        const start_date_local = new Date(start_date_utc.getTime() - (start_date_utc.getTimezoneOffset() * 60000))


        const element = `
            <li class="association" data-association-id="${association_id}">
                <div class="controls">
                    <p>
                        <span><span>×</span>${count}</span>&nbsp;
                        ${plant_name}&nbsp;
                        <span>(${toDisplayDate(start_date_local)})</span></p>
    
                    <button type="button" onclick="removePlant(${association_id})">Retirer</button>
                </div>
                <div class="config">
                    <p>
                        Temp&#x202F;: ${temperature}°C,
                        Sol HR&#x202F;: ${soil_humidity}%,
                        Air HR&#x202F;: ${air_humidity}%,
                        Lux&#x202F;: ${light},
                        O2&#x202F;: ${o2}%
                    </p>
                </div>
            </li>`

        currentPlants.innerHTML += element;
    })

    document.getElementById('newPlantSearch').addEventListener('input', function(){
        const searchValue = this.value.toLowerCase();
        updateSearchPlants(searchValue);
    })
    updateSearchPlants('');


    // const plantInput = document.getElementById('newPlantInput');
    // const plantList = document.getElementById('plantList');
    //
    // plantInput.addEventListener('input', function() {
    //     const searchValue = plantInput.value.toLowerCase();
    //     const filteredPlants = availablePlants.filter(([id, [name]]) => name.toLowerCase().includes(searchValue));
    //
    //     plantList.innerHTML = '';
    //     filteredPlants.forEach(([id, [name]]) => {
    //         const option = document.createElement('div');
    //         option.textContent = name;
    //         option.setAttribute('data-plant-id', id);
    //         option.addEventListener('click', function() {
    //             plantInput.value = name;
    //             plantInput.setAttribute('data-plant-id', id);
    //             plantList.innerHTML = '';
    //         });
    //         plantList.appendChild(option);
    //     });
    // });
});

// document.getElementById('plantForm').addEventListener('submit', function(event) {
//     const counts = document.querySelectorAll('input[name^="count_"]');
//     counts.forEach(count => {
//         if (count.name.startsWith('count_new_') && count.value == 0) {
//             const plantId = count.name.replace('count_new_', '');
//             newPlants = newPlants.filter(np => !np.startsWith(plantId + ':'));
//         } else if (count.name.startsWith('count_') && count.value == 0) {
//             const associationId = count.name.replace('count_', '');
//             removePlants.push(associationId);
//         }
//     });
//     updateHiddenInputs();
// });
