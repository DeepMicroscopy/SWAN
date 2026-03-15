"use strict";

(() => {
    if (window.location.href.endsWith("/add/")) return;

    document.addEventListener("DOMContentLoaded", function () {
        const labels = document.getElementById("id_labels_textarea");
        const postpone = document.getElementById("id_postpone");

        const origLabels = labels.value;
        const origPostpone = postpone.value;

        document.getElementById("ui_form").addEventListener("submit", e => {
            if (labels.value !== origLabels || postpone.value !== origPostpone) {
                if (!confirm("Changing 'labels' or 'postpone' may affect results of related studies. Continue?")) {
                    e.preventDefault();
                }
            }
        });
    });
})()