// =====================================
// CardioVision AI Clinical JS
// =====================================
const steps=document.querySelectorAll(".step");
const lines=document.querySelectorAll(".line");

function updateStep(index){

    steps.forEach((step,i)=>{

        if(i<=index)
            step.classList.add("active");
        else
            step.classList.remove("active");

    });

    lines.forEach((line,i)=>{

        if(i<index)
            line.classList.add("active");
        else
            line.classList.remove("active");

    });

}
document.addEventListener("DOMContentLoaded", function () {

    console.log("Clinical JS Loaded");

    const form = document.getElementById("predictionForm");

    if (!form) {
        console.error("predictionForm not found.");
        return;
    }

    const predictBtn = document.getElementById("predictBtn");
    const loader = document.getElementById("loader");

    //--------------------------------------------------
    // Auto BMI
    //--------------------------------------------------

    const weight = document.getElementById("weight");
    const height = document.getElementById("height");
    const bmi = document.getElementById("bmi");

    function calculateBMI() {

        const w = parseFloat(weight?.value);
        const h = parseFloat(height?.value);

        if (!isNaN(w) && !isNaN(h) && h > 0) {

            bmi.value = (w / ((h / 100) * (h / 100))).toFixed(2);

        } else {

            bmi.value = "";

        }
    }

    if (weight) weight.addEventListener("input", calculateBMI);
    if (height) height.addEventListener("input", calculateBMI);

    //--------------------------------------------------
    // Submit
    //--------------------------------------------------
form.addEventListener("submit", async function (e) {

    e.preventDefault();

    if (loader) loader.style.display = "block";

    predictBtn.style.display = "none";
    
    const formData = new FormData(form);

    try {

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        console.log("SERVER RESPONSE:", result);

        if (!result.success) {

            alert(result.error);

            loader.style.display = "none";
            predictBtn.disabled = false;
            predictBtn.innerHTML = "Predict CAD Risk";

            return;
        }

        sessionStorage.setItem(
            "cad_result",
            JSON.stringify(result)
        );

        window.location.href = "/result";

    }

    catch (err) {

        console.error(err);

        loader.style.display = "none";

        predictBtn.disabled = false;

        predictBtn.innerHTML = "Predict CAD Risk";

        alert("Prediction Failed");

    }

});

});