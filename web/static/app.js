async function predict() {
  let h = document.getElementById("humidity").value;
  let p = document.getElementById("pressure").value;
  let w = document.getElementById("wind").value;
  let resultDiv = document.getElementById("result");

  if (!h || !p || !w) {
    resultDiv.innerHTML = "Please enter all fields";
    return;
  }

  resultDiv.innerHTML = "Predicting...";

  try {
    let res = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        humidity: Number(h),
        pressure: Number(p),
        wind: Number(w)
      })
    });

    let data = await res.json();

    if (data.status === "success") {
      const temp = data.prediction;

      resultDiv.innerHTML = `🌡 Prediction: ${temp.toFixed(2)}°C`;

      resultDiv.scrollIntoView({ behavior: "smooth" });
// --- HISTORY LOGIC ---
const historyList = document.getElementById('history-list');
const newEntry = document.createElement('li');

// Create a nice string showing what the AI learned
newEntry.innerHTML = `
    <strong>${temp.toFixed(2)}°C</strong> 
    <small>(H: ${h}%, P: ${p}, W: ${w})</small>
`;

// Remove the "No data yet" message on first click
if (historyList.children[0].innerText === "No data yet...") {
    historyList.innerHTML = "";
}

// Add the new prediction to the top of the list
historyList.insertBefore(newEntry, historyList.firstChild);

// Keep only the last 5 items to keep it clean
if (historyList.children.length > 5) {
    historyList.removeChild(historyList.lastChild);
}

      // Dynamic background
      if (temp > 30) {
        document.body.style.background = "linear-gradient(135deg, #ff4b2b, #ff416c)";
      } else if (temp > 20) {
        document.body.style.background = "linear-gradient(135deg, #f2994a, #f2c94c)";
      } else if (temp > 10) {
        document.body.style.background = "linear-gradient(135deg, #56ab2f, #a8e063)";
      } else {
        document.body.style.background = "linear-gradient(135deg, #2980b9, #6dd5fa)";
      }

    } else {
      resultDiv.innerHTML = "Server error. Try again.";
    }

  } catch (error) {
    resultDiv.innerHTML = "Connection error";
    console.log(error);
  }
}
