document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM content loaded");

    var habitatDropdown = document.getElementById('id_habitat');
    var mediaTypeDropdown = document.getElementById('id_media');
    var mediaNField = document.getElementById('id_media_n');
    var mediaConcField = document.getElementById('id_media_conc');
    var mediaStatusDropdown = document.getElementById('id_media_wet_dry');
    var mediaUnitsDropdown = document.getElementById('id_media_conc_units');
    var biotaNField = document.getElementById('id_biota_n');
    var biotaConcField = document.getElementById('id_biota_conc');
    var biotaStatusDropdown = document.getElementById('id_biota_wet_dry');
    var biotaUnitsDropdown = document.getElementById('id_biota_conc_units');


    // Helper functions to add options to the dropdown
    function addMediaUnitOption(text, value) {
        var option = document.createElement('option');
        option.text = text;
        option.value = value;
        mediaUnitsDropdown.add(option);
    }

    function addStatusOption(text, value) {
        var option = document.createElement('option');
        option.text = text;
        option.value = value;
        mediaStatusDropdown.add(option);
    }

    function updateMediaType() {
        console.log("updateMediaType() started");

        // Clear previous options
        mediaTypeDropdown.innerHTML = '';

        // Get the selected value of Habitat
        var selectedHabitat = habitatDropdown.value.toLowerCase();

        fetch(`/get-media-for-habitat/?habitat_id=${selectedHabitat}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous options
                mediaTypeDropdown.innerHTML = '';

                // Filter out 'Biota' from the options, add else
                data.filter(media => media.media_type.toLowerCase() !== 'biota').forEach(function (media) {
                    var option = new Option(media.media_type, media.media_id);
                    mediaTypeDropdown.add(option);
                });
                // Following the Media Type selection, update the media units possible
                updateMediaUnits();
            })
            .catch(error => console.error('Error fetching media types:', error));
    }

    // Function to update Media Units based on the selected Media Type
    function updateMediaUnits() {
        if (!mediaTypeDropdown.options.length || mediaTypeDropdown.selectedIndex < 0) {
            console.log("Media type not selected or options not available.");
            return; // Exit if no options are available or selected
        }
        console.log("updateMediaUnits() started");

        // Clear previous options
        mediaUnitsDropdown.innerHTML = '';
        mediaStatusDropdown.innerHTML = '';

        // Get the selected value of Media Type
        var selectedMedia = mediaTypeDropdown.options[mediaTypeDropdown.selectedIndex];

        var selectedMediaType = selectedMedia.text.toLowerCase();

        // Add unit options based on the selected Media Type
        if (selectedMediaType === 'air') {
            addMediaUnitOption('Bq/m3', 'Bq/m3');
        } else if ((selectedMediaType === 'soil')
            || (selectedMediaType === "sediment")
            || (selectedMediaType === "water")) {
            addMediaUnitOption('µCi/kg', 'µCi/kg');
            addMediaUnitOption('Bq/g', 'Bq/g');
            addMediaUnitOption('Bq/m2', 'Bq/m2');
            addMediaUnitOption('mBq/g', 'mBq/g');
            addMediaUnitOption('mBq/kg', 'mBq/kg');
            addMediaUnitOption('mg/g', 'mg/g');
            addMediaUnitOption('mg/kg', 'mg/kg');
            addMediaUnitOption('pCi/g', 'pCi/g');
            addMediaUnitOption('pCi/kg', 'pCi/kg');
            addMediaUnitOption('ppb', 'ppb');
            addMediaUnitOption('ppm', 'ppm');
            addMediaUnitOption('ug/g', 'ug/g');
            addMediaUnitOption('ug/kg', 'ug/kg');
        }

        // Add wt/dry options based on the selected Media Type
        if (selectedMediaType === 'air') {
            addStatusOption('Air', 'Air');
        } else if (selectedMediaType === "water") {
            addStatusOption('Water', 'Water');
        } else if (selectedMediaType === 'soil') {
            addStatusOption('Dry', 'Dry');
        }

        // If possible, fill in the CR now
        updateConcentrationRatio();
    }


    habitatDropdown.addEventListener('input', updateMediaType);
    mediaTypeDropdown.addEventListener('input', updateMediaUnits);
    updateMediaType();
    updateMediaUnits();

    // Function to update Concentration Ratio based on Media and Biota Concentration
    function updateConcentrationRatio() {
        if (mediaUnitsDropdown.selectedIndex < 0 || biotaUnitsDropdown.selectedIndex < 0) {
            console.log("Prerequisites for updateConcentrationRatio not met");
            return; // Exit if required selections are not made
        }
        console.log("updateConcentrationRatio() started");
        var mediaUnitSymbol = document.getElementById('id_media_conc_units').value;
        console.log("mediaUnitSymbol", mediaUnitSymbol);
        var biotaUnitSymbol = document.getElementById('id_biota_conc_units').value;
        console.log("biotaUnitSymbol", biotaUnitSymbol);
        var mediaType = document.getElementById('id_media').options[document.getElementById('id_media').selectedIndex].text;
        console.log("mediaType", mediaType);
        var biotaType = document.getElementById('id_tissue').options[document.getElementById('id_tissue').selectedIndex].text;
        console.log("biotaType", biotaType);

        fetch(`/get_correction_factor/?unit_symbol=${mediaUnitSymbol}&media_type=${mediaType}`)
            .then(response => response.json())
            .then(mediaData => {
                // Make AJAX request for biota unit correction factor
                fetch(`/get_correction_factor/?unit_symbol=${biotaUnitSymbol}&media_type=${biotaType}`)
                    .then(response => response.json())
                    .then(biotaData => {
                        // Display the result for media unit
                        var mediaCorrectionFactor = mediaData.correction_factor || 1.0;
                        var mediaConcentration = parseFloat(mediaConcField.value);
                        var mediaResult = mediaCorrectionFactor * mediaConcentration;
                        // updating invisible field to save this too
                        console.log("setting stand_media_conc with ", mediaResult);
                        document.getElementById('id_stand_media_conc').value = mediaResult;

                        // Display the result for biota unit
                        var biotaCorrectionFactor = biotaData.correction_factor || 1.0;
                        var biotaConcentration = parseFloat(biotaConcField.value);
                        var biotaResult = biotaCorrectionFactor * biotaConcentration;
                        console.log("setting stand_biota_conc with ", biotaResult);
                        document.getElementById('id_stand_biota_conc').value = biotaResult;

                        // Calculate and display the Concentration Ratio
                        var crField = document.getElementById('id_cr');
                        var concentrationRatio = biotaResult / mediaResult;
                        console.log("Concentration Ratio before conversion:", concentrationRatio);
                        concentrationRatio = concentrationRatio.toFixed(10); // limit to 10 decimal places
                        console.log("Concentration Ratio after conversion:", concentrationRatio);
                        crField.value = concentrationRatio;
                        document.getElementById('id_cr').value = concentrationRatio;
                    })
                    .catch(biotaError => {
                        console.error('Error fetching biota correction factor:', biotaError);
                    });
            })
            .catch(mediaError => {
                console.error('Error fetching media correction factor:', mediaError);
            });
    }

    mediaNField.addEventListener('input', updateConcentrationRatio);
    mediaConcField.addEventListener('input', updateConcentrationRatio);
    mediaStatusDropdown.addEventListener('input', updateConcentrationRatio);
    mediaUnitsDropdown.addEventListener('input', updateConcentrationRatio);
    biotaNField.addEventListener('input', updateConcentrationRatio);
    biotaConcField.addEventListener('input', updateConcentrationRatio);
    biotaStatusDropdown.addEventListener('input', updateConcentrationRatio);
    biotaUnitsDropdown.addEventListener('input', updateConcentrationRatio);
})