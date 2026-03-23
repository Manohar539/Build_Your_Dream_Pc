function openLogin(){
    document.getElementById("loginBox").style.display = "flex"
}

function closeLogin(){
    document.getElementById("loginBox").style.display = "none"
}

function goB(type){
    window.location.href = "/builder/?type=" + type;
}