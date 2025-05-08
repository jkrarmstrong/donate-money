
// Variables
const amountButtons = document.querySelectorAll('.preset_btn');
const donationInput = document.querySelector('.donation_input');


amountButtons.forEach(button => {
    button.addEventListener('click', () => {
        const value = button.getAttribute('data-amount');
        donationInput.value = value;
    });
});


donationInput.addEventListener('focus', () => {
  donationInput.placeholder = '';
});


donationInput.addEventListener('blur', () => {
  if (donationInput.value === '') {
    donationInput.placeholder = '$$$';
  }
});

