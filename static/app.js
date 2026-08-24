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

/*
function expand(evt) {
  event.target.classList.toggle('expanded');
}

const shortened = document.querySelectorAll('.descrip');
shortened.forEach(function(el) {
  el.addEventListener('click', expand);
})
*/

function updateOrderTotal() {
    const itemCount = document.getElementById('numitems');
    const totalPrice = document.getElementById('totprice');
    let count = 0;
    let price = 0;

    document.querySelectorAll('#order_pizzas .qtynum').forEach(function (input) {
        const quantity = Number(input.value);
        const rowPrice = Number(input.closest('tr').querySelector('.price').textContent.replace('$', ''));
        count += quantity;
        price += quantity * rowPrice;
    });

    itemCount.textContent = count;
    totalPrice.textContent = price;
}

document.addEventListener('DOMContentLoaded', function () {
    const orderForm = document.getElementById('order_pizzas');
    if (!orderForm) return;

    orderForm.querySelectorAll('.qty button').forEach(function (button) {
        button.addEventListener('click', function () {
            const input = button.parentElement.querySelector('.qtynum');
            const change = button.classList.contains('+') ? 1 : -1;
            input.value = Math.max(0, Number(input.value) + change);
            updateOrderTotal();
        });
    });

    orderForm.querySelectorAll('.expand').forEach(function (button) {
        button.addEventListener('click', function () {
            button.closest('tr').querySelectorAll('.long').forEach(function (element) {
                element.classList.toggle('hidden');
            });
            button.textContent = button.textContent === '^' ? '⌄' : '^';
        });
    });
});

function verifNum(event) {
  event.target.value = event.target.value.replace(/\D/g, '');
}

document.querySelectorAll('input.number').forEach(function (el) { 
  el.addEventListener('input', verifNum);
})
