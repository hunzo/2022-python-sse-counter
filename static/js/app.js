const sse = new EventSource("/stream")

sse.addEventListener(
  "message",
  (e) => {
    const data = JSON.parse(e.data)
    const counter = document.querySelector("#counter")
    const kpm = document.querySelector("#kpm")
    counter.innerText = data.count
    kpm.innerText = `count per minutes: ${data.kpm}`
  },
  false,
)
