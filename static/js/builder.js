// store selected parts
let dataBox = {}
let totalVal = 0

function addItem(type, name, price, power, socket){

    // remove old
    if(dataBox[type]){
        totalVal -= dataBox[type].price
    }

    // store
    dataBox[type] = {
        name: name,
        price: parseFloat(price),
        power: parseInt(power || 0),
        socket: socket || ""
    }

    // update UI
    document.getElementById(type).innerText = name

    // update total (UI only)
    totalVal = 0
    for(let key in dataBox){
        totalVal += dataBox[key].price
    }

    document.getElementById("total").innerText = totalVal
}


// CSRF TOKEN
function getToken(name) {
    let val = null
    if (document.cookie && document.cookie !== '') {
        let arr = document.cookie.split(';')
        for (let i = 0; i < arr.length; i++) {
            let c = arr[i].trim()
            if (c.substring(0, name.length + 1) === (name + '=')) {
                val = decodeURIComponent(c.substring(name.length + 1))
                break
            }
        }
    }
    return val
}


// SAVE BUILD → BACKEND
function saveBuild(){

    if(Object.keys(dataBox).length === 0){
        alert("Build something first")
        return
    }

    fetch("/save-config/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": getToken("csrftoken")
        },
        body: JSON.stringify(dataBox)
    })
    .then(res => res.json())
    .then(data => {

        // ✅ SHOW BACKEND RESULTS (IMPORTANT)
        document.getElementById("power").innerText = data.power
        document.getElementById("compat").innerText = data.compatibility
        document.getElementById("perf").innerText = data.performance

        alert("Build saved!")
    })
}


// CATEGORY FILTER
function showCat(type){

    let items = document.querySelectorAll(".boxP")

    for(let i=0; i<items.length; i++){

        let t = items[i].getAttribute("data-type")

        if(t === type){
            items[i].style.display = "block"
        }else{
            items[i].style.display = "none"
        }

    }

}