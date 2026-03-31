async function predict() {
  // 1. Get values
  let h = document.getElementById("humidity").value;
  let p = document.getElementById("pressure").value;
  let w = document.getElementById("wind").value;
  let resultDiv = document.getElementById("result");

  // 2. Validation
  if (!h || !p || !w) {
    resultDiv.innerHTML = "Please enter all fields!";
    return;
  }

  resultDiv.innerHTML = "Predicting...";

  try {
    // 3. Send data to Flask
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

    // 4. Display & Change Background
    if (data.status === "success") {
      const temp = data.prediction;
      resultDiv.innerHTML = `Prediction: ${temp.toFixed(2)}°C`;

      // --- DYNAMIC BACKGROUND LOGIC ---
      if (temp > 30) {
        // Hot: Deep Orange/Red
        document.body.style.background = "linear-gradient(135deg, #ff4b2b, #ff416c)";
      } else if (temp > 20) {
        // Pleasant: Sunset Orange/Yellow
        document.body.style.background = "linear-gradient(135deg, #f2994a, #f2c94c)";
      } else if (temp > 10) {
        // Cool: Calm Blue/Green
        document.body.style.background = "linear-gradient(135deg, #56ab2f, #a8e063)";
      } else {
        // Cold: Icy Blue
        document.body.style.background = "linear-gradient(135deg, #2980b9, #6dd5fa)";
      }
      
    } else {
      resultDiv.innerHTML = `Error: ${data.message}`;
    }
  } catch (error) {
    resultDiv.innerHTML = "Connection Error!";
    console.error(error);
  }
}

