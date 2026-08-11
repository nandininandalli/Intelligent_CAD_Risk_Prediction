// ======================================================
// CardioVision AI
// Professional Hospital Report
// ======================================================

document.addEventListener("DOMContentLoaded", function () {

    //----------------------------------------------------
    // Read Prediction
    //----------------------------------------------------

    const raw = sessionStorage.getItem("cad_result");

    if (!raw) {

        alert("No prediction data found.");

        return;
    }

    const prediction = JSON.parse(raw);

    //----------------------------------------------------
    // Helper
    //----------------------------------------------------

    function value(v) {

        if (v === null || v === undefined || v === "")
            return "--";

        return v;
    }

    function percent(v) {

        if (v === null || v === undefined)
            return "--";

        return Number(v).toFixed(1) + "%";
    }

    //----------------------------------------------------
    // Report ID
    //----------------------------------------------------

    document.getElementById("reportID").innerHTML =
        "CAD-" + Math.floor(Math.random() * 1000000);

    document.getElementById("reportID2").innerHTML =
        document.getElementById("reportID").innerHTML;

    //----------------------------------------------------
    // Report Date
    //----------------------------------------------------

    document.getElementById("reportDate").innerHTML =
        new Date().toLocaleString();

    //----------------------------------------------------
    // Patient Details
    //----------------------------------------------------

    document.getElementById("patientID").innerHTML =
        value(prediction.patient_id);

    document.getElementById("patientName").innerHTML =
        value(prediction.patient_name);

    document.getElementById("patientAge").innerHTML =
        value(prediction.age);

    document.getElementById("patientGender").innerHTML =
        value(prediction.sex);

    document.getElementById("patientHeight").innerHTML =
        value(prediction.height) + " cm";

    document.getElementById("patientWeight").innerHTML =
        value(prediction.weight) + " kg";

    document.getElementById("patientBMI").innerHTML =
        value(prediction.bmi);

    document.getElementById("patientBMI2").innerHTML =
        value(prediction.bmi);

    document.getElementById("patientBP").innerHTML =
        value(prediction.bp);

    document.getElementById("patientBP2").innerHTML =
        value(prediction.bp);

    document.getElementById("patientPhone").innerHTML =
        value(prediction.phone);

    document.getElementById("predictionDate").innerHTML =
        value(prediction.date);

    //----------------------------------------------------
    // Clinical Findings
    //----------------------------------------------------

    document.getElementById("patientFBS").innerHTML =
        value(prediction.fbs);

    document.getElementById("patientLDL").innerHTML =
        value(prediction.ldl);

    document.getElementById("patientHDL").innerHTML =
        value(prediction.hdl);

    document.getElementById("patientTG").innerHTML =
        value(prediction.tg);

    //----------------------------------------------------
    // Prediction Scores
    //----------------------------------------------------

    document.getElementById("clinicalScore").innerHTML =
        percent(prediction.clinical);

    document.getElementById("clinicalScore2").innerHTML =
        percent(prediction.clinical);

    document.getElementById("ecgScore").innerHTML =
        percent(prediction.ecg);

    document.getElementById("ecgScore2").innerHTML =
        percent(prediction.ecg);

    document.getElementById("echoScore").innerHTML =
        percent(prediction.echo);

    document.getElementById("echoScore2").innerHTML =
        percent(prediction.echo);

    document.getElementById("tmtScore").innerHTML =
        percent(prediction.tmt);

    document.getElementById("tmtScore2").innerHTML =
        percent(prediction.tmt);

    document.getElementById("overallScore").innerHTML =
        percent(prediction.overall_score);

    document.getElementById("overallRisk").innerHTML =
        prediction.risk_level;

    document.getElementById("overallRisk2").innerHTML =
        prediction.risk_level;
        //----------------------------------------------------
    // AI Medical Recommendation
    //----------------------------------------------------

    document.getElementById("medicalRecommendation").innerHTML =
        prediction.medical_recommendation || "No recommendation available.";

    //----------------------------------------------------
    // Investigation Interpretation
    //----------------------------------------------------

    function interpretation(score){

        if(score == null)
            return "Not Available";

        if(score < 35)
            return "Low Risk";

        if(score < 75)
            return "Moderate Risk";

        return "High Risk";
    }

    document.getElementById("clinicalInterpretation").innerHTML =
        interpretation(prediction.clinical);

    document.getElementById("ecgInterpretation").innerHTML =
        interpretation(prediction.ecg);

    document.getElementById("echoInterpretation").innerHTML =
        interpretation(prediction.echo);

    document.getElementById("tmtInterpretation").innerHTML =
        interpretation(prediction.tmt);

    //----------------------------------------------------
    // Risk Factors
    //----------------------------------------------------

    const riskFactors =
        document.getElementById("riskFactors");

    riskFactors.innerHTML = "";

    if(prediction.risk_factors &&
       prediction.risk_factors.length>0){

        prediction.risk_factors.forEach(factor=>{

            riskFactors.innerHTML +=
            `
            <li>${factor}</li>
            `;

        });

    }

    else{

        riskFactors.innerHTML =
        `
        <li>No significant risk factors detected.</li>
        `;

    }

    //----------------------------------------------------
    // Lifestyle Recommendations
    //----------------------------------------------------

    const lifestyleGrid =
        document.getElementById("lifestyleGrid");

    lifestyleGrid.innerHTML = "";

    if(prediction.lifestyle &&
       prediction.lifestyle.length>0){

        prediction.lifestyle.forEach(item=>{

            lifestyleGrid.innerHTML +=

            `
            <div class="tip">

                <i class="fa-solid ${item.icon}"></i>

                <h4>${item.title}</h4>

                <p>${item.description}</p>

            </div>
            `;

        });

    }

    else{

        lifestyleGrid.innerHTML =

        `
        <div class="tip">

            <i class="fa-solid fa-heart"></i>

            <h4>Healthy Lifestyle</h4>

            <p>

                Continue maintaining
                a balanced diet,
                regular physical activity,
                adequate sleep,
                and periodic health checkups.

            </p>

        </div>
        `;

    }
        //----------------------------------------------------
    // Comparison Chart
    //----------------------------------------------------

    const ctx = document.getElementById("comparisonChart");

    if (ctx) {

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

                    label: "Risk Score (%)",

                    data: [

                        prediction.clinical || 0,
                        prediction.ecg || 0,
                        prediction.echo || 0,
                        prediction.tmt || 0

                    ],

                    backgroundColor: [

                        "#28a745",
                        "#ff9800",
                        "#00BCD4",
                        "#9C27B0"

                    ],

                    borderRadius: 10,
                    borderWidth: 0

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    x: {

                        grid: {

                            display: false

                        },

                        ticks: {

                            color: "#444",
                            font: {

                                size: 13,
                                weight: "600"

                            }

                        }

                    },

                    y: {

                        beginAtZero: true,

                        max: 100,

                        ticks: {

                            stepSize: 20,

                            color: "#444"

                        },

                        grid: {

                            color: "#dddddd"

                        }

                    }

                }

            }

        });

    }

    //----------------------------------------------------
    // Print Button
    //----------------------------------------------------

    const printBtn =
        document.getElementById("printBtn");

    if (printBtn) {

        printBtn.addEventListener("click", () => {

            window.print();

        });

    }

    //----------------------------------------------------
    // Download PDF
    //----------------------------------------------------

    const downloadBtn =
        document.getElementById("downloadBtn");

    if (downloadBtn) {

        downloadBtn.addEventListener("click", downloadPDF);

    }

});
//----------------------------------------------------
// Download PDF
//----------------------------------------------------

async function downloadPDF() {

    const { jsPDF } = window.jspdf;

    const report = document.getElementById("report");

    if (!report) {

        alert("Report not found.");

        return;
    }

    const canvas = await html2canvas(report, {

        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff",
        scrollY: -window.scrollY

    });

    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    const imgWidth = pageWidth;

    const imgHeight = canvas.height * imgWidth / canvas.width;

    let heightLeft = imgHeight;

    let position = 0;

    pdf.addImage(

        imgData,
        "PNG",
        0,
        position,
        imgWidth,
        imgHeight

    );

    heightLeft -= pageHeight;

    while (heightLeft > 0) {

        position = heightLeft - imgHeight;

        pdf.addPage();

        pdf.addImage(

            imgData,
            "PNG",
            0,
            position,
            imgWidth,
            imgHeight

        );

        heightLeft -= pageHeight;

    }

    pdf.save("CardioVision_AI_Report.pdf");

}

//----------------------------------------------------
// Auto Download (Optional)
//----------------------------------------------------

const params = new URLSearchParams(window.location.search);

if (params.get("download") === "true") {

    setTimeout(() => {

        downloadPDF();

    }, 800);

}