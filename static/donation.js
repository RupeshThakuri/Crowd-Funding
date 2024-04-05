let pay = document.getElementById('pay');
let value = document.getElementById('input_amt');
pay.addEventListener('click', () => {
    fetch('/redirect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: value.value }),
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.redirect;
    });
});
