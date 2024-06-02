let newPlants = [];
let removePlants = [];

function addPlant() {
    const plantSelect = document.getElementById('newPlantSelect');
    const plantCount = document.getElementById('newPlantCount').value;
    const plantId = plantSelect.value;
    const plantName = plantSelect.options[plantSelect.selectedIndex].text;

    const row = document.createElement('tr');
    row.innerHTML = `
                <td>${plantName}</td>
                <td>...</td> <!-- Temperature -->
                <td>...</td> <!-- Soil Humidity -->
                <td>...</td> <!-- Air Humidity -->
                <td>...</td> <!-- Light -->
                <td>...</td> <!-- O2 -->
                <td>New</td> <!-- Start Date -->
                <td><input type="number" name="count_new_${plantId}" value="${plantCount}" min="1"></td>
                <td><button type="button" onclick="removeNewPlant(this, '${plantId}')">Remove</button></td>
            `;
    document.getElementById('currentPlants').appendChild(row);
    newPlants.push(plantId + ':' + plantCount);
    updateHiddenInputs();
}

function removePlant(associationId) {
    const row = document.querySelector(`tr[data-association-id="${associationId}"]`);
    if (row) {
        row.remove();
        removePlants.push(associationId);
        updateHiddenInputs();
    }
}

function removeNewPlant(button, plantId) {
    const row = button.closest('tr');
    row.remove();
    newPlants = newPlants.filter(np => !np.startsWith(plantId + ':'));
    updateHiddenInputs();
}

function updateHiddenInputs() {
    document.getElementById('newPlantsInput').value = newPlants.join(',');
    document.getElementById('removePlantsInput').value = removePlants.join(',');
}

document.addEventListener("DOMContentLoaded", function() {

    const currentPlants = document.getElementById('currentPlants');

    window.current_plants.forEach(([associationId, plantId, plantName, temperature, soilHumidity, airHumidity, light, o2, startDate, count]) => {

    })


    const plantInput = document.getElementById('newPlantInput');
    const plantList = document.getElementById('plantList');

    plantInput.addEventListener('input', function() {
        const searchValue = plantInput.value.toLowerCase();
        const filteredPlants = availablePlants.filter(([id, [name]]) => name.toLowerCase().includes(searchValue));

        plantList.innerHTML = '';
        filteredPlants.forEach(([id, [name]]) => {
            const option = document.createElement('div');
            option.textContent = name;
            option.setAttribute('data-plant-id', id);
            option.addEventListener('click', function() {
                plantInput.value = name;
                plantInput.setAttribute('data-plant-id', id);
                plantList.innerHTML = '';
            });
            plantList.appendChild(option);
        });
    });
});

document.getElementById('plantForm').addEventListener('submit', function(event) {
    const counts = document.querySelectorAll('input[name^="count_"]');
    counts.forEach(count => {
        if (count.name.startsWith('count_new_') && count.value == 0) {
            const plantId = count.name.replace('count_new_', '');
            newPlants = newPlants.filter(np => !np.startsWith(plantId + ':'));
        } else if (count.name.startsWith('count_') && count.value == 0) {
            const associationId = count.name.replace('count_', '');
            removePlants.push(associationId);
        }
    });
    updateHiddenInputs();
});
