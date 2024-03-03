function ReSendOTP(username, mess_id) {

    mess = document.getElementById(mess_id);
    mess.innerText = "Sending...";
    $.ajax({
      type: 'GET',
      url: '/resend_otp',
      data: { user: username },
      success: function (data) {
        mess.innerText = "Resend";
      }
    })
  };