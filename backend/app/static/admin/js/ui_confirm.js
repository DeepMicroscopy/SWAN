"use strict";

(() => {
    if (window.location.href.endsWith("/add/")) return;

    document.addEventListener("DOMContentLoaded", function () {
        const labels = document.getElementById("id_labels_textarea");
        const postpone = document.getElementById("id_postpone");

        // noinspection JSUnresolvedReference
        const origLabels = labels.value;
        // noinspection JSUnresolvedReference
        const origPostpone = postpone.value;

        document.getElementById("ui_form").addEventListener("submit", e => {
            // noinspection JSUnresolvedReference
            if (labels.value !== origLabels || postpone.value !== origPostpone) {
                if (!confirm("Changing 'labels' or 'postpone' may affect results of related studies. Continue?")) {
                    e.preventDefault();
                }
            }
        });
    });
})()