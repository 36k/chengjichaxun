function doPost() {
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;
  var email = document.getElementById('email').value;
  console.log(username)
  $.post('http:127.0.0.1：5000/POST/', {
    'username': username,
    'password': password,
    'email': email
  }, function(data) {
    alert(data);
  })
}
