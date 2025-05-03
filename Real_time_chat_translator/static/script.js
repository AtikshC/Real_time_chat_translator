/**
 * Author: Atiksh Chawla
 * Date: May 2, 2025
 */

const socket = io();
const chatDiv = document.getElementById('chat');
const sendBtn = document.getElementById('send');
const usernameInput = document.getElementById('username');
const langSelect = document.getElementById('lang');
const targetInput = document.getElementById('target');

// Register user and set default language
function register() {
  const uname = usernameInput.value.trim() || 'User';
  socket.emit('register', { username: uname });
  socket.emit('set_language', { lang: langSelect.value });
}
usernameInput.addEventListener('change', register);
langSelect.addEventListener('change', () => {
  socket.emit('set_language', { lang: langSelect.value });
});
register();

sendBtn.addEventListener('click', () => {
  const msg      = document.getElementById('message').value.trim();
  const username = usernameInput.value.trim() || 'User';
  const target   = targetInput.value.trim();
  if (!msg || !target) return;

  // Local echo of own message
  const me = document.createElement('p');
  me.className = 'text-right text-gray-700';
  me.innerHTML = `<span class="bg-green-200 inline-block p-1 rounded-md">${msg}</span>`;
  chatDiv.appendChild(me);
  chatDiv.scrollTop = chatDiv.scrollHeight;

  socket.emit('send_message', { msg, username, target });
  document.getElementById('message').value = '';
});

socket.on('receive_message', data => {
  const p = document.createElement('p');
  p.className = 'text-left text-gray-800';
  p.innerHTML = `<span class="bg-blue-200 inline-block p-1 rounded-md"><strong>${data.username}:</strong> ${data.translated}</span>`;
  chatDiv.appendChild(p);
  chatDiv.scrollTop = chatDiv.scrollHeight;
});

socket.on('error', data => {
  alert(data.msg);
});