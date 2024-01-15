const sse = new EventSource("/stream")

sse.addEventListener(
  "message",
  (e) => {
    const data = JSON.parse(e.data)
    const counter = document.querySelector("#counter")
    counter.innerText = data.count
  },
  false,
)

document.body.onkeyup = function (e) {
  if (e.key === " " || e.code === "Space" || e.keyCode === 32) {
    fetch("/increase", {
      method: "post",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
      })
  }

  if (e.code === "Backspace" || e.keyCode === 8) {
    fetch("/decrease", {
      method: "post",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
      })
  }
}

const increase = async () => {
  console.log("increase by click webapp")
  const response = await fetch("/increase", {
    method: "post",
  })
    .then((res) => res.json())
    .then((data) => {
      return data
    })
  console.log(response)
}

const decrease = async () => {
  console.log("decrease by click webapp")
  const response = await fetch("/decrease", {
    method: "post",
  })
    .then((res) => res.json())
    .then((data) => {
      return data
    })
  console.log(response)
}

const reset = async () => {
  console.log("!reset counter")
  const q = prompt("Reset Counter ?")
  if (!q) {
    alert(`Please enter "yes" to reset Counter:`)
    return
  }

  const response = await fetch("/reset", {
    method: "post",
  })
    .then((res) => res.json())
    .then((data) => {
      return data
    })

  console.log(response)
}

const setCounter = async () => {
  counter = prompt("set counter")
  if (!counter) {
    alter("Please enter your counter of exit")
    return
  }
  const response = await fetch(`/set/${counter}`, {
    method: "post",
  })
    .then((res) => res.json())
    .then((data) => {
      return data
    })

  console.log(response)
}
