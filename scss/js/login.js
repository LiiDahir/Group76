document.getElementById('loginToggle').addEventListener('click', function() {
  document.getElementById('loginForm').classList.remove('hidden');
  document.getElementById('signupForm').classList.add('hidden');
});

document.getElementById('signupToggle').addEventListener('click', function() {
  document.getElementById('signupForm').classList.remove('hidden');
  document.getElementById('loginForm').classList.add('hidden');
});
