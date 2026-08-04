// -----------------------------
// CardioVision AI Dashboard
// -----------------------------

const form = document.getElementById("predictionForm");

let riskChart = null;
let contributionChart = null;

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const btn = document.querySelector(".predict-btn");

  btn.innerHTML = "Predicting...";
  btn.disabled = true;

  const formData = new FormData(form);

  try {
    const response = await fetch("/predict", {
      method: "POST",

      body: formData,
    });

    const data = await response.json();

    btn.innerHTML = "Predict CAD Risk";
    btn.disabled = false;

    if (!data.success) {
      alert(data.error);

      return;
    }

    //------------------------------------------------
    // Result Cards
    //------------------------------------------------

    document.getElementById("clinicalScore").innerHTML = data.clinical
      ? data.clinical.toFixed(1) + "%"
      : "--";

    document.getElementById("ecgScore").innerHTML = data.ecg
      ? data.ecg.toFixed(1) + "%"
      : "--";

    document.getElementById("echoScore").innerHTML = data.echo
      ? data.echo.toFixed(1) + "%"
      : "--";

    document.getElementById("tmtScore").innerHTML = data.tmt
      ? data.tmt.toFixed(1) + "%"
      : "--";

    document.getElementById("overallScore").innerHTML =
      data.overall_score.toFixed(1) + "%";

    document.getElementById("riskLevel").innerHTML = data.risk_level;

    //------------------------------------------------
    // Recommendation
    //------------------------------------------------

    let recommendation = "";

    if (data.overall_score < 35) {
      recommendation =
        "✅ Low CAD Risk<br><br>" +
        "• Continue healthy lifestyle.<br>" +
        "• Regular exercise.<br>" +
        "• Balanced diet.<br>" +
        "• Annual cardiac check-up.";
    } else if (data.overall_score < 70) {
      recommendation =
        "🟠 Moderate CAD Risk<br><br>" +
        "• Consult a Cardiologist.<br>" +
        "• Monitor Blood Pressure.<br>" +
        "• Reduce Cholesterol.<br>" +
        "• Regular ECG Follow-up.";
    } else {
      recommendation =
        "🔴 High CAD Risk<br><br>" +
        "• Immediate Cardiologist Consultation.<br>" +
        "• Detailed Cardiac Evaluation.<br>" +
        "• Consider Angiography.<br>" +
        "• Lifestyle Modification.<br>" +
        "• Medication as advised.";
    }

    document.getElementById("recommendation").innerHTML = recommendation;

    //------------------------------------------------
    // Risk Chart
    //------------------------------------------------

    if (riskChart != null) riskChart.destroy();

    riskChart = new Chart(
      document.getElementById("riskChart"),

      {
        type: "doughnut",

        data: {
          labels: ["Risk", "Remaining"],

          datasets: [
            {
              data: [data.overall_score, 100 - data.overall_score],

              backgroundColor: ["#ff4b5c", "#2f3d59"],
            },
          ],
        },

        options: {
          responsive: true,

          plugins: {
            legend: {
              labels: {
                color: "white",
              },
            },
          },
        },
      }
    );

    //------------------------------------------------
    // Contribution Chart
    //------------------------------------------------

    if (contributionChart != null) contributionChart.destroy();

    contributionChart = new Chart(
      document.getElementById("contributionChart"),

      {
        type: "bar",

        data: {
          labels: ["Clinical", "ECG", "Echo", "TMT"],

          datasets: [
            {
              label: "Contribution (%)",

              data: [
                60,

                15,

                15,

                10,
              ],

              backgroundColor: ["#4CAF50", "#00BCD4", "#FF9800", "#E91E63"],
            },
          ],
        },

        options: {
          responsive: true,

          scales: {
            y: {
              beginAtZero: true,

              max: 100,

              ticks: {
                color: "white",
              },
            },

            x: {
              ticks: {
                color: "white",
              },
            },
          },

          plugins: {
            legend: {
              labels: {
                color: "white",
              },
            },
          },
        },
      }
    );
  } catch (error) {
    btn.innerHTML = "Predict CAD Risk";
    btn.disabled = false;

    alert("Prediction Failed!");

    console.log(error);
  }
});
// ============================================
// AI CAD Dashboard JavaScript
// ============================================

// Page Fade In
window.addEventListener("load", () => {
  document.body.style.opacity = "1";
});

// ============================================
// Animated Statistics Counter
// ============================================

function animateCounter(element, target, suffix = "") {

  let count = 0;

  const speed = target / 80;

  const timer = setInterval(() => {

      count += speed;

      if (count >= target) {

          count = target;

          clearInterval(timer);

      }

      element.innerHTML = count.toFixed(1) + suffix;

  }, 20);

}

document.querySelectorAll(".stat-card h1").forEach(card => {

  let value = parseFloat(card.innerText);

  let suffix = "%";

  animateCounter(card, value, suffix);

});

// ============================================
// Progress Bar Animation
// ============================================

document.querySelectorAll(".progress div").forEach(bar => {

  const width = bar.style.width;

  bar.style.width = "0";

  setTimeout(() => {

      bar.style.transition = "2s";

      bar.style.width = width;

  }, 300);

});

// ============================================
// Module Card Hover Effect
// ============================================

document.querySelectorAll(".module-card").forEach(card => {

  card.addEventListener("mouseenter", () => {

      card.style.transform = "translateY(-12px) scale(1.03)";

  });

  card.addEventListener("mouseleave", () => {

      card.style.transform = "translateY(0px) scale(1)";

  });

});

// ============================================
// Floating Assistant Card
// ============================================

const assistant = document.querySelector(".assistant-card");

if (assistant) {

  let direction = 1;

  setInterval(() => {

      assistant.style.transform = `translateY(${direction * 8}px)`;

      direction *= -1;

  }, 2000);

}

// ============================================
// Button Ripple Effect
// ============================================

document.querySelectorAll(".primary-btn,.secondary-btn").forEach(button => {

  button.addEventListener("click", function(e) {

      const circle = document.createElement("span");

      const diameter = Math.max(this.clientWidth, this.clientHeight);

      const radius = diameter / 2;

      circle.style.width = circle.style.height = diameter + "px";

      circle.style.left = (e.clientX - this.offsetLeft - radius) + "px";

      circle.style.top = (e.clientY - this.offsetTop - radius) + "px";

      circle.classList.add("ripple");

      const ripple = this.getElementsByClassName("ripple")[0];

      if (ripple) {

          ripple.remove();

      }

      this.appendChild(circle);

  });

});

// ============================================
// Greeting Based on Time
// ============================================

const welcome = document.querySelector(".welcome");

if (welcome) {

  const hour = new Date().getHours();

  let greeting = "Welcome";

  if (hour < 12)

      greeting = "Good Morning";

  else if (hour < 17)

      greeting = "Good Afternoon";

  else

      greeting = "Good Evening";

  welcome.innerHTML =
      `<i class="fa-solid fa-user-doctor"></i> ${greeting}, Admin`;

}

// ============================================
// Live Date & Time
// ============================================

function updateTime() {

  const now = new Date();

  const options = {

      weekday: "short",

      day: "numeric",

      month: "short",

      year: "numeric"

  };

  const date = now.toLocaleDateString("en-US", options);

  const time = now.toLocaleTimeString();

  document.title = "AI CAD Dashboard | " + date + " | " + time;

}

setInterval(updateTime, 1000);

// ============================================
// Scroll Animation
// ============================================

const observer = new IntersectionObserver(entries => {

  entries.forEach(entry => {

      if (entry.isIntersecting) {

          entry.target.style.opacity = "1";

          entry.target.style.transform = "translateY(0px)";

      }

  });

});

document.querySelectorAll(".module-card,.stat-card,.summary-card,.report-card").forEach(card => {

  card.style.opacity = "0";

  card.style.transform = "translateY(60px)";

  card.style.transition = ".8s";

  observer.observe(card);

});

// ============================================
// Console Message
// ============================================

console.log("❤️ AI CAD Dashboard Loaded Successfully");