const sse = new EventSource('/stream')

sse.addEventListener(
    'message',
    (e) => {
        var data = JSON.parse(e.data)
        let counter = document.querySelector("#counter")
        let kpm = document.querySelector("#kpm")
        counter.innerText = data.count
        kpm.innerText = `COUNT_PER_MINUTES: ${data.kpm}`
        
        // let kpm = document.querySelector("#kpm")
        // kpm.innerText = data.kpm
        
        // let status = document.querySelector("#control-status")
        // console.log(data.control)
        // console.log(status.innerText)
        // status.innerText = data.control
        // data.control == "stop" ? status.style.background = "red" : status.style.background = "green"
    },
    false
)
