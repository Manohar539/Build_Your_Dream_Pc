// store selected parts
let dataBox = {}
let totalVal = 0


function addItem(type, name, price){

    // remove old if exists
    if(dataBox[type]){
        totalVal -= dataBox[type].price
    }

    // store new
    dataBox[type] = {
        name: name,
        price: parseFloat(price)
    }

    // update UI
    document.getElementById(type).innerText = name

    // update total
    totalVal += parseFloat(price)
    document.getElementById("total").innerText = totalVal
}
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
        alert("Build saved!")
    })
}