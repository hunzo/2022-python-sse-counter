const sse = new EventSource('/stream')

sse.addEventListener(
    'message',
    (e) => {
        var data = JSON.parse(e.data)
        let counter = document.querySelector("#counter")
        let kpm = document.querySelector("#kpm")
        counter.innerText = data.count
        kpm.innerText = `count per minutes: ${data.kpm}`
    },
    false
)
