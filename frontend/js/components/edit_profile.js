
// profileEditor.js

document.getElementById('editProfileBtn').addEventListener('click', () => {
    const section = document.getElementById('editNicknameSection');
    section.classList.toggle('hidden');
});

document.getElementById('saveNickname').addEventListener('click', () => {
    const newNickname = document.getElementById('nicknameInput').value.trim();
    if (newNickname) {
        document.getElementById('userName').textContent = newNickname;
        document.getElementById('editNicknameSection').classList.add('hidden');
    }
});
