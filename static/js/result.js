// =======================================
// CardioVision AI Result Page
// =======================================
console.log("RESULT JS LOADED");
document.addEventListener("DOMContentLoaded", function () {

    // ----------------------------
    // Get Prediction
    // ----------------------------

    const raw = sessionStorage.getItem("cad_result");

console.log("RAW STORAGE:", raw);

const prediction = JSON.parse(raw);
document.getElementById("patientName").textContent =
prediction.name || "--";

document.getElementById("patientAge").textContent =
prediction.age || "--";

document.getElementById("patientGender").textContent =
prediction.sex || "--";

document.getElementById("patientBMI").textContent =
prediction.bmi || "--";

document.getElementById("patientBP").textContent =
prediction.bp || "--";

document.getElementById("reportDate").textContent =
new Date().toLocaleDateString();
    // ----------------------------
    // Helper
    // ----------------------------

    function value(v) {
        return v == null ? "--" : Number(v).toFixed(1);
    }

    // ----------------------------
    // Overall Score
    // ----------------------------

    document.getElementById("overallScore").innerHTML =
        value(prediction.overall_score) + "%";

    document.getElementById("riskLevel").innerHTML =
        prediction.risk_level;

    document.getElementById("overallDescription").innerHTML =
        prediction.recommendation;

    // ----------------------------
    // Circle Animation
    // ----------------------------

    const circle = document.getElementById("progressCircle");

    const radius = 100;

    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = circumference;

    circle.style.strokeDashoffset = circumference;

    const offset =
        circumference -
        (prediction.overall_score / 100) * circumference;

    setTimeout(() => {

        circle.style.strokeDashoffset = offset;

    }, 400);

    // ----------------------------
    // Risk Badge Color
    // ----------------------------

    const badge = document.getElementById("riskLevel");

    badge.classList.remove("low");
    badge.classList.remove("moderate");
    badge.classList.remove("high");

    if (prediction.risk_level.includes("Low")) {

        badge.classList.add("low");

    }

    else if (prediction.risk_level.includes("Moderate")) {

        badge.classList.add("moderate");

    }

    else {

        badge.classList.add("high");

    }

    // ----------------------------
    // Individual Scores
    // ----------------------------

    document.getElementById("clinicalScore").innerHTML =
        value(prediction.clinical) + "%";

    document.getElementById("ecgScore").innerHTML =
        prediction.ecg == null ? "--" : value(prediction.ecg) + "%";

    document.getElementById("echoScore").innerHTML =
        prediction.echo == null ? "--" : value(prediction.echo) + "%";

    document.getElementById("tmtScore").innerHTML =
        prediction.tmt == null ? "--" : value(prediction.tmt) + "%";

    // ----------------------------
    // Progress Bars
    // ----------------------------

    function animateBar(id, score) {

        const bar = document.getElementById(id);

        if (!bar) return;

        setTimeout(() => {

            bar.style.width = score + "%";

        }, 500);

    }

    animateBar("clinicalProgress", prediction.clinical || 0);
    animateBar("ecgProgress", prediction.ecg || 0);
    animateBar("echoProgress", prediction.echo || 0);
    animateBar("tmtProgress", prediction.tmt || 0);

    // ----------------------------
    // Status Labels
    // ----------------------------

    function status(score) {

        if (score == null)
            return "Not Available";

        if (score < 35)
            return "Low Risk";

        if (score < 75)
            return "Moderate Risk";

        return "High Risk";

    }

    document.getElementById("clinicalStatus").innerHTML =
        status(prediction.clinical);

    document.getElementById("ecgStatus").innerHTML =
        status(prediction.ecg);

    document.getElementById("echoStatus").innerHTML =
        status(prediction.echo);

    document.getElementById("tmtStatus").innerHTML =
        status(prediction.tmt);

    // ----------------------------
    // AI Decision
    // ----------------------------
    document.getElementById("aiDecision").innerHTML =
        prediction.risk_level;

    document.getElementById("recommendationText").innerHTML =
        prediction.medical_recommendation;
    // ----------------------------
// Lifestyle Recommendations
// ----------------------------

const lifestyleGrid = document.getElementById("lifestyleGrid");

if (lifestyleGrid) {

    lifestyleGrid.innerHTML = "";

    if (prediction.lifestyle && prediction.lifestyle.length > 0) {

        prediction.lifestyle.forEach(item => {

            lifestyleGrid.innerHTML += `
                <div class="tip">
                    <i class="fa-solid ${item.icon}"></i>
                    <h4>${item.title}</h4>
                    <p>${item.description}</p>
                </div>
            `;

        });

    }

    else {

        lifestyleGrid.innerHTML = `
            <div class="tip">
                <i class="fa-solid fa-heart"></i>
                <h4>Healthy Lifestyle</h4>
                <p>Continue following a balanced diet and regular exercise.</p>
            </div>
        `;

    }

}
    // ----------------------------
    // Risk Factors
    // ----------------------------
const riskFactors = document.getElementById("riskFactors");

riskFactors.innerHTML = "";

if (prediction.risk_factors && prediction.risk_factors.length > 0) {

    prediction.risk_factors.forEach(factor => {

        riskFactors.innerHTML += `<li>${factor}</li>`;

    });

}
else{

    riskFactors.innerHTML =
    "<li>No significant risk factors detected.</li>";

}
    // ----------------------------
    // Comparison Chart
    // ----------------------------
const ctx = document.getElementById("comparisonChart").getContext("2d");

// ===== Gradients =====
const green = ctx.createLinearGradient(0, 0, 0, 400);
green.addColorStop(0, "#7CFC00");
green.addColorStop(1, "#2E7D32");

const orange = ctx.createLinearGradient(0, 0, 0, 400);
orange.addColorStop(0, "#FFD54F");
orange.addColorStop(1, "#F57C00");

const cyan = ctx.createLinearGradient(0, 0, 0, 400);
cyan.addColorStop(0, "#80DEEA");
cyan.addColorStop(1, "#00BCD4");

const purple = ctx.createLinearGradient(0, 0, 0, 400);
purple.addColorStop(0, "#D05CE3");
purple.addColorStop(1, "#8E24AA");

// ===== Plugin for values above bars =====
Chart.register({
    id: "valueLabel",
    afterDatasetsDraw(chart) {

        const { ctx } = chart;

        chart.data.datasets.forEach((dataset, i) => {

            const meta = chart.getDatasetMeta(i);

            meta.data.forEach((bar, index) => {

                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 15px Poppins";
                ctx.textAlign = "center";

                ctx.fillText(
                    dataset.data[index] + "%",
                    bar.x,
                    bar.y - 10
                );

            });

        });

    }
});

new Chart(ctx, {

    type: "bar",

    data: {

        labels: [
            "Clinical",
            "ECG",
            "Echo",
            "TMT"
        ],

        datasets: [{

            label: "Risk (%)",

            data: [
                prediction.clinical || 0,
                prediction.ecg || 0,
                prediction.echo || 0,
                prediction.tmt || 0
            ],

            backgroundColor: [
                green,
                orange,
                cyan,
                purple
            ],

            borderRadius: 15,
            borderSkipped: false,
            barThickness: 80,
            maxBarThickness: 90

        }]
    },

    options: {

        responsive: true,

        animation: {

            duration: 2000,
            easing: "easeOutBounce"

        },

        plugins: {

            legend: {

                position: "top",

                labels: {

                    color: "#ffffff",

                    font: {

                        size: 16,
                        weight: "bold"

                    },

                    padding: 25,
                    boxWidth: 20

                }

            },

            tooltip: {

                backgroundColor: "#101827",

                titleColor: "#00d4ff",

                bodyColor: "#ffffff",

                padding: 15,

                cornerRadius: 10

            }

        },

        scales: {

            x: {

                grid: {

                    display: false

                },

                ticks: {

                    color: "#ffffff",

                    font: {

                        size: 15,
                        weight: "bold"

                    }

                }

            },

            y: {

                beginAtZero: true,

                max: 100,

                ticks: {

                    stepSize: 20,

                    color: "#ffffff",

                    font: {

                        size: 14

                    }

                },

                grid: {

                    color: "rgba(255,255,255,0.08)"

                }

            }

        }

    }

});
});
async function downloadPDF() {

    const { jsPDF } = window.jspdf;

    const report = document.getElementById("report");

    if (!report) {
        alert("Report section not found.");
        return;
    }
    const canvas = await html2canvas(report, {
        scale: 2,
        useCORS: true,
        backgroundColor: "#081220"
    });
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");

    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    const imgWidth = pdfWidth;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    pdf.addImage(
        imgData,
        "PNG",
        0,
        0,
        imgWidth,
        Math.min(imgHeight, pageHeight)
    );

    pdf.save("CardioVision_AI_Report.pdf");
}
document.getElementById("downloadPDF")
.addEventListener("click", downloadPDF);
document.getElementById("generatedDate").innerHTML =
new Date().toLocaleString();