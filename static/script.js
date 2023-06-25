const signInButton = document.querySelector('.sign-in .sub');

signInButton.addEventListener('click', (event) => {
  event.preventDefault();
  window.location.href = 'signin-success.html';
});
