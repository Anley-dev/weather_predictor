async function predict() {
  let h = document.getElementById("humidity").value;
  let p = document.getElementById("pressure").value;
  let w = document.getElementById("wind").value;
  let resultDiv = document.getElementById("result");

  if (!h || !p || !w) {
    resultDiv.innerHTML = "Please enter all fields";
    resultDiv.style.color = "#ff4d4d";
    return;
  }

  resultDiv.innerHTML = "Predicting...";
  resultDiv.style.color = "white";

  try {
    let res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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
      resultDiv.style.color = "#00ffcc";

      // --- HISTORY LOGIC ---
      const historyList = document.getElementById('history-list');
      const newEntry = document.createElement('li');
      newEntry.innerHTML = `<strong>${temp.toFixed(2)}°C</strong> <small>(H: ${h}%, P: ${p})</small>`;

      if (historyList.children[0]?.innerText === "No data yet...") {
          historyList.innerHTML = "";
      }
      historyList.insertBefore(newEntry, historyList.firstChild);

      if (historyList.children.length > 5) {
          historyList.removeChild(historyList.lastChild);
      }

      // --- DYNAMIC BACKGROUND ---
      if (temp > 30) document.body.style.background = "linear-gradient(135deg, #ff4b2b, #ff416c)";
      else if (temp > 20) document.body.style.background = "linear-gradient(135deg, #f2994a, #f2c94c)";
      else if (temp > 10) document.body.style.background = "linear-gradient(135deg, #56ab2f, #a8e063)";
      else document.body.style.background = "linear-gradient(135deg, #2980b9, #6dd5fa)";

    } else {
      resultDiv.innerHTML = "Error: " + data.message;
      resultDiv.style.color = "#ff4d4d";
    }
  } catch (error) {
    resultDiv.innerHTML = "Connection error";
    console.log(error);
  }
}

