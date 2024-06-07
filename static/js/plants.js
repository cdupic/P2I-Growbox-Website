let addPlantsData = [];
let addPlantsCountData = [];
let removeAssociationData = [];
let removeAssociationCountData = [];

function updateHiddenInputs(){
    document.getElementById('addPlantsInput').value = addPlantsData.join(',');
    document.getElementById('addPlantsCountInput').value = addPlantsCountData.join(',');
    document.getElementById('removeAssociationsInput').value = removeAssociationData.join(',');
    document.getElementById('removeAssociationsCountInput').value = removeAssociationCountData.join(',');
}

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


function removeExistingPlant(associationId, all = false){
    const row = document.querySelector(`ul#currentPlants li[data-association-id="${associationId}"]`);
    if(row){
        let count = 0;
        if(!all) count = Math.max(0, parseInt(row.getAttribute('data-count')) - 1);

        if(removeAssociationData.includes(associationId)){
            const index = removeAssociationData.indexOf(associationId);
            removeAssociationCountData[index] = count;
        }else{
            removeAssociationData.push(associationId);
            removeAssociationCountData.push(count);
        }

        row.querySelector('span').innerHTML = `<span>×</span>${count}`;
        row.setAttribute('data-count', count.toString());
        updateHiddenInputs();
    }
}

function addExistingPlant(associationId){
    const row = document.querySelector(`ul#currentPlants li[data-association-id="${associationId}"]`);
    if(row){
        let count = parseInt(row.getAttribute('data-count')) + 1;
        const original_count = parseInt(row.getAttribute('data-original-count'));
        if(count > original_count) count = original_count;

        row.querySelector('span').innerHTML = `<span>×</span>${count}`;
        row.setAttribute('data-count', count.toString());

        if(count === original_count){
            if(removeAssociationData.includes(associationId)){
                const index = removeAssociationData.indexOf(associationId);
                delete removeAssociationData[index];
                delete removeAssociationCountData[index];
            }
        }else{
            if(removeAssociationData.includes(associationId)){
                const index = removeAssociationData.indexOf(associationId);
                removeAssociationCountData[index] = count;
            }else{
                removeAssociationData.push(associationId);
                removeAssociationCountData.push(count);
            }
        }
        updateHiddenInputs();
    }
}

function removeNewPlant(plantId, all = false){
    const row = document.querySelector(`ul#currentPlants li[data-plant-id="${plantId}"]`);

    if(row){
        let count = 0;
        if(!all) count = Math.max(0, parseInt(row.getAttribute('data-count')) - 1);

        if(count === 0){
            row.remove();
            if(addPlantsData.includes(plantId)){
                const index = addPlantsData.indexOf(plantId);
                delete addPlantsData[index];
                delete addPlantsCountData[index];
            }
        }else{
            if(addPlantsData.includes(plantId)){
                const index = addPlantsData.indexOf(plantId);
                addPlantsCountData[index] = count;
            }else{
                addPlantsData.push(plantId);
                addPlantsCountData.push(count);
            }

            row.querySelector('span').innerHTML = `<span>×</span>${count}`;
            row.setAttribute('data-count', count.toString());
        }
        updateHiddenInputs();
    }
}

const addNewPlant = (plant_id) => {
    let count = parseInt(document.getElementById('newPlantCount').value);
    if(count < 0) count = -count;
    if(!count || count < 1) count = 1;
    const currentPlants = document.getElementById('currentPlants');

    if(addPlantsData.includes(plant_id)){
        const index = addPlantsData.indexOf(plant_id);
        addPlantsCountData[index] = addPlantsCountData[index] + count;

        const row = document.querySelector(`ul#currentPlants li[data-plant-id="${plant_id}"]`);
        row.querySelector('span').innerHTML = `<span>×</span>${addPlantsCountData[index]}`;
        row.setAttribute('data-count', addPlantsCountData[index].toString());

    }else{
        addPlantsData.push(plant_id);
        addPlantsCountData.push(count);

        const [plant_name, temperature, soil_humidity, air_humidity, light, o2] = window.available_plants[plant_id];
        const start_date_local = new Date();

        const element = `
            <li class="association" data-plant-id="${plant_id}" data-count="${count}">
                <div class="controls">
                    <p>
                        <span><span>×</span>${count}</span>&nbsp;
                        ${plant_name}&nbsp;
                        <span>(${toDisplayDate(start_date_local)})</span>
                    </p>
    
                    <div>
                        <button type="button" class="button-pm" onclick="removeNewPlant(${plant_id})">–</button>
                        <button type="button" class="button-pm" onclick="addNewPlant(${plant_id})">+</button>
                        <button type="button" class="button-rm" onclick="removeNewPlant(${plant_id}, true)">Retirer</button>
                    </div>
                </div>
                <div class="config">
                    <p>
                        Temp&#x202F;: ${temperature}°C,
                        Sol HR&#x202F;: ${soil_humidity}%,
                        Air HR&#x202F;: ${air_humidity}%,
                        Lux&#x202F;: ${light}
                    </p>
                </div>
            </li>`

        currentPlants.innerHTML += element;
    }
    updateHiddenInputs()
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
            <li data-plant-id="${id}" onclick="addNewPlant(${id})">
                <div role="button">
                    <p>${plant_name}</p>
                </div>
                <div class="config">
                    <p>
                        Temp&#x202F;: ${temperature}°C,
                        Sol HR&#x202F;: ${soil_humidity}%,
                        Air HR&#x202F;: ${air_humidity}%,
                        Lux&#x202F;: ${light}
                    </p>
                </div>
            </li>`)

        plantList.appendChild(element);
    });

    if(filteredPlants.length === 0){
        plantList.innerHTML = '<li><p>Aucune plante trouvée</p></li>';
    }

}

document.addEventListener("DOMContentLoaded", function(){

    const customConfigInputs = document.getElementById('manual-config-inputs');
    const autoConfigInputs = document.getElementById('auto-config-inputs');
    const autoConfigButton = document.getElementById('auto-config-button');

    if(window.is_custom_config){
        customConfigInputs.style.display = 'block';
        autoConfigButton.value = 'Passer en configuration automatique'
        autoConfigButton.classList = 'main-button red'
    }else{
        autoConfigInputs.style.display = 'block';

    }


    const currentPlants = document.getElementById('currentPlants');

    Object.keys(window.current_plants).forEach((association_id) => {
        const [plant_id, count, start_date] = window.current_plants[association_id];
        const [plant_name, temperature, soil_humidity, air_humidity, light, o2] = window.available_plants[plant_id];

        const start_date_utc = new Date(start_date);
        const start_date_local = new Date(start_date_utc.getTime() - (start_date_utc.getTimezoneOffset() * 60000))


        const element = `
            <li class="association" data-association-id="${association_id}" data-count="${count}" data-original-count="${count}">
                <div class="controls">
                    <p>
                        <span><span>×</span>${count}</span>&nbsp;
                        ${plant_name}&nbsp;
                        <span>(${toDisplayDate(start_date_local)})</span>
                    </p>
                    <div>
                        <button type="button" class="button-pm" onclick="removeExistingPlant(${association_id})">–</button>
                        <button type="button" class="button-pm" onclick="addExistingPlant(${association_id})">+</button>
                        <button type="button" class="button-rm" onclick="removeExistingPlant(${association_id}, true)">Retirer</button>
                    </div>
                </div>
                <div class="config">
                    <p>
                        Temp&#x202F;: ${temperature}°C,
                        Sol HR&#x202F;: ${soil_humidity}%,
                        Air HR&#x202F;: ${air_humidity}%,
                        Lux&#x202F;: ${light}
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
});
