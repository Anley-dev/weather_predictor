async function predict() {
  // 1. Get all three values from the new HTML inputs
  let h = document.getElementById("humidity").value;
  let p = document.getElementById("pressure").value;
  let w = document.getElementById("wind").value;

  // 2. Validation
  if (!h || !p || !w) {
    document.getElementById("result").innerHTML = "Please fill all fields!";
    return;
  }

  document.getElementById("result").innerHTML = "Predicting...";

  try {
    // 3. Send all three features to the Flask server
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

    // 4. Display the result
    if (data.status === "success") {
      document.getElementById("result").innerHTML = `Prediction: ${data.prediction}°C`;
    } else {
      document.getElementById("result").innerHTML = `Error: ${data.message}`;
    }
  } catch (error) {
    document.getElementById("result").innerHTML = "Connection failed!";
    console.error(error);
  }
}

