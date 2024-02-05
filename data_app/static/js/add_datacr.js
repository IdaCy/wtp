document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM content loaded");
    // Generate a unique reference_id based on the date and time
    /*var reference_id = new Date().toISOString().replace(/[-:TZ.]/g, '');*/
    var reference_id = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(3, -5);
    document.getElementById('ref_id').value = reference_id;
    console.log("Reference ID set:", reference_id);

    // Get references to the Media Type and Media Units dropdowns
    var habitatDropdown = document.getElementById('id_habitat');
    var mediaTypeDropdown = document.getElementById('id_media');
    var mediaUnitsDropdown = document.getElementById('id_media_conc_units');
    var mediaWetDryDropdown = document.getElementById('id_media_wet_dry');

    // Function to update Media Type based on the selected Habitat
    function updateMediaType() {
        console.log("updateMediaType() started");
        // Clear previous options
        mediaTypeDropdown.innerHTML = '';

        // Get the selected value of Habitat
        var selectedHabitat = habitatDropdown.value.toLowerCase();
        var selectedHabitatIndex = habitatDropdown.selectedIndex;
        var selectedHabitatText = habitatDropdown.options[selectedHabitatIndex].text.toLowerCase();
        console.log("Selected Habitat: ", selectedHabitatText);

        console.log("Selected Habitat no: ", selectedHabitat);


        console.log("changes follow");
        //var selectedHabitatId = habitatDropdown.value;
        //console.log("Selected Habitat ID: ", selectedHabitatId);

        fetch(`/get-media-for-habitat/?habitat_id=${selectedHabitat}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous options
                mediaTypeDropdown.innerHTML = '';

                // Filter out 'Biota' from the options, add else
                data.filter(media => media.media_type.toLowerCase() !== 'biota').forEach(function (media) {
                    var option = new Option(media.media_type, media.media_id);
                    console.log("media_type: ", media.media_type);
                    console.log("id: ", media.id);
                    console.log("media_id: ", media.media_id);
                    mediaTypeDropdown.add(option);
                });
            })
            .catch(error => console.error('Error fetching media types:', error));
    }

    // Function to update Media Units based on the selected Media Type
    function updateMediaUnits() {
        console.log("updateMediaUnits() started");
        // Clear previous options
        mediaUnitsDropdown.innerHTML = '';
        mediaWetDryDropdown.innerHTML = '';

        // Get the selected value of Media Type
        var selectedMedia = mediaTypeDropdown.options[mediaTypeDropdown.selectedIndex];
        console.log("selectedMedia: ", selectedMedia);
        var selectedMediaID = selectedMedia.value;
        console.log("selectedMediaID: ", selectedMediaID);
        var selectedMediaType = selectedMedia.text.toLowerCase();
        console.log("selectedMediaType: ", selectedMediaType);

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
            addWetDryOption('Air', 'Air');
        } else if (selectedMediaType === "water") {
            addWetDryOption('Water', 'Water');
        } else if (selectedMediaType === 'soil') {
            addWetDryOption('Dry', 'Dry');
        }
    }

    // Helper functions to add options to the dropdown
    function addMediaUnitOption(text, value) {
        var option = document.createElement('option');
        option.text = text;
        option.value = value;
        mediaUnitsDropdown.add(option);
    }

    function addWetDryOption(text, value) {
        var option = document.createElement('option');
        option.text = text;
        option.value = value;
        mediaWetDryDropdown.add(option);
    }

    // Attach the functions to the change event of dropdowns
    habitatDropdown.addEventListener('change', updateMediaType);
    mediaTypeDropdown.addEventListener('change', updateMediaUnits);

    // Initialize functions on page load
    //updateMediaType();
    //updateMediaUnits();

    var mediaConcField = document.getElementById('id_media_conc');
    var biotaConcField = document.getElementById('id_biota_conc');
    mediaConcField.addEventListener('input', updateTest);
    mediaUnitsDropdown.addEventListener('input', updateTest);

    function updateTest() {
        console.log("updateTest() started");
        console.log("updateTest() started");
        console.log("updateTest() started");
        console.log("updateTest() started");
    }


    /******************* CR CALCULATIONS ***************************/

        // Get references to the relevant input fields and select dropdowns
    var biotaUnitsDropdown = document.getElementById('id_biota_conc_units');

    // Function to update Concentration Ratio based on Media and Biota Concentration
    function updateConcentrationRatio() {
        console.log("updateConcentrationRatio() started");
        var mediaUnitSymbol = document.getElementById('id_media_conc_units').value;
        console.log("mediaUnitSymbol", mediaUnitSymbol);
        var biotaUnitSymbol = document.getElementById('id_biota_conc_units').value;
        console.log("biotaUnitSymbol", biotaUnitSymbol);
        var mediaType = document.getElementById('id_media').options[document.getElementById('id_media').selectedIndex].text;
        console.log("mediaType", mediaType);

        fetch(`/get_correction_factor/?unit_symbol=${mediaUnitSymbol}&media_type=${mediaType}`)
            .then(response => response.json())
            .then(mediaData => {
                // Make AJAX request for biota unit correction factor
                fetch(`/get_correction_factor/?unit_symbol=${biotaUnitSymbol}&media_type=${mediaType}`)
                    .then(response => response.json())
                    .then(biotaData => {
                        // Display the result for media unit
                        var mediaCorrectionFactor = mediaData.correction_factor || 1.0;
                        var mediaConcentration = parseFloat(mediaConcField.value);
                        var mediaResult = mediaCorrectionFactor * mediaConcentration;
                        // updating invisible field to save this too
                        console.log("setting media_standardised with ", mediaResult);
                        document.getElementById('id_media_standardised').value = mediaResult;

                        // Display the result for biota unit
                        var biotaCorrectionFactor = biotaData.correction_factor || 1.0;
                        var biotaConcentration = parseFloat(biotaConcField.value);
                        var biotaResult = biotaCorrectionFactor * biotaConcentration;
                        console.log("setting biota_standardised with ", biotaResult);
                        document.getElementById('id_biota_standardised').value = biotaResult;

                        // Calculate and display the Concentration Ratio
                        var crField = document.getElementById('id_cr');
                        var concentrationRatio = biotaResult / mediaResult;
                        crField.value = concentrationRatio.toFixed(2);
                    })
                    .catch(biotaError => {
                        console.error('Error fetching biota correction factor:', biotaError);
                    });
            })
            .catch(mediaError => {
                console.error('Error fetching media correction factor:', mediaError);
            });
    }

    // Attach the updateConcentrationRatio function to the input event of Media and Biota Concentration fields
    mediaConcField.addEventListener('input', updateConcentrationRatio);
    biotaConcField.addEventListener('input', updateConcentrationRatio);
    mediaUnitsDropdown.addEventListener('input', updateConcentrationRatio);
    biotaUnitsDropdown.addEventListener('input', updateConcentrationRatio);
    mediaUnitsDropdown.addEventListener('change', updateConcentrationRatio);
});