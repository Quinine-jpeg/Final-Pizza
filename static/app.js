if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker
        .register("static/js/serviceWorker.js")
        .then((res) => console.log("service worker registered"))
        .catch((err) => console.log("service worker not registered", err));
    });
  }

const error = document.getElementById('error');
const pw = document.getElementById('pw');
const submit = document.getElementById('submit');

function validate() {
  submit.disabled = true;
  if (pw.value.length < 8) {
    error.textContent = 'Password must be 8 characters or longer.'; return;
  } else if (!/[A-Z]/.test(pw.value) || !/[a-z]/.test(pw.value)) {
    error.textContent = 'Password must contain a capital and lowercase letter.'; return;
  } else if (!/\d/.test(pw.value)) {
    error.textContent = 'Password must contain a number'; return;
  } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(pw.value)) {
    error.textContent = 'Password must contain a special character'; return;
  } else {
    submit.disabled = false;
    error.textContent = '';
  }
}

if (pw) {pw.addEventListener('input', validate)}

function encode(event) {
  event.target.value = event.target.value.replace(/['"<>/\\]/g, '');
}

document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('input');
  
  inputs.forEach(function(input) {
    input.addEventListener('input', encode);
    console.log('Listener applied to:', input)
  });
});

function expand(evt) {
  event.target.classList.toggle('expanded');
}

const shortened = document.querySelectorAll('.descrip');
shortened.forEach(function(el) {
  el.addEventListener('click', expand);
})

