document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM content loaded");

    // Reference to the ref_id input
    var refIdInput = document.getElementById('ref_id');

    // Only generate a new reference_id if the ref_id input does not already have a value
    if (!refIdInput.value) {
        var reference_id = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(2);
        refIdInput.value = reference_id;
        console.log("Reference ID set:", reference_id);
    } else {
        console.log("Retaining existing Reference ID:", refIdInput.value);
    }
});