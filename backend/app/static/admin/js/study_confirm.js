"use strict";

(() => {
    if (window.location.href.endsWith("/add/")) return;

    document.addEventListener("DOMContentLoaded", function () {
        const dataset = document.getElementById("id_dataset");
        const ui = document.getElementById("id_ui");

        const origDataset = dataset.value;
        const origUi = ui.value;

        document.getElementById("study_form").addEventListener("submit", e => {
            if (dataset.value !== origDataset || ui.value !== origUi) {
                if (!confirm("Changing 'dataset' or 'ui' is not recommended after a study started. Continue?")) {
                    e.preventDefault();
                }
            }
        });
    });
})()