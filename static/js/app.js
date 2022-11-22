const sse = new EventSource('/stream')

sse.addEventListener(
    'message',
    (e) => {
        var data = JSON.parse(e.data)
        let counter = document.querySelector("#counter")
        counter.innerText = data.count
        // let status = document.querySelector("#control-status")
        // console.log(data.control)
        // console.log(status.innerText)
        // status.innerText = data.control
        // data.control == "stop" ? status.style.background = "red" : status.style.background = "green"
    },
    false
)
