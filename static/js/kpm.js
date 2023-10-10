let keyPresses = 0
let startTime = null

async function kpm_to_redis(key) {
  const response = await fetch("/keypress", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "kpm": key,
    }),
  })

  return response.json()
}

function updateKPM() {
  const currentTime = Date.now()
  const elapsedTimeSeconds = (currentTime - startTime) / 1000 // Convert to seconds
  const kpm = (keyPresses / elapsedTimeSeconds) * 60 // Convert to minutes
  // fetch to update redis
  let key_per_minutes = kpm.toFixed(2)
  document.getElementById("kpmDisplay").textContent =
    `COUNT_PER_MINUTES: ${key_per_minutes}`
  return key_per_minutes
}

var KPPM = 0

document.addEventListener("keydown", function () {
  // Start the timer when the first key is pressed
  if (keyPresses === 0) {
    startTime = Date.now()
    setInterval(() => {
      KPPM = updateKPM()
    }, 1000) // Update KPM every second
    // setInterval(updateKPM, 1000) // Update KPM every second
  }

  fetch("/keypress", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "kpm": KPPM
    }),
  })
    .then((res) => res.json())
    .then((data) => console.log(data))
    .catch((e) => {
      console.log(e)
    })

  console.log(KPPM)

  // Increment key press count
  keyPresses++
})
