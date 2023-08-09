const signInButton = document.querySelector('.sign-in .sub');

signInButton.addEventListener('click', (event) => {
  event.preventDefault();
  window.location.href = 'signin-success.html';
});

// Function to display the error message as a window.alert popup
function displayErrorPopup(errorMessage) {
  window.alert(errorMessage);
}

// Get the error message from the HTML template and display it as a popup
var errorElement = document.getElementById('error-message');
if (errorElement) {
  var errorMessage = errorElement.textContent;
  displayErrorPopup(errorMessage);
}
