document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM content loaded");

    // Generate a unique reference_id based on the date and time
    var reference_id = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(3, -5);
    document.getElementById('ref_id').value = reference_id;
    console.log("Reference ID set:", reference_id);
});