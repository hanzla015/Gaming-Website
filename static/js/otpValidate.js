function clearErrors(){

    errors = document.getElementsByClassName("error");
    for(let item of errors)
    {
        item.innerHTML = "";
    } 
}

// set errors inside tags of id

function setError(div_id, error){
    // id = div id
    element = document.getElementById(div_id)
    element.getElementsByClassName("error")[0].innerHTML = error;
}

function validateForm(){
    var returnVal = true;
    clearErrors();
    // Validating Otp 
    var otp = document.forms['otpForm']["otp"].value;
    if (otp.length<6){
        setError("otp", "OTP cannot be less than 6 digits!");
        returnVal = false;
    }
    if (otp.length>6){
        setError("otp", "OTP cannot be greater than 6 digits!");
        returnVal = false;
    }

    return returnVal;
}